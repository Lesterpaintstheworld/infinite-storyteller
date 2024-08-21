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

def read_page(title):
    """
    Lit et affiche le contenu d'une page existante.
    """
    filename = title.lower().replace(" ", "_") + ".txt"
    
    if not os.path.exists(filename):
        print(f"La page '{title}' n'existe pas.")
        return False
    
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    
    print(f"Contenu de la page '{title}':\n")
    print(content)
    return True

# Menu principal
if __name__ == "__main__":
    while True:
        print("\n1. Créer une nouvelle page")
        print("2. Lire une page existante")
        print("3. Quitter")
        
        choice = input("Choisissez une option (1-3): ")
        
        if choice == '1':
            titre = input("Entrez le titre de la nouvelle page : ")
            contenu = input("Entrez le contenu de la page : ")
            create_page(titre, contenu)
        elif choice == '2':
            titre = input("Entrez le titre de la page à lire : ")
            read_page(titre)
        elif choice == '3':
            print("Au revoir!")
            break
        else:
            print("Option invalide. Veuillez choisir 1, 2 ou 3.")
