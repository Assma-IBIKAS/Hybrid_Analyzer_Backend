from google import genai
from google.genai import types
from dotenv import load_dotenv
import os


load_dotenv()
GENAI_API_KEY = os.getenv("Gemini_API_KEY")

# Créer le client Gemini
client = genai.Client(api_key=GENAI_API_KEY)

def call_gemini(text: str, category: str) -> dict:
    
    try:
        # Prompt Engineering
        prompt = f"""
            Texte : {text}
            Catégorie : {category}

            Tu es un expert en résumé de textes.

            Objectifs :
            - Fournir un résumé court, clair et facile à lire.
            - Rendre le résumé fluide et structuré en quelques lignes.
        """


        # Appel de l'API Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(
                    thinking_budget=1
                )
            )
        )

        summary_text = response.text

        # Détection simple du ton
        tone = "neutre"
        lower_text = summary_text.lower()
        if "positif" in lower_text:
            tone = "positif"
        elif "negatif" in lower_text:
            tone = "negatif"

        return {
            "summary": summary_text,
            "tone": tone
        }

    except Exception as e:
        print("Erreur Gemini :", e)
        return {
            "summary": "",
            "tone": "unknown"
        }

# # Test du service
# if __name__ == "__main__":
#     texte_exemple = "L'intelligence artificielle transforme le secteur financier en améliorant la détection de fraude."
#     categorie_exemple = "Finance"

#     resultat = call_gemini(texte_exemple, categorie_exemple, max_length=50)
#     print("Résumé :", resultat["summary"])
#     print("Ton :", resultat["tone"])
