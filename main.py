from AST.AST_handler import AST_handler
from JSON_serializer import JSON_serializer

tree = AST_handler.get_AST("examples\GPT_teste.py")

classes = AST_handler.get_classes(tree.body)
print("\n")

dict_classes = list()
for curr_class in classes:
    dict_classes.append(curr_class.to_dict())

JSON_serializer.save_to_json(data=dict_classes, filename="class.json")
