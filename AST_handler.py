import ast
from pprint import pprint

from data_class.assignments_info import assignments_info
from data_class.class_info import class_info
from data_class.function_info import function_info


class AST_handler:
    @staticmethod
    def get_AST(file_path):
        with open(file_path, "r") as file:
            return ast.parse(file.read())

    @staticmethod
    def print_tree(AST_tree):
        print("\n")
        pprint(ast.dump(AST_tree))

    @staticmethod
    def get_classes(tree_body):
        classes = list()
        for node in tree_body:
            if isinstance(node, ast.ClassDef):
                bases = [base.id for base in node.bases]

                functions = AST_handler.get_functions(node.body)

                assignments = AST_handler.get_assignments(node.body)
                for assignment in AST_handler._get_init_assignment(node.body):
                    assignments.append(assignment)

                curr_data = class_info(
                    name=node.name, heritage=bases, functions=functions, assignments=assignments)
                classes.append(curr_data)
        return classes

    @staticmethod
    def get_functions(node_body):
        functions = list()
        for statement in node_body:
            if isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append(AST_handler._get_function(statement))
        return functions

    @staticmethod
    def _get_function(statement):
        function_name = statement.name
        arguments = [arg.arg for arg in statement.args.args]
        return function_info(name=function_name, args=arguments, return_value=None)

    @staticmethod
    def get_assignments(node_body):
        assignments = list()
        for statement in node_body:
            if isinstance(statement, ast.Assign):
                for assignment in AST_handler._get_assignment(statement):
                    assignments.append(assignment)
        return assignments

    @staticmethod
    def _get_assignment(statement):
        assignment_names = list()
        for target in statement.targets:
            if isinstance(target, ast.Name):
                assignment_names.append(target.id)
            elif isinstance(target, ast.Tuple):
                assignment_names = [
                    name.id for name in target.elts if isinstance(name, ast.Name)]
            elif isinstance(target, ast.Attribute):
                assignment_names.append(target.attr)
        assignment_encapsulation = [f"Private" if name.startswith(
            '_') else f"Public" for name in assignment_names]

        if (len(assignment_names) > 1):
            return [assignments_info(name=assignment_names[i], data_type=None, encapsulation=assignment_encapsulation[i]) for i in range(len(assignment_names))]
        return [assignments_info(name=assignment_names[0], data_type=None, encapsulation=assignment_encapsulation[0])]

    @staticmethod
    def _get_init_assignment(node_body):
        for statement in node_body:
            if isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef)) and statement.name == "__init__":
                return AST_handler.get_assignments(statement.body)
        return list()
