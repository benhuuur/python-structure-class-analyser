import ast
from encoder import detect_encode

from ast_visitor import ClassVisitor, visitor, print_node


def AST_from_file(file_path):
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
        with open(file_path, "r", encoding=detect_encode(file_path)) as file:
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


def class_nodes(tree):
    visitor = ClassVisitor()
    visitor.visit(tree)
    return visitor.classes


if __name__ == "__main__":
    tree = AST_from_file(
        "refactoring\\Test.py")
    classes = class_nodes(tree)
    print_node(tree)
    classes_data = list()
    my_visitor = visitor()
    for node_class in classes:
        classes_data.append(my_visitor.visit(node_class))

    print(classes_data)
