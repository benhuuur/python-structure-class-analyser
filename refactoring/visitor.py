from _ast import AnnAssign
import ast
from typing import Any


class ClassVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.classes = list()

    def visit_ClassDef(self, node):
        self.classes.append(node)
        self.generic_visit(node)


class visitor(ast.NodeVisitor):
    _instance = None
    current_class: ast.ClassDef = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(visitor, cls).__new__(cls)
        return cls._instance

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        self.current_class = node
        self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        print(node.name, self.current_class.name)
        self.generic_visit(node)
        return node
    
    def visit_AnnAssign(self, node: AnnAssign) -> Any:
        return super().visit_AnnAssign(node)

