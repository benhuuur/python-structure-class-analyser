import re

def get_file_text(file_path):
    """Lê um arquivo e retorna seu conteúdo."""
    with open(file_path, "r") as file:
        return file.read()

def get_lines(file_path):
    """Lê um arquivo e retorna suas linhas como uma lista."""
    with open(file_path, "r") as file:
        lines = [line.rstrip('\n') for line in file.readlines()]
    return lines

def filter_string(string_filter, string):
    """Faz uma busca usando uma expressão regular na string fornecida."""
    return re.search(string_filter, string)

def get_class_in_line(line):
    """Extrai o nome da classe de uma linha que contenha 'class ... (' ou 'class ... :'."""
    result = filter_string(r'class\s+(\w+)\s*\(', line)
    if not result:
        result = filter_string(r'class\s+(\w+)\s*\:', line)
    return result.group(1) if result else None

def get_class_heritage_in_line(line):
    """Extrai o conteúdo entre parênteses de uma linha que define uma classe."""
    result = filter_string(r'class\s+\w+\s*\((.*?)\)\s*:', line)
    return result.group(1).strip() if result else ""

def get_class_header(line):
    """Retorna um dicionário com o nome da classe e seu conteúdo entre parênteses."""
    class_name = get_class_in_line(line)
    class_heritage = get_class_heritage_in_line(line)
    return {
        'name': class_name,
        'heritage': class_heritage
    }


def get_identation_level(line):
    letters = list(line)
    identation_level = 0
    for letter in letters:
        if letter == " ":
            identation_level += 1
        else:
            return identation_level

if __name__ == "__main__":
    # # Exemplo de uso
    # line = "class Humano( Ser_Vivo ):"
    # class_name = get_class_in_line(line)
    # class_heritage = get_class_heritage_in_line(line)
    # print(f"Nome da classe: {class_name}")        # Saída: Humano
    # print(f"Herança da classe: {class_heritage}") # Saída: Ser_Vivo

    # Exemplo de uso:
    texto_com_identacao = "     if True:"
    print(get_identation_level(texto_com_identacao))  # Saída: True
    texto_com_identacao = " if True:"
    print(get_identation_level(texto_com_identacao))  # Saída: True
    texto_sem_identacao = "if True:"
    print(get_identation_level(texto_sem_identacao))  # Saída: False

