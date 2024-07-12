import ast
from pprint import pprint
import class_structure_collector

import file_management


def parse_ast_from_file(file_path: str) -> ast.AST:
    """
    Parses the given Python file and returns the abstract syntax tree (AST).

    Args:
    - file_path (str): Path to the Python file.

    Returns:
    - ast.AST: Abstract syntax tree representation of the parsed Python file.

    Raises:
    - FileNotFoundError: If the file specified by `file_path` does not exist.
    - SyntaxError: If there is an error in parsing the Python code.
    - OSError: If there is a general operating system error while accessing `file_path`.
    """
    try:
        with open(file_path, "r", encoding=file_management.detect_file_encoding(file_path)) as file:
            return ast.parse(file.read())
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        raise
    except SyntaxError as e:
        print(f"Syntax error in file '{file_path}': {e}")
        raise
    except OSError as e:
        print(f"OS error while accessing file '{file_path}': {e}")
        raise


def display_ast_node(node: ast.stmt):
    """
    Pretty prints the structure of the AST node.

    Args:
    - node: Abstract syntax tree node representation of the Python code.
    """
    pprint(ast.dump(node))


def extract_class_nodes(tree: ast.AST) -> list:
    """
    Extracts ClassDef nodes from the AST.

    Args:
    - tree (ast.AST): Abstract syntax tree of the Python code.

    Returns:
    - list: List of ClassDef nodes found in the AST.
    """
    collector = class_structure_collector.ClassDefCollector()
    collector.visit(tree)
    return collector.class_defs


if __name__ == "__main__":
    # Find all Python files in a specified directory and its subdirectories
    target_directory = r"c:\Users\aluno\AppData\Local\Programs\Python\Python310\Lib\site-packages\PIL"
    python_files = file_management.find_files_with_extension(
        target_directory, ".py")

    print(python_files)

    class_data_list = []
    for file_path in python_files:
        ast_tree = parse_ast_from_file(file_path)
        class_nodes = extract_class_nodes(ast_tree)
        print(file_path)
        for class_node in class_nodes:
            visitor = class_structure_collector.ClassNodeVisitor()
            class_data_list.append(visitor.visit(class_node))

    class_dicts = [current_class.to_dictionary()
                   for current_class in class_data_list]

    file_management.save_data_to_json(
        data=class_dicts, filename=r"ast_analysis\class.json"
    )
