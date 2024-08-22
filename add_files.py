import os

def get_files_in_directory(directory):
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

def main():
    directories_to_scan = [
        "projet_redaction",
        "system/story_generation",
        "system/world_simulation",
        "system/interaction_engine",
        "assets",
        "ai_society",
        "cities"
    ]
    
    files_to_add = []
    for directory in directories_to_scan:
        files_to_add.extend(get_files_in_directory(directory))
    
    return files_to_add

if __name__ == "__main__":
    files = main()
    print("Files to add:")
    for file in files:
        print(file)
