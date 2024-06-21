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
        assignment_name = [Name.id for Name in statement.targets]
        assignment_encapsulation = [f"privado {name}" if name.startswith('_') else f"público {name}" for name in assignment_name]
        return assignments_info(name = assignment_name, data_type=None, encapsulation= assignment_encapsulation)
    
