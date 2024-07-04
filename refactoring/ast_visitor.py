from _ast import AsyncFunctionDef, Attribute, arguments
import ast
from pprint import pprint
from typing import Any

from data_class.class_info import class_info
from data_class.function_info import function_info


def print_node(node):
    """
    Pretty prints the node structure.

    Args:
    - node: Abstract syntax tree node representation of the Python code.
    """
    pprint(ast.dump(node))


class ClassVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.classes = list()

    def visit_ClassDef(self, node):
        self.classes.append(node)
        self.generic_visit(node)


class visitor(ast.NodeVisitor):
    _instance = None

    def __init__(self) -> None:
        self.current_class: ast.ClassDef = None
        self.current_function: ast.stmt = None
        self.methods: list = []
        self.attributes: set = set()
        self.inheritance: list = []

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(visitor, cls).__new__(cls)
        return cls._instance

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        self.current_class = node
        self.generic_visit(node)

        return class_info(name=node.name, inheritance=self.inheritance, methods=self.methods, attributes=self.attributes)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        args = list()
        for arg in node.args.args:
            args.append(arg.arg)

        self.methods.append(function_info(
            name=node.name, args=args, return_value=None))

        self.current_function = node
        self.generic_visit(node)
        self.current_function = None
        return node

    def visit_AsyncFunctionDef(self, node: AsyncFunctionDef) -> Any:
        args = list()
        for arg in node.args.args:
            args.append(arg.arg)

        self.methods.append(function_info(
            name=node.name, args=args, return_value=None))

        self.current_function = node
        self.generic_visit(node)
        self.current_function = None
        return node

    def visit_AnnAssign(self, node: ast.AnnAssign) -> Any:
        if self.current_function is None or self.current_function.name == "__init__":
            self.attributes.add(self.visit(node.target))
        return node

    def visit_Assign(self, node: ast.Assign) -> Any:
        for target in node.targets:
            if self.current_function is None or self.current_function.name == "__init__":
                self.attributes.add(self.visit(target))
        return node

    def visit_Attribute(self, node: Attribute) -> Any:
        if isinstance(node.value, ast.Name):
            return node.attr
        return self.visit(node.value)

    def visit_Name(self, node: ast.Name) -> Any:
        return node.id
