import ast
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
    # Find all Python files in a specific directory and its subdirectories
    files = file_operations.find_files_with_extension(
        r"C:\Users\aluno\AppData\Local\Programs\Python\Python310\Lib\multiprocessing", ".py")
    # r"c:\Users\aluno\AppData\Local\Programs\Python\Python310\Lib\site-packages\PIL", ".py")
    # r"C:\Users\aluno\AppData\Local\Programs\Python\Python310\Lib\urllib", ".py")

    classes_data = []
    for file in files:
        file = r"first_try\examples\test.py"
        tree = ast_from_file(file)
        classes = class_nodes(tree)
        print(file)
        for node_class in classes:
            # print_node(node_class)
            my_visitor = ast_visitors.ASTVisitor()
            classes_data.append(my_visitor.visit(node_class))
        break

    # for class_data in classes_data:
    #     print(class_data, "\n")

    dict_classes = [current_class.to_dict() for current_class in classes_data]

    file_operations.save_to_json(
        data=dict_classes, filename=r"ast_analysis\class.json")
