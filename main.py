from class_diagram_builder import class_structure_collector, file_management, ast_management
from class_diagram_builder.schemas import ClassInformation


def get_class_metadata(class_node):
    visitor = class_structure_collector.ClassNodeVisitor()
    current_class_data: ClassInformation = visitor.visit(class_node)
    analyzer = class_structure_collector.RelationshipAnalyzer(set())
    current_class_data.relationships = analyzer.visit(class_node)
    return current_class_data


if __name__ == "__main__":
    # Find all Python files in a specified directory and its subdirectories
    target_directory = r"C:\Users\Aluno\AppData\Local\Programs\Python\Python312\Lib\tkinter"
    python_files = file_management.find_files_with_extension(
        target_directory, ".py")

    print(python_files)

    class_data_list = []
    
    is_package = False
    for python_file in python_files:
        if "__init__" in python_file:
            is_package = True
        
    for file_path in python_files:
        ast_tree = ast_management.parse_ast_from_file(file_path)
        class_nodes = ast_management.extract_class_nodes(ast_tree)
        print(file_path)
        for class_node in class_nodes:
            current_class_data = get_class_metadata(class_node)
            #TODO: find module from this class 
            current_class_data.module = file_path.replace(
                target_directory+"\\", "").replace(".py", "").replace("\\", ".")
            class_data_list.append(current_class_data)

    class_dicts = [current_class.to_dictionary()
                   for current_class in class_data_list]

    file_management.save_data_to_json(
        data=class_dicts, filename=r"class.json"
    )

    # # Find all Python files in a specified file and its subdirectories
    # target_file = r"C:\Users\Aluno\AppData\Local\Programs\Python\Python312\Lib\tkinter\__init__.py"
    # ast_tree = ast_management.parse_ast_from_file(target_file)
    # class_nodes = ast_management.extract_class_nodes(ast_tree)
    # print(target_file)
    # class_data_list = []
    # for class_node in class_nodes:
    #     class_data_list.append(get_class_metadata(class_node))

    # class_dicts = [current_class.to_dictionary()
    #                for current_class in class_data_list]

    # file_management.save_data_to_json(
    #     data=class_dicts, filename=r"class.json"
    # )
