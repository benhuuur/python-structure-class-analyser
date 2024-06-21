import ast

from function_info import function_info
from assignments_info import assignments_info


class AST_handler:
    @staticmethod
    def get_AST(file_path):
        with open(file_path, "r") as file:
            return ast.parse(file.read())

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
                assignments.append(AST_handler._get_assignment(statement))
        return assignments

    @staticmethod
    def _get_assignment(statement):
        # print(print(ast.dump(statement)))
        assignment_names = list()
        for target in statement.targets:
            if isinstance(target, ast.Name):
                assignment_names.append(target.id)
            elif isinstance(target, ast.Tuple):
                assignment_names = [name.id for name in target.elts if isinstance(name, ast.Name)]
        print(assignment_names)
        assignment_encapsulation = [f"Private" if name.startswith('_') else f"Public" for name in assignment_names]
        return assignments_info(name=assignment_names, data_type=None, encapsulation=assignment_encapsulation)

    
