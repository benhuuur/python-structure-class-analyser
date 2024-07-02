import ast
from pprint import pprint

from data_class.assignments_info import assignments_info
from data_class.class_info import class_info
from data_class.function_info import function_info
from encoder import get_encode


class AST_handler:
    @staticmethod
    def get_AST(file_path):
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
            with open(file_path, "r", encoding=get_encode(file_path)) as file:
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

    @staticmethod
    def print_tree(AST_tree):
        """
        Pretty prints the AST tree structure.

        Args:
        - AST_tree (ast.AST): Abstract syntax tree representation of the Python code.
        """
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
                bases = AST_handler._get_bases(node)

                functions = AST_handler.get_functions(node.body)

                assignments = AST_handler.get_assignments(node.body)

                for assignment in AST_handler._get_init_assignment(node.body):
                    assignments.append(assignment)

                current_class = class_info(
                    name=node.name, inheritance=bases, methods=functions, attributes=assignments)
                classes.append(current_class)
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
        
        print("_get_assignment: ")
        AST_handler.print_tree(statement)
        assignment_names = AST_handler._get_assignment_names(statement.targets)

        assignment_encapsulation = AST_handler._get_assignment_encapsulation(
            assignment_names)

        assignment_data_type = AST_handler._get_assignment_data_type(
            statement.value, len(assignment_names))

        # print("assignment_names", len(assignment_names))
        # print("assignment_data_type", len(assignment_data_type))
        # print("assignment_encapsulation", len(assignment_encapsulation))

        if (len(assignment_names) > 1):
            return [assignments_info(name=assignment_names[i], data_type=assignment_data_type[i], encapsulation=assignment_encapsulation[i]) for i in range(len(assignment_names))]

        return [assignments_info(name=assignment_names[0], data_type=assignment_data_type[0], encapsulation=assignment_encapsulation[0])]

    @staticmethod
    def _get_assignment_names(statement_targets):
        """
        Extracts assignment names from AST nodes representing assignment targets.

        Args:
        - statement_targets (list of ast.AST): List of AST nodes representing assignment targets.

        Returns:
        - assignment_names (list of str): List containing the names of assignment targets extracted from `statement_targets`.
        """
        assignment_names = list()
        for target in statement_targets:

            #   when there is direct attribution of value and one assignment on line
            if isinstance(target, ast.Name):
                assignment_names.append(target.id)

            #   when there is more than one assignment on the same line
            elif isinstance(target, ast.Tuple):
                #   when there is direct attribution
                for elt in target.elts:
                    if isinstance(elt, ast.Name):
                        assignment_names.append(elt.id)
                    elif isinstance(elt, ast.Attribute):
                        assignment_names.append(elt.attr)

            #   when there is a attribute assignment
            elif isinstance(target, ast.Attribute):
                assignment_names.append(target.attr)

        return assignment_names

    @staticmethod
    def _get_assignment_encapsulation(assignment_names):
        """
        Determines the encapsulation type for each assignment name based on its naming convention.

        Args:
        - assignment_names (list of str): List of assignment names to determine encapsulation type for.

        Returns:
        - encapsulation_types (list of str): List containing the encapsulation type ("Private" or "Public") 
          for each assignment name based on whether the name starts with an underscore (`_`) or not.
        """
        return [f"Private" if name.startswith(
            '_') else f"Public" for name in assignment_names]

    @staticmethod
    def _get_assignment_data_type(statement_value, assignment_inline=1):
        """
        Extracts assignment data type information from an AST node representing a statement value.

        Args:
        - statement_value (ast.AST): The AST node representing the statement value to extract data type information from.

        Returns:
        - assignment_data_type (list of str): A list containing extracted data type names of the statement value. 
          Each element in the list is a string representing the type name of the corresponding part of the assignment.
        """
        assignment_data_type = list()

        # AST_handler.print_tree(statement_value)

        while len(assignment_data_type) < assignment_inline:
            # print(len(assignment_data_type))
            #   when there is direct attribution of value and one assignment on line
            if isinstance(statement_value, ast.Constant) and statement_value.value is not None:
                assignment_data_type.append(
                    f"{type(statement_value.value).__name__}")

            #   when there is more than one assignment on the same line
            elif isinstance(statement_value, ast.Tuple):
                if len(statement_value.elts) == 0:
                    assignment_data_type.append("None")
                for elt in statement_value.elts:
                    #   when there is direct attribution of value
                    if isinstance(elt, ast.Constant) and elt.value is not None:
                        assignment_data_type += [f"{type(elt.value).__name__}"]

                    #   when you have initialization of a class
                    if isinstance(elt, ast.Call):
                        # TODO
                        assignment_data_type.append("None")
                        pass
                    else:
                        print(f"Type is not handle:  {type(elt)}")
                        AST_handler.print_tree(elt)
                        assignment_data_type.append("None")

            #   when it is not possible to identify, and it is necessary to analyze context
            else:
                print(f"Type is not handle:  {type(statement_value)}")
                AST_handler.print_tree(statement_value)
                assignment_data_type.append("None")

        return assignment_data_type

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

    @staticmethod
    def _handle_attribute(attribute: ast.Attribute):
        if isinstance(attribute.value, ast.Name):
            return attribute.value.id + "." + attribute.attr
        elif isinstance(attribute.value, ast.Attribute):
            return AST_handler._handle_attribute(attribute.value) + "." + attribute.attr

    @staticmethod
    def _get_bases(node):
        bases = list()
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases.append(AST_handler._handle_attribute(base))

        return bases
