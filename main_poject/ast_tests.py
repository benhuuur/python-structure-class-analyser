import ast
from AST_handler import AST_handler

classes = list()

tree = AST_handler.get_AST("teste.py")


for node in tree.body:
    if isinstance(node, ast.ClassDef):
        bases = [base.id for base in node.bases]

        methods = AST_handler.get_functions(node.body)
        print(methods)

        assignments = AST_handler.get_assignments(node.body)
        print(assignments)        

        # curr_data = data_class(node.name, bases, atributes, methods)
        # classes.append(curr_data)


# for dt_class in classes:
#     print(dt_class)

# print("\n")
# pprint(ast.dump(tree))