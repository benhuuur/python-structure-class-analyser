from os import listdir, walk
from os.path import isfile, join, isdir
import re


class dir_explorer:
    @staticmethod
    def get_files_from_dir(directory, ignore_patterns=None):
        """
        Recursively retrieves all files in a directory and its subdirectories.

        Args:
        - directory (str): Directory path to start exploring.
        - ignore_patterns (list, optional): List of patterns for files to be ignored.

        Returns:
        - list: List of file paths found in the directory and its subdirectories.
        """
        if ignore_patterns is None:
            ignore_patterns = []

        files = []

        for item in listdir(directory):
            item_path = join(directory, item)

            if isdir(item_path):
                files += dir_explorer.get_files_from_dir(
                    item_path, ignore_patterns)
            elif isfile(item_path):
                # Check if the file matches any ignore pattern
                if any(re.match(pattern, item) for pattern in ignore_patterns):
                    continue  # Ignore this file if it matches any pattern

                files.append(item_path)

        return files

    def get_ignore_patterns(gitignore_path):
        """
        Reads the .gitignore file and extracts patterns for ignored files.

        Args:
        - gitignore_path (str): Path to the .gitignore file.

        Returns:
        - list: List of patterns for files to be ignored.
        """
        ignore_patterns = []
        with open(gitignore_path, "r") as file:
            for line in file:
                # Ignore comments and empty lines
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                # Handle negation patterns
                if line.startswith("!"):
                    continue

                pattern = line.replace(
                    "/", "").replace("*", "").split()[0].strip()
                ignore_patterns.append(pattern)

        return ignore_patterns


if __name__ == "__main__":
    patterns = dir_explorer.get_ignore_patterns(".gitignore")
    patterns.append(".gitignore")
    patterns.append(".git")
    print(dir_explorer.get_files_from_dir("C:\\Users\\aluno\\Desktop\\python-structure-generator",
          ))
