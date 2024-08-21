import os

def get_files_in_directory(directory):
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

def main():
    files_to_add = get_files_in_directory("projet_redaction")
    print("Files to add:")
    for file in files_to_add:
        print(file)

if __name__ == "__main__":
    main()
