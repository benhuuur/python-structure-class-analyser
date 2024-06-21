import re

def get_file_text(file_path):
    """Lê um arquivo e retorna seu conteúdo."""
    with open(file_path, "r") as file:
        return file.read()
