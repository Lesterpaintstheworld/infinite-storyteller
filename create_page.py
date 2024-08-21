import os

def create_page(title, content):
    """
    Crée une nouvelle page avec le titre et le contenu spécifiés.
    """
    # Nettoyer le titre pour l'utiliser comme nom de fichier
    filename = title.lower().replace(" ", "_") + ".txt"
    
    # Vérifier si le fichier existe déjà
    if os.path.exists(filename):
        print(f"La page '{title}' existe déjà.")
        return False
    
    # Créer le fichier et écrire le contenu
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"Titre: {title}\n\n")
        file.write(content)
    
    print(f"La page '{title}' a été créée avec succès.")
    return True

# Test de la fonction
if __name__ == "__main__":
    titre = input("Entrez le titre de la page : ")
    contenu = input("Entrez le contenu de la page : ")
    create_page(titre, contenu)
