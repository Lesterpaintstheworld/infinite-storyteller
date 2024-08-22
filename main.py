import os
from run_commands import run_commands

def get_files_in_directory(directory):
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

def main():
    files_to_add = get_files_in_directory("projet_redaction")
    result = f"Added {len(files_to_add)} files from projet_redaction. Continue with the next action."
    
    # Run commands systematically
    run_commands()
    
    return result

if __name__ == "__main__":
    result = main()
    print(result)
    
    # Print the list of files (optional)
    files = get_files_in_directory("projet_redaction")
    if files:
        print("\nFiles added:")
        for file in files:
            print(file)
    else:
        print("\nNo files found in projet_redaction directory.")
