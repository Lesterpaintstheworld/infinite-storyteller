import add_files

if __name__ == "__main__":
    files = add_files.main()
    print("Files to add:")
    for file in files:
        print(file)
