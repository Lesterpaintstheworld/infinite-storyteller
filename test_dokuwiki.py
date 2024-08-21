import requests
import json
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Informations de connexion
DOKUWIKI_URL = os.getenv("DOKUWIKI_URL")
API_URL = f"{DOKUWIKI_URL}/lib/exe/xmlrpc.php"
USERNAME = os.getenv("DOKUWIKI_USERNAME")
PASSWORD = os.getenv("DOKUWIKI_PASSWORD")

def get_session_cookie():
    """Se connecte à DokuWiki et retourne le cookie de session."""
    login_data = {
        "u": USERNAME,
        "p": PASSWORD,
    }
    response = requests.post(f"{DOKUWIKI_URL}/doku.php", data=login_data)
    return response.cookies.get("DokuWiki")

def create_page(title, content):
    """Crée une nouvelle page sur DokuWiki."""
    session_cookie = get_session_cookie()
    
    headers = {
        "Cookie": f"DokuWiki={session_cookie}",
        "Content-Type": "application/json",
    }
    
    data = {
        "method": "wiki.putPage",
        "params": [title, content, {"sum": "Test de création de page via API"}],
        "id": 1
    }
    
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        print(f"Page '{title}' créée avec succès.")
    else:
        print(f"Erreur lors de la création de la page : {response.status_code}")
        print(response.text)

# Test de création d'une page
if __name__ == "__main__":
    create_page("TestPage", "Ceci est un test de création de page via l'API DokuWiki.")
