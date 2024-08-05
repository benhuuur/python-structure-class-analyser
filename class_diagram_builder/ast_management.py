import ast

from pprint import pprint
from typing import List, Tuple
from class_diagram_builder import class_structure_collector
from class_diagram_builder import file_management
from pathlib import Path

from class_diagram_builder.schemas import ClassInformation


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


def extract_class_nodes(tree: ast.AST) -> List:
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

def extract_import_alias(tree: ast.AST):
    collector = class_structure_collector.ImportColector()
    collector.visit(tree)
    imports = collector.imports
    
    visitor = class_structure_collector.AliasVisitor()
    for import_node in imports:
        visitor.visit(import_node)
    
    return visitor.alias_import

def split_module_path(module_path: str) -> Tuple[str, ...]:
    """
    Splits a file path into its component parts and removes the file extension.

    Args:
    - module_path (str): The path to the Python module file.

    Returns:
    - Tuple[str, ...]: A tuple containing the path components with the file extension removed.

    Example:
    >>> split_module_path("src/utils/helpers.py")
    ('src', 'utils', 'helpers')
    """
    path = Path(module_path)

    # Extract parts of the path and remove the '.py' extension from the last part
    path_parts = [part for part in path.with_suffix('').parts]

    return tuple(path_parts)


def extract_sublist_between(arr, start, end=None):
    """
    Extracts a contiguous sublist from a given list starting from the specified start value up to (and including) the end value.

    Args:
    - arr (list): The list from which to extract the sublist.
    - start (any): The value to start the extraction from.
    - end (any, optional): The value to end the extraction at. If not provided, the sublist will go from the start value to the end of the list.

    Returns:
    - list: A sublist starting from the start value up to (and including) the end value. If no end value is provided, the sublist extends to the end of the list.

    Example:
    >>> extract_sublist_between(["a", "b", "c", "d", "e"], "b", "d")
    ['b', 'c', 'd']

    >>> extract_sublist_between(["a", "b", "c", "d", "e"], "b")
    ['b', 'c', 'd', 'e']
    """
    if start not in arr:
        raise ValueError("Start value not found in the list")
    start_index = arr.index(start)
    if end is None:
        return arr[start_index:]

    if end not in arr:
        raise ValueError("End value not found in the list")
    end_index = arr.index(end)

    if start_index > end_index:
        raise ValueError(
            "Start value must appear before end value in the list")

    return arr[start_index:end_index + 1]

def get_class_metadata(class_node, alias):
    visitor = class_structure_collector.ClassNodeVisitor()
    current_class_data: ClassInformation = visitor.visit(class_node)
    analyzer = class_structure_collector.RelationshipAnalyzer(set())
    current_class_data.relationships = analyzer.visit(class_node)
    return current_class_data