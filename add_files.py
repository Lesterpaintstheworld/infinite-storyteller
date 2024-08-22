import os

def get_files_in_directory(directory):
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

def main():
    files_to_add = get_files_in_directory("projet_redaction")
    return files_to_add

if __name__ == "__main__":
    files = main()
    print("Files to add:")
    for file in files:
        print(file)
