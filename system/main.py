import add_files

def main():
    files = add_files.main()
    return f"Added {len(files)} files from projet_redaction. Continue with the next action."

if __name__ == "__main__":
    print(main())
