import os
import requests
from dotenv import load_dotenv


load_dotenv()

HF_TOKEN = os.getenv('HF_TOKEN')

API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"
hf_headers = {
    "Authorization": f"Bearer {os.environ['HF_TOKEN']}",
    "Content-Type": "application/json"
}


def classify_with_hf(text, labels):
    
    try:
        payload = {
            "inputs": text,
            "parameters": {
                "candidate_labels": labels
            }
        }
        
        response = requests.post(
            API_URL, 
            headers=hf_headers, 
            json=payload
        )
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erreur Hugging Face: {str(e)}")


# #Test
# if __name__ == "__main__":
#     res = classify_with_hf("Le nouveau logiciel améliore les opérations de l'entreprise.",
#         ["IT", "Finance", "Opérations"])
#     print(res)