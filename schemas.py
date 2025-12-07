from pydantic import BaseModel
from datetime import datetime
from typing import List

#Reçoit les informations envoyées par l’utilisateur pour s’inscrire
class UserRequest(BaseModel):
    username: str
    password: str

#Reçoit les informations pour se connecter
class UserLogin(BaseModel):
    username: str
    password: str

#Ce que le backend renvoie après inscription
class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    created_at: datetime


#Ce que le backend renvoie après connexion
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


#ce que tu reçois du frontend
class AnalyzeRequest(BaseModel):
    text: str
    labels: List[str] = ["Finance", "RH", "IT", "Opérations", "Marketing"]

#ce que tu renvoies au frontend
# Modèle de réponse 
class AnalyzeResponse(BaseModel):
    category: str
    score: float
    summary: str
    tone: str