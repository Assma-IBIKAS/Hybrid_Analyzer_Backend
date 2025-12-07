from fastapi import FastAPI, Depends,HTTPException, status
from db import Base, SessionLocal, engine
from models import User
from schemas import *
from jose import jwt 
from dotenv import load_dotenv
import os
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
import bcrypt
from gemini_service import call_gemini
from hf_service import classify_with_hf


load_dotenv()

ALGORITHM = os.getenv('ALGORITHM')
SC = os.getenv('SC')

type_token = HTTPBearer()

Base.metadata.create_all(engine)

app = FastAPI(title = "Hybrid-Analyzer AI")

db = SessionLocal()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)


#fonction pour hasher le mot de passe avec bcrypt
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()                 # génère un salt
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')           # convertir bytes → string pour stockage



@app.get("/")
def root():
    return {"message": "Hybrid-Analyzer Backend Running"}

# Endpoint de Register
@app.post("/Register")
def signup(user: UserRequest):
    # Hasher le password
    hashed_pw = hash_password(user.password)

    # Remplacer password par password_hash
    db_user = User(
        username=user.username,
        password_hash=hashed_pw
    )

    # Enregistrer l’utilisateur
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "User Created !!"}

#Endpoint de connexion
@app.post('/login')
def login(user: UserLogin):
    # Récupérer l'utilisateur
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Vérifier le mot de passe
    if not bcrypt.checkpw(user.password.encode('utf-8'), db_user.password_hash.encode('utf-8')):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Créer le token JWT
    payload = {"sub": db_user.username}
    token = jwt.encode(payload, SC, algorithm=ALGORITHM)

    # Retourner le token
    return {"access_token": token, "token_type": "bearer"}


#Endpoint qui liste tous les utilisateurs qui ont dans la base de données
@app.get("/Users")
def get_users(credentials: HTTPAuthorizationCredentials = Depends(type_token)):
    # Récupérer le token JWT
    my_token = credentials.credentials

    try:
        # Décoder le token avec secret et algorithme
        payload = jwt.decode(my_token, SC, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    # Récupérer tous les utilisateurs de la DB
    users = db.query(User).all()

    # Transformer en liste de dictionnaires (JSON serializable)
    users_list = [
        {
            "id": u.id,
            "username": u.username,
            "created_at": u.created_at
        }
        for u in users
    ]

    return {"users": users_list}


#Endpoint analyse
@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest, payload: dict = Depends(type_token)):
    try:
        # Hugging Face
        hf_result = classify_with_hf(request.text, request.labels)
        if isinstance(hf_result, dict) and "labels" in hf_result and "scores" in hf_result:
            category = hf_result["labels"][0]
            score = hf_result["scores"][0]
        elif isinstance(hf_result, list) and len(hf_result) > 0:
            best = max(hf_result, key=lambda x: x.get("score", 0))
            category = best.get("label", "unknown")
            score = best.get("score", 0.0)
        else:
            category = "unknown"
            score = 0.0

        # Gemini
        gemini_result = call_gemini(request.text, category)

        return AnalyzeResponse(
            category=category,
            score=score,
            summary=gemini_result["summary"],
            tone=gemini_result["tone"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur Analyse: {str(e)}")