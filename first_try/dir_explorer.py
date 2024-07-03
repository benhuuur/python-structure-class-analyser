import ast
from os import listdir, walk
from os.path import isfile, join, isdir
import re

from AST.AST_handler import AST_handler
from JSON.JSON_serializer import JSON_serializer


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

            # Check if the file matches any ignore pattern
            if (any(pattern in item_path for pattern in ignore_patterns) and len(patterns) > 0):
                # Ignore this file if it matches any pattern
                continue

            if isdir(item_path):
                files += dir_explorer.get_files_from_dir(
                    item_path, ignore_patterns)

            elif isfile(item_path):
                files.append(item_path)

        return files
    
    def get_files_with_extension(directory, extension):
        files = []
        for item in listdir(directory):
            item_path = join(directory, item)
            if isdir(item_path):
                files += dir_explorer.get_files_with_extension(
                    item_path, extension)
            elif item.endswith(extension):
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
    patterns.append("README.md")
    
    classes = list()
    for file in dir_explorer.get_files_with_extension(
        # "C:\\Users\\aluno\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\urllib", ".py"):
        "c:\\Users\\aluno\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\PIL", ".py"):
        print(file)
        tree = AST_handler.get_AST(file)
        # AST_handler.print_tree(tree)
        classes += AST_handler.get_classes(tree.body)


    dict_classes = list()
    for current_class in classes:
        dict_classes.append(current_class.to_dict())
    
    JSON_serializer.save_to_json(data=dict_classes, filename="first_try/class.json")