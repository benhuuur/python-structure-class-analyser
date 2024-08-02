import ast

from class_diagram_builder.schemas import ClassInformation, FunctionInformation, AttributeInformation, RelationshipInformation


class ClassDefCollector(ast.NodeVisitor):
    """
    A NodeVisitor implementation to collect ClassDef nodes from AST.

    Attributes:
    - class_defs (list): List to store ClassDef nodes found during traversal.
    """

    def __init__(self) -> None:
        """
        Initializes an instance of ClassDefCollector.
        """
        self.class_defs = []

    def visit_ClassDef(self, node):
        """
        Visits a ClassDef node and appends it to the class_defs list.

        Args:
        - node (ast.ClassDef): ClassDef node to visit.
        """
        self.class_defs.append(node)
        self.generic_visit(node)


class ClassNodeVisitor(ast.NodeVisitor):
    """
    A NodeVisitor implementation to visit and analyze various nodes in AST and get metadata from the classes.

    Attributes:
    - current_class (ast.ClassDef or None): Current ClassDef node being visited.
    - current_function (ast.stmt or None): Current function node being visited.
    - methods (list): List to store FunctionInfo objects representing methods.
    - attributes (list): List to store AttributeInfo objects representing attributes.
    - inheritance (list): List to store inheritance information of a class.
    """

    def __init__(self) -> None:
        """
        Initializes an instance of ASTVisitor.
        """
        self.current_class: ast.ClassDef = None
        self.current_function: ast.stmt = None
        self.current_assign: ast.stmt = None
        self.methods = []
        self.attributes = []

    def visit_ClassDef(self, node: ast.ClassDef) -> ClassInformation:
        """
        Visits a ClassDef node and collects information about it.

        Args:
        - node (ast.ClassDef): ClassDef node to visit.

        Returns:
        - ClassInformation: Information about the visited class.
        """
        self.current_class = node
        self.generic_visit(node)

        class_info = ClassInformation(
            module=None, name=node.name, relationships=None, methods=self.methods, attributes=self.attributes
        )

        return class_info

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        """
        Visits a FunctionDef node and collects information about it.

        Args:
        - node (ast.FunctionDef): FunctionDef node to visit.

        Returns:
        - ast.FunctionDef: The visited function node.
        """
        args = [arg.arg for arg in node.args.args]

        function_name: str = node.name
        function_encapsulation: str = "Public" if function_name.startswith('__') and function_name.endswith(
            '__') else "Private" if function_name.startswith('_') else "Public"

        self.methods.append(FunctionInformation(
            name=function_name, args=args, return_value=None, encapsulation=function_encapsulation))

        self.current_function = node
        self.generic_visit(node)
        self.current_function = None

        return node

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AsyncFunctionDef:
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

    def visit_AnnAssign(self, node: ast.AnnAssign) -> ast.AnnAssign:
        """
        Visits an AnnAssign node (annotation assignment) and collects attribute information.

        Args:
        - node (ast.AnnAssign): AnnAssign node to visit.

        Returns:
        - ast.AnnAssign: The visited AnnAssign node.
        """
        self.current_assign = node
        self.visit(node.target)
        self.current_assign = None

        return node

    def visit_Assign(self, node: ast.Assign) -> ast.Assign:
        """
        Visits an Assign node and collects attribute information.

        Args:
        - node (ast.Assign): Assign node to visit.

        Returns:
        - ast.Assign: The visited Assign node.
        """
        self.current_assign = node
        for target in node.targets:
            self.visit(target)
        self.current_assign = None

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
            if (self.current_assign is not None):
                if (self.current_function is None) or ((self.current_function.name == "__init__") and (isinstance(self.current_assign, (ast.Assign, ast.AnnAssign)))):
                    attribute_name = node.attr
                    attribute_encapsulation = "Private" if attribute_name.startswith(
                        '_') else "Public"
                    # TODO: logic to determine attribute type
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
        if (self.current_assign is not None):
            if (self.current_function is None) or ((self.current_function.name == "__init__") and (isinstance(self.current_assign, ast.Attribute))):
                attribute_name = node.id
                attribute_encapsulation = "Private" if attribute_name.startswith(
                    '_') else "Public"
                # TODO: logic to determine attribute type
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
        return type(node.value).__name__

    def visit_Tuple(self, node: ast.Tuple) -> list:
        """
        Visits a Tuple node and retrieves its values.

        Args:
        - node (ast.Tuple): Tuple node to visit.

        Returns:
        - list: List of values in the tuple.
        """
        values = [self.visit(elt)
                  for elt in node.elts if self.visit(elt) is not None]

        return values

    def visit_arg(self, node: ast.arg) -> ast.arg:
        """
        Visits an arg node and returns it.

        Args:
        - node (arg): arg node to visit.

        Returns:
        - arg: The visited arg node.
        """
        # skipp this node
        return node


class RelationshipAnalyzer(ast.NodeVisitor):
    def __init__(self, classes: set) -> None:
        self.classes = classes
        self.relationships = list()
        self.current_inheritance: ast.stmt = None

    def visit_ClassDef(self, node: ast.ClassDef):
        for base in node.bases:
            self.current_inheritance = base
            self.relationships.append(RelationshipInformation(
                type="inheritance", related=self.visit(base)))
            self.current_inheritance = None
        return self.relationships

    def visit_Attribute(self, node: ast.Attribute):
        """
        Visits an Attribute node and retrieves the attribute name.

        Args:
        - node (ast.Attribute): Attribute node to visit.

        Returns:
        - str: The name of the visited attribute.
        """
        if self.current_inheritance is not None:
            return f"{self.visit(node.value)}.{node.attr}"

    def visit_Subscript(self, node: ast.Subscript) -> str:
        """
        Visits a Subscript node and retrieves its string representation.

        Args:
        - node (Subscript): Subscript node to visit.

        Returns:
        - str: String representation of the visited Subscript node.
        """
        # if self.current_inheritance is not None:
        return f"{self.visit(node.value)}[{self.visit(node.slice)}]"

    def visit_Name(self, node: ast.Name) -> str:
        """
        Visits a Name node and retrieves the identifier.

        Args:
        - node (ast.Name): Name node to visit.

        Returns:
        - str: The identifier of the visited name.
        """
        return node.id

    def visit_Call(self, node: ast.Call) -> str:
        function_name = self.visit(node.func)
        args = ""
        for index, arg in enumerate(node.args):
            if index != len(node.args) - 1:
                args += f"{self.visit(arg)}, "
            else:
                args += f"{self.visit(arg)}"

        return f"{function_name}({args})"

    def visit_Constant(self, node: ast.Constant) -> str:
        return node.value

    def visit_Tuple(self, node: ast.Tuple) -> str:
        values = ""
        for index, elt in enumerate(node.elts):
            if index != len(node.elts) - 1:
                values += f"{self.visit(elt)}, "
            else:
                values += f"{self.visit(elt)}"
        return f"({values})"
