from class_diagram_builder import class_structure_collector, file_management, ast_management


if __name__ == "__main__":
    # # Find all Python files in a specified directory and its subdirectories
    # target_directory = r"C:\Users\benhuuur\AppData\Local\Programs\Python\Python311\Lib\multiprocessing"
    # python_files = file_management.find_files_with_extension(
    #     target_directory, ".py")

    # print(python_files)

    # class_data_list = []
    # for file_path in python_files:
    #     ast_tree = ast_management.parse_ast_from_file(file_path)
    #     class_nodes = ast_management.extract_class_nodes(ast_tree)
    #     print(file_path)
    #     for class_node in class_nodes:
    #         visitor = class_structure_collector.ClassNodeVisitor()
    #         class_data_list.append(visitor.visit(class_node))

    # class_dicts = [current_class.to_dictionary()
    #                for current_class in class_data_list]

    # file_management.save_data_to_json(
    #     data=class_dicts, filename=r"class.json"
    # )

    # Find all Python files in a specified file and its subdirectories
    target_file = r"C:\Users\benhuuur\AppData\Local\Programs\Python\Python311\Lib\multiprocessing\util.py"
    ast_tree = ast_management.parse_ast_from_file(target_file)
    class_nodes = ast_management.extract_class_nodes(ast_tree)
    print(target_file)
    class_data_list = []
    for class_node in class_nodes:
        visitor = class_structure_collector.ClassNodeVisitor()
        class_data_list.append(visitor.visit(class_node))

    class_dicts = [current_class.to_dictionary()
                   for current_class in class_data_list]

    file_management.save_data_to_json(
        data=class_dicts, filename=r"class.json"
    )
