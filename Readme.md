#  🤖 Hybrid-Analyzer 🤖

## 🎯 Contexte du projet
L’agence spécialisée en media monitoring souhaite automatiser l’analyse de centaines d’articles de presse reçus chaque jour.

Actuellement, le traitement est entièrement manuel, ce qui est :  
- Lent  
- Coûteux  
- Difficile à fiabiliser à grande échelle  
- Dépendant de l’expertise humaine pour catégoriser et synthétiser les contenus  

Pour industrialiser ce processus, la direction souhaite mettre en place une application **fullstack interne, sécurisée et maintenable**, capable d’orchestrer deux services d’IA externes :

- **Classification Zero-Shot (Hugging Face)**  
  - Modèle : `facebook/bart-large-mnli`  
  - Utilisé pour déterminer la catégorie probable d’un texte (Finance, RH, IT, Opérations, etc.)

- **Analyse et Synthèse Contextuelle (API Gemini)**  
  - Génération d’un résumé ciblé  
  - Évaluation du ton (positif, négatif, neutre)  
  - Gemini reçoit la catégorie issue de Hugging Face comme contexte dans son prompt  

La direction confie à votre équipe la conception et le développement de l’application **Hybrid-Analyzer**, qui doit garantir :  
- Sécurité  
- Qualité du code  
- Orchestrations fiables  
- Logs exploitables  
- Tests automatisés  

---

## 🔍 Le Besoin
L’entreprise souhaite une plateforme fullstack qui :  
1. Reçoit un texte brut (article, paragraphe, note)  
2. Envoie ce texte à Hugging Face pour une classification Zero-Shot  
3. Transmet ensuite la classification à Gemini pour une synthèse contextuelle  
4. Retourne au frontend un JSON structuré contenant :  
   - La catégorie prédite  
   - Le score associé  
   - Le résumé généré  
   - Le ton détecté  
5. Gère l’ensemble du workflow de façon sécurisée (authentification + gestion d’erreurs)  
6. Fournisse une interface web claire permettant :  
   - L’envoi de texte  
   - L’affichage de la classification et de la synthèse  
   - Un retour visuel (loading / success / erreurs)  


---

## 📋 La réalisation 

### 1. Backend (Python) – Orchestration complète

**Fonctionnalités à implémenter :**  
- Endpoint `/analyze` recevant un texte à analyser  
- Appel au service Hugging Face :  
  - Modèle : `facebook/bart-large-mnli`  
  - Gestion des scores faibles, timeouts, erreurs réseau, réponses invalides  
- Transmission du résultat à Gemini via un prompt contextualisé  
- Agrégation des réponses HF + Gemini  
- Retour d’un JSON structuré au frontend  
- Sécurisation du backend (JWT)   

---

### 2. Authentification JWT

**Endpoints obligatoires :**  
- `POST /register`  
  - Enregistrer un utilisateur dans PostgreSQL  
  - Stockage du mot de passe hashé (bcrypt recommandé)  
- `POST /login`  
  - Renvoie un token JWT signé  
- `POST /analyze`  
  - Protégé par JWT  

---

### 3. Base de Données PostgreSQL

- **Table `users` :**  
  | id | username | passwordhash | createdat |  

---

### 4. Intégration Hugging Face Zero-Shot Classification

- Utilisation de l’API Inference  
- Header d’authentification (token HF)  

---

### 5. Intégration de l’API Gemini

- **Prompt Engineering incluant :**  
  - Le texte source  
  - La catégorie prédite par Hugging Face  
  - Les contraintes de synthèse (longueur, ton, structure)  
- Détection du ton : positif / neutre / négatif  
- Gestion des erreurs Gemini (réponses mal formées, API down)  

---

### 6. Frontend (Next.js / React / HTML, CSS, JS)

**Pages attendues :**  
- `/analyze`  
- `/auth` : Inscription / Connexion  
- Gestion du token JWT côté client  

---

### 7. Tests Unitaires et Qualité

- Mock complet de l’API :  
  - Mock Hugging Face  
  - Mock Gemini  

---

## 🚀 Technologies Utilisées

- **Backend** : Python, FastAPI  
- **Frontend** : React / Next.js / HTML, CSS, JS  
- **Base de données** : PostgreSQL  
- **IA externes** : Hugging Face, API Gemini  
- **Sécurité** : JWT, bcrypt  

---

## Exemple de JSON retourné par `/analyze`

```json
{
  "category": "Finance",
  "score": 0.87,
  "summary": "Résumé synthétique du texte fourni...",
  "tone": "positif"
}
