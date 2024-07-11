from _ast import Subscript, arg
import ast
from typing import Any

from data_class.class_information import ClassInformation
from data_class.function_information import FunctionInformation
from data_class.attribute_information import AttributeInformation


class ClassNodeVisitor(ast.NodeVisitor):
    """
    A NodeVisitor implementation to visit and collect ClassDef nodes from AST.

    Attributes:
    - classes (list): List to store ClassDef nodes found during traversal.
    """

    def __init__(self) -> None:
        """
        Initializes an instance of ClassNodeVisitor.
        """
        self.classes = list()

    def visit_ClassDef(self, node):
        """
        Visits a ClassDef node and appends it to the classes list.

        Args:
        - node (ast.ClassDef): ClassDef node to visit.
        """
        self.classes.append(node)
        self.generic_visit(node)


class ASTVisitor(ast.NodeVisitor):
    """
    A NodeVisitor implementation to visit and analyze various nodes in AST.

    Attributes:
    - current_class (ast.ClassDef or None): Current ClassDef node being visited.
    - current_function (ast.stmt or None): Current function node being visited.
    - methods (list): List to store FunctionInfo objects representing methods.
    - attributes (list): List to store AttributeInfo objects representing attributes.
    - inheritance (list): List to store inheritance information of a class.
    """

    _instance = None

    def __new__(cls):
        """
        Ensures only one instance of ASTVisitor exists (Singleton pattern).
        """
        if not cls._instance:
            cls._instance = super(ASTVisitor, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initializes an instance of ASTVisitor.
        """
        self.current_class: ast.ClassDef = None
        self.current_function: ast.stmt = None
        self.current_attribute: ast.stmt = None
        self.methods: list = []
        self.attributes: list = []
        self.inheritance: list = []

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        """
        Visits a ClassDef node and collects information about it.

        Args:
        - node (ast.ClassDef): ClassDef node to visit.

        Returns:
        - ClassInfo: Information about the visited class.
        """
        self.current_class = node
        self.generic_visit(node)

        return ClassInformation(name=node.name, inheritance=self.inheritance, methods=self.methods, attributes=self.attributes)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        """
        Visits a FunctionDef node and collects information about it.

        Args:
        - node (ast.FunctionDef): FunctionDef node to visit.

        Returns:
        - ast.FunctionDef: The visited function node.
        """
        args = [arg.arg for arg in node.args.args]

        self.methods.append(FunctionInformation(
            name=node.name, args=args, return_value=None))

        self.current_function = node
        self.generic_visit(node)
        self.current_function = None
        return node

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> Any:
        """
        Visits an AsyncFunctionDef node and collects information about it.

        Args:
        - node (ast.AsyncFunctionDef): AsyncFunctionDef node to visit.

        Returns:
        - ast.AsyncFunctionDef: The visited async function node.
        """
        args = [arg.arg for arg in node.args.args]

        self.methods.append(FunctionInformation(
            name=node.name, args=args, return_value=None))

        self.current_function = node
        self.generic_visit(node)
        self.current_function = None
        return node

    def visit_AnnAssign(self, node: ast.AnnAssign) -> Any:
        """
        Visits an AnnAssign node (annotation assignment) and collects attribute information.

        Args:
        - node (ast.AnnAssign): AnnAssign node to visit.

        Returns:
        - ast.AnnAssign: The visited AnnAssign node.
        """
        self.current_attribute = node
        self.visit(node.target)
        self.current_attribute = None

        return node

    def visit_Assign(self, node: ast.Assign) -> Any:
        """
        Visits an Assign node and collects attribute information.

        Args:
        - node (ast.Assign): Assign node to visit.

        Returns:
        - ast.Assign: The visited Assign node.
        """
        self.current_attribute = node
        for target in node.targets:
            self.visit(target)
        self.current_attribute = None
        return node

    def visit_Attribute(self, node: ast.Attribute) -> str:
        """
        Visits an Attribute node and retrieves the attribute name.

        Args:
        - node (ast.Attribute): Attribute node to visit.

        Returns:
        - str: The name of the visited attribute.
        """
        if isinstance(node.value, ast.Name):
            if (self.current_attribute is not None):
                if (self.current_function is None) or ((self.current_function.name == "__init__") and (isinstance(self.current_attribute, (ast.Assign, ast.AnnAssign)))):
                    attribute_name = node.attr
                    attribute_encapsulation = "Private" if attribute_name.startswith(
                        '_') else "Public"

                    # TODO
                    # attribute_type =

                    self.attributes.append(AttributeInformation(
                        name=attribute_name, encapsulation=attribute_encapsulation, data_type=None))

            return node.attr
        return self.visit(node.value)

    def visit_Name(self, node: ast.Name) -> str:
        """
        Visits a Name node and retrieves the identifier.

        Args:
        - node (ast.Name): Name node to visit.

        Returns:
        - str: The identifier of the visited name.
        """

        if (self.current_attribute is not None):
            if (self.current_function is None) or ((self.current_function.name == "__init__") and (isinstance(self.current_attribute, ast.Attribute))):
                attribute_name = node.id
                attribute_encapsulation = "Private" if attribute_name.startswith(
                    '_') else "Public"

                # TODO
                # attribute_type =

                self.attributes.append(AttributeInformation(
                    name=attribute_name, encapsulation=attribute_encapsulation, data_type=None))

        return node.id

    def visit_Constant(self, node: ast.Constant) -> str:
        """
        Visits a Constant node and retrieves its value type.

        Args:
        - node (ast.Constant): Constant node to visit.

        Returns:
        - str: The type of the constant value.
        """
        return f"{type(node.value).__name__}"

    def visit_Tuple(self, node: ast.Tuple) -> Any:
        values = list()
        for elt in node.elts:
            value = self.visit(elt)
            if value is not None:
                values.append(value)
        return values

    def visit_arg(self, node: arg) -> Any:
        return node

    def visit_Subscript(self, node: Subscript) -> Any:
        return node
