import os
import sys
import requests
from urllib.parse import quote
from dotenv import load_dotenv
import fnmatch
import pathlib
import base64
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Chargement des variables d'environnement
load_dotenv()

# Configuration
DOKUWIKI_URL = os.getenv('DOKUWIKI_URL')
USERNAME = os.getenv('DOKUWIKI_USERNAME')
PASSWORD = os.getenv('DOKUWIKI_PASSWORD')

# Timeout for requests in seconds
REQUEST_TIMEOUT = 10

def test_connection():
    """Teste la connexion au serveur DokuWiki."""
    try:
        response = requests.get(f"{DOKUWIKI_URL}/lib/exe/xmlrpc.php", timeout=REQUEST_TIMEOUT, auth=(USERNAME, PASSWORD))
        response.raise_for_status()
        print(f"Connexion au serveur DokuWiki réussie. URL: {DOKUWIKI_URL}")
        return True
    except requests.exceptions.ConnectionError as e:
        print(f"Erreur de connexion : Impossible de se connecter à {DOKUWIKI_URL}")
        print(f"Détails de l'erreur : {str(e)}")
        print("Vérifiez que l'URL du wiki est correcte et que le serveur est accessible.")
        print(f"URL utilisée : {DOKUWIKI_URL}")
        print(f"Nom d'utilisateur : {USERNAME}")
        return False
    except requests.exceptions.Timeout:
        print(f"Erreur de connexion : Le délai d'attente de {REQUEST_TIMEOUT} secondes a été dépassé.")
        print(f"URL tentée : {DOKUWIKI_URL}")
        print("Le serveur wiki pourrait être surchargé ou inaccessible.")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la connexion au serveur DokuWiki : {str(e)}")
        print(f"URL tentée : {DOKUWIKI_URL}")
        print("Vérifiez vos informations de connexion dans le fichier .env")
        return False

def sanitize_pagename(name):
    """Convertit un nom de fichier en un nom de page DokuWiki valide."""
    return name.replace(' ', '_').lower()

def get_file_content(file_path):
    """Lit le contenu d'un fichier en essayant différents encodages."""
    encodings = ['utf-8', 'iso-8859-1', 'windows-1252']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue
    print(f"Erreur : Impossible de lire le fichier {file_path} avec les encodages connus.")
    return None

def page_exists(pagename):
    """Vérifie si une page existe déjà sur le wiki."""
    url = f"{DOKUWIKI_URL}/lib/exe/xmlrpc.php"
    headers = {'Content-Type': 'application/xml'}
    
    xml_template = f"""
    <?xml version="1.0"?>
    <methodCall>
      <methodName>wiki.getPage</methodName>
      <params>
        <param><value><string>{pagename}</string></value></param>
      </params>
    </methodCall>
    """
    
    response = requests.post(url, data=xml_template, headers=headers, auth=(USERNAME, PASSWORD))
    return response.status_code == 200 and response.text.strip() != ''

def create_or_update_page(pagename, content):
    """Crée ou met à jour une page sur le wiki."""
    url = f"{DOKUWIKI_URL}/lib/exe/xmlrpc.php"
    headers = {'Content-Type': 'application/xml'}
    
    action = "mise à jour" if page_exists(pagename) else "création"
    
    # Encoder le contenu en UTF-8
    content_encoded = content.encode('utf-8')
    content_base64 = base64.b64encode(content_encoded).decode('ascii')
    
    xml_template = f"""
    <?xml version="1.0"?>
    <methodCall>
      <methodName>wiki.putPage</methodName>
      <params>
        <param><value><string>{pagename}</string></value></param>
        <param><value><base64>{content_base64}</base64></value></param>
        <param><value><struct>
          <member>
            <name>sum</name>
            <value><string>{action.capitalize()} automatique</string></value>
          </member>
        </struct></value></param>
      </params>
    </methodCall>
    """
    
    print(f"Tentative de {action} de la page '{pagename}'...")
    try:
        response = requests.post(url, data=xml_template, headers=headers, auth=(USERNAME, PASSWORD))
        response.raise_for_status()
        print(f"Page '{pagename}' {action} avec succès.")
        try:
            print(f"Contenu de la page (premiers 100 caractères) : {content[:100]}...")
        except UnicodeEncodeError:
            print("Impossible d'afficher le contenu de la page en raison de caractères non encodables.")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la {action} de la page '{pagename}': {str(e)}")
    print(f"URL de la page : {DOKUWIKI_URL}/doku.php?id={quote(pagename)}")
    print("-" * 50)

def create_namespace(namespace):
    """Crée une structure de namespace si elle n'existe pas."""
    parts = namespace.split(':')
    current_namespace = ''
    for part in parts:
        current_namespace = f"{current_namespace}:{part}" if current_namespace else part
        if not page_exists(current_namespace):
            create_or_update_page(current_namespace, f"====== {part.capitalize()} ======\n\nCette page est un espace de noms.")

def process_directory(directory, wiki_namespace='', ignore_patterns=None):
    """Parcourt récursivement le répertoire et crée/met à jour les pages correspondantes."""
    if ignore_patterns is None:
        ignore_patterns = read_ignore_patterns(directory)

    if wiki_namespace:
        create_namespace(wiki_namespace)
    
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        relative_path = os.path.relpath(item_path, directory)

        if any(fnmatch.fnmatch(relative_path, pattern) for pattern in ignore_patterns):
            print_flush(f"Ignoré : {item_path}")
            continue

        if os.path.isfile(item_path):
            file_name, file_extension = os.path.splitext(item)
            pagename = sanitize_pagename(f"{wiki_namespace}:{file_name}" if wiki_namespace else file_name)
            content = get_file_content(item_path)
            if content is not None:
                create_or_update_page(pagename, content)
            else:
                print_flush(f"Impossible de traiter le fichier {item_path}. Il sera ignoré.")
        elif os.path.isdir(item_path):
            new_namespace = f"{wiki_namespace}:{sanitize_pagename(item)}" if wiki_namespace else sanitize_pagename(item)
            process_directory(item_path, new_namespace, ignore_patterns)

def create_index_page(directory, wiki_namespace=''):
    """Crée une page d'index pour le dossier courant."""
    index_content = f"====== Index de {wiki_namespace or 'la racine'} ======\n\n"
    for item in sorted(os.listdir(directory)):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            file_name, _ = os.path.splitext(item)
            pagename = sanitize_pagename(f"{wiki_namespace}:{file_name}" if wiki_namespace else file_name)
            index_content += f"  * [[{pagename}|{file_name}]]\n"
        elif os.path.isdir(item_path):
            subdir_name = sanitize_pagename(item)
            subdir_index = f"{wiki_namespace}:{subdir_name}:index" if wiki_namespace else f"{subdir_name}:index"
            index_content += f"  * [[{subdir_index}|{item}]]\n"
    
    create_or_update_page(f"{wiki_namespace}:index" if wiki_namespace else 'index', index_content)

def read_ignore_patterns(directory):
    """Lit les fichiers .gitignore et .aiderignore et retourne les patterns à ignorer."""
    ignore_patterns = []
    ignore_files = ['.gitignore', '.aiderignore']
    
    for ignore_file in ignore_files:
        file_path = os.path.join(directory, ignore_file)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                ignore_patterns.extend(line.strip() for line in f if line.strip() and not line.startswith('#'))
    
    return ignore_patterns

if __name__ == "__main__":
    if not all([DOKUWIKI_URL, USERNAME, PASSWORD]):
        print("Erreur : Les informations de connexion au wiki sont manquantes dans le fichier .env")
        print("Assurez-vous que DOKUWIKI_URL, DOKUWIKI_USERNAME et DOKUWIKI_PASSWORD sont définis.")
        print(f"DOKUWIKI_URL actuel : {DOKUWIKI_URL}")
        print(f"DOKUWIKI_USERNAME actuel : {USERNAME}")
        print("DOKUWIKI_PASSWORD : [Non affiché pour des raisons de sécurité]")
        sys.exit(1)

    folder_path = os.path.dirname(os.path.abspath(__file__))
    print_flush(f"Début de la synchronisation du dossier '{folder_path}' avec le wiki...")
    print(f"URL du wiki : {DOKUWIKI_URL}")
    print(f"Utilisateur : {USERNAME}")
    
    print_flush("Test de la connexion au wiki...")
    if not test_connection():
        print_flush("Impossible de se connecter au wiki. Vérifiez vos paramètres de connexion et l'état du serveur.")
        sys.exit(1)
    
    try:
        ignore_patterns = read_ignore_patterns(folder_path)
        process_directory(folder_path, ignore_patterns=ignore_patterns)
        create_index_page(folder_path)
        print_flush("Synchronisation terminée avec succès.")
    except UnicodeEncodeError as e:
        print(f"Une erreur d'encodage est survenue lors de la synchronisation : {str(e)}")
        print("Certains caractères ne peuvent pas être encodés correctement.")
        sys.exit(1)
    except Exception as e:
        print_flush(f"Une erreur est survenue lors de la synchronisation : {str(e)}")
        sys.exit(1)
