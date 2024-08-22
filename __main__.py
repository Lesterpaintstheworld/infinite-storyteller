import run_main

if __name__ == "__main__":
    result = run_main.main()
    print(result)

    # Print the list of files (optional)
    files = run_main.get_files_in_directory("projet_redaction")
    if files:
        print("\nFiles added:")
        for file in files:
            print(file)
    else:
        print("\nNo files found in projet_redaction directory.")
