import ast
from pprint import pprint
from data_class import data_class
from data_function import data_function

from second_prototype.reader import get_file_text

classes = list()

tree = ast.parse(get_file_text("teste.py"))

for node in tree.body:
    if isinstance(node, ast.ClassDef):
        bases = [base.id for base in node.bases]

        methods = []
        atributes = []
        for data in node.body:
            if isinstance(data, ast.FunctionDef):
                method_name = data.name  # Nome da função
                argument_names = [arg.arg for arg in data.args.args]  # Nomes dos argumentos
                method = data_function(method_name, argument_names)
                methods.append(method)

            if isinstance(data, ast.Assign):
                atributes = [Name.id for Name in data.targets]            

        curr_data = data_class(node.name, bases, atributes, methods)
        classes.append(curr_data)


for dt_class in classes:
    print(dt_class)

# print("\n")
# pprint(ast.dump(tree))