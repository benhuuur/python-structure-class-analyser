import ast
import os
from pprint import pprint

import file_operations
import ast_visitors


def ast_from_file(file_path: str) -> ast.AST:
    """
    Parses the given Python file and returns the abstract syntax tree (AST) representation.

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
        with open(file_path, "r", encoding=file_operations.detect_encoding(file_path)) as file:
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


def print_node(node: ast.stmt):
    """
    Pretty prints the node structure.

    Args:
    - node: Abstract syntax tree node representation of the Python code.
    """
    pprint(ast.dump(node))


def class_nodes(tree: ast.AST) -> list:
    """
    Extracts ClassDef nodes from the AST.

    Args:
    - tree (ast.AST): Abstract syntax tree of the Python code.

    Returns:
    - list: List of ClassDef nodes found in the AST.
    """
    visitor = ast_visitors.ClassNodeVisitor()
    visitor.visit(tree)
    return visitor.classes


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Current directory: {current_dir}")

    # Find parent directory
    parent_dir = os.path.dirname(current_dir)
    print(f"Parent directory: {parent_dir}")

    # Uncomment to add parent directory to sys.path
    # sys.path.append(parent_dir)

    # Find all Python files in a specific directory and its subdirectories
    files = file_operations.find_files_with_extension(
        # r"C:\Users\aluno\AppData\Local\Programs\Python\Python310\Lib\multiprocessing", ".py")
        r"c:\Users\aluno\AppData\Local\Programs\Python\Python310\Lib\site-packages\PIL", ".py")
    # r"C:\Users\aluno\AppData\Local\Programs\Python\Python310\Lib\urllib", ".py")
    # r"C:\Users\aluno\Desktop\TCC_SENAI_IA-main\TCC_SENAI_IA-main", ".py")

    classes_data = []

    # Process each Python file
    for file in files:
        tree = ast_from_file(file)
        classes = class_nodes(tree)
        print(file)
        # Process each class node in the file
        for node_class in classes:
            print_node(node_class)
            my_visitor = ast_visitors.ASTVisitor()
            classes_data.append(my_visitor.visit(node_class))

    # Print class information
    for class_data in classes_data:
        print(class_data, "\n")

    # Convert class information to dictionaries
    dict_classes = [current_class.to_dict() for current_class in classes_data]

    # Save class information to a JSON file
    file_operations.save_to_json(data=dict_classes, filename="class.json")
