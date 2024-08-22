import add_files
from run_commands import run_commands

def main():
    # Add files from projet_redaction
    files = add_files.main()
    result = f"Added {len(files)} files from projet_redaction."
    
    # Run commands systematically
    run_commands()
    
    return result + " Continue with the next action."

if __name__ == "__main__":
    print(main())
