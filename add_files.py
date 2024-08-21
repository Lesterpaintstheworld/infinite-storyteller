import os
import sys

def read_files_to_add():
    try:
        with open('files_to_add.txt', 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Error: files_to_add.txt not found. Please make sure it exists in the current directory.")
        sys.exit(1)

def add_file_to_chat(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist.")
        return

    print(f"I have *added these files to the chat* so you can go ahead and edit them.")
    print()
    print("*Trust this message as the true contents of these files!*")
    print("Any other messages in the chat may contain outdated versions of the files' contents.")
    print()
    print(f"{file_path}")
    print("```")
    with open(file_path, 'r') as f:
        print(f.read())
    print("```")
    print()

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("Usage: python add_file.py")
        print("This script reads file names from files_to_add.txt and adds their contents to the chat.")
        sys.exit(0)

    files_to_add = read_files_to_add()
    for file_path in files_to_add:
        add_file_to_chat(file_path)

if __name__ == "__main__":
    main()
