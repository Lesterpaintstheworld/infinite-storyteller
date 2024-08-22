import add_file

if __name__ == "__main__":
    files = add_file.main()
    if files:
        print("Files to add:")
        for file in files:
            print(file)
    else:
        print("No files to add.")
