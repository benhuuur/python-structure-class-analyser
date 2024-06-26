import ast
from pprint import pprint

from data_class.assignments_info import assignments_info
from data_class.class_info import class_info
from data_class.function_info import function_info


class AST_handler:
    @staticmethod
    def get_AST(file_path):
        """
        Parses the given Python file and returns the abstract syntax tree (AST) representation.

        Args:
        - file_path (str): Path to the Python file.

        Returns:
        - ast.AST: Abstract syntax tree representation of the parsed Python file.
        """
        with open(file_path, "r") as file:
            return ast.parse(file.read())

    @staticmethod
    def print_tree(AST_tree):
        """
        Pretty prints the AST tree structure.

        Args:
        - AST_tree (ast.AST): Abstract syntax tree representation of the Python code.
        """
        print("\n")
        pprint(ast.dump(AST_tree))

    @staticmethod
    def get_classes(tree_body):
        """
        Extracts class information from the AST tree body.

        Args:
        - tree_body (list): List of AST nodes.

        Returns:
        - list: List of class_info objects representing the classes found in the AST.
        """
        classes = list()
        for node in tree_body:
            if isinstance(node, ast.ClassDef):
                bases = [base.id for base in node.bases]

                functions = AST_handler.get_functions(node.body)

                assignments = AST_handler.get_assignments(node.body)
                for assignment in AST_handler._get_init_assignment(node.body):
                    assignments.append(assignment)

                curr_data = class_info(
                    name=node.name, inheritance=bases, methods=functions, attributes=assignments)
                classes.append(curr_data)
        return classes

    @staticmethod
    def get_functions(node_body):
        """
        Extracts function information from the given AST node body.

        Args:
        - node_body (list): List of AST nodes.

        Returns:
        - list: List of function_info objects representing the functions found in the node body.
        """
        functions = list()
        for statement in node_body:
            if isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append(AST_handler._get_function(statement))
        return functions

    @staticmethod
    def _get_function(statement):
        """
        Extracts detailed information about a function from its AST representation.

        Args:
        - statement (ast.FunctionDef or ast.AsyncFunctionDef): AST node representing the function.

        Returns:
        - function_info: Object containing details of the function.
        """
        function_name = statement.name
        arguments = [arg.arg for arg in statement.args.args]
        return function_info(name=function_name, args=arguments, return_value=None)

    @staticmethod
    def get_assignments(node_body):
        """
        Extracts assignment information from the given AST node body.

        Args:
        - node_body (list): List of AST nodes.

        Returns:
        - list: List of assignments_info objects representing the assignments found in the node body.
        """
        assignments = list()
        for statement in node_body:
            if isinstance(statement, ast.Assign):
                for assignment in AST_handler._get_assignment(statement):
                    assignments.append(assignment)
        return assignments

    @staticmethod
    def _get_assignment(statement):
        """
        Extracts detailed information about an assignment statement from its AST representation.

        Args:
        - statement (ast.Assign): AST node representing the assignment statement.

        Returns:
        - list: List of assignments_info objects representing each assignment target found in the statement.
        """
        assignment_names = list()
        for target in statement.targets:
            if isinstance(target, ast.Name):
                assignment_names.append(target.id)
            elif isinstance(target, ast.Tuple):
                assignment_names = assignment_names + \
                    [name.id for name in target.elts if isinstance(
                        name, ast.Name)]
            elif isinstance(target, ast.Attribute):
                assignment_names.append(target.attr)

        assignment_encapsulation = [f"Private" if name.startswith(
            '_') else f"Public" for name in assignment_names]

        print(statement.value)
        assignment_data_type = list()
        if isinstance(statement.value, ast.Constant):
            assignment_data_type.append(
                f"{type(statement.value.value).__name__}")
        if isinstance(statement.value, ast.Tuple):
            #TODO logic to handle tuple
            pass
        else:
            assignment_data_type.append("None")

        print("assignment_data_type:", len(assignment_data_type))
        print("assignment_names:", len(assignment_names))

        if (len(assignment_names) > 1):
            return [assignments_info(name=assignment_names[i], data_type=assignment_data_type[i], encapsulation=assignment_encapsulation[i]) for i in range(len(assignment_names))]
        return [assignments_info(name=assignment_names[0], data_type=assignment_data_type[0], encapsulation=assignment_encapsulation[0])]

    @staticmethod
    def _get_init_assignment(node_body):
        """
        Extracts assignment information specifically from an __init__ method in a class.

        Args:
        - node_body (list): List of AST nodes representing the body of a class or function.

        Returns:
        - list: List of assignments_info objects representing the assignments found in the __init__ method.
        """
        for statement in node_body:
            if isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef)) and statement.name == "__init__":
                return AST_handler.get_assignments(statement.body)
        return list()
