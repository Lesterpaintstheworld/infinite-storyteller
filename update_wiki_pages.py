import os
import requests
from markdown import markdown
from bs4 import BeautifulSoup

# Configuration
DOKUWIKI_URL = "http://ec2-35-180-63-1.eu-west-3.compute.amazonaws.com/dokuwiki"
USERNAME = "your_username"
PASSWORD = "your_password"
FOLDER_PATH = "./pages_to_upload"  # Chemin vers le dossier contenant les fichiers Markdown

def convert_markdown_to_dokuwiki(markdown_content):
    # Convertir Markdown en HTML
    html = markdown(markdown_content)
    
    # Utiliser BeautifulSoup pour extraire le texte et conserver certaines balises
    soup = BeautifulSoup(html, 'html.parser')
    
    # Fonction récursive pour traiter les éléments
    def process_element(element):
        if element.name == 'h1':
            return f"====== {element.get_text()} ======\n\n"
        elif element.name == 'h2':
            return f"===== {element.get_text()} =====\n\n"
        elif element.name == 'h3':
            return f"==== {element.get_text()} ====\n\n"
        elif element.name == 'p':
            return f"{element.get_text()}\n\n"
        elif element.name == 'ul':
            return ''.join([f"  * {process_element(li)}" for li in element.find_all('li', recursive=False)])
        elif element.name == 'ol':
            return ''.join([f"  - {process_element(li)}" for li in element.find_all('li', recursive=False)])
        elif element.name == 'li':
            return f"{element.get_text()}\n"
        elif element.name == 'a':
            return f"[[{element['href']}|{element.get_text()}]]"
        elif element.name == 'strong':
            return f"**{element.get_text()}**"
        elif element.name == 'em':
            return f"//{element.get_text()}//"
        else:
            return element.get_text()

    # Traiter tous les éléments de premier niveau
    dokuwiki_content = ''.join([process_element(elem) for elem in soup.body.children if elem.name])
    
    return dokuwiki_content

def update_wiki_page(page_name, content):
    session = requests.Session()
    
    # Connexion
    login_data = {
        "u": USERNAME,
        "p": PASSWORD,
        "do": "login"
    }
    session.post(f"{DOKUWIKI_URL}/doku.php", data=login_data)
    
    # Mise à jour de la page
    edit_data = {
        "id": page_name,
        "wikitext": content,
        "do": "save"
    }
    response = session.post(f"{DOKUWIKI_URL}/doku.php", data=edit_data)
    
    if response.status_code == 200:
        print(f"Page '{page_name}' mise à jour avec succès.")
    else:
        print(f"Erreur lors de la mise à jour de la page '{page_name}'.")

def main():
    for filename in os.listdir(FOLDER_PATH):
        if filename.endswith(".md"):
            file_path = os.path.join(FOLDER_PATH, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                markdown_content = file.read()
            
            dokuwiki_content = convert_markdown_to_dokuwiki(markdown_content)
            page_name = os.path.splitext(filename)[0]
            
            update_wiki_page(page_name, dokuwiki_content)

if __name__ == "__main__":
    main()
