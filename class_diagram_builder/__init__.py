import class_diagram_builder.ast_management
import class_diagram_builder.class_structure_collector
import class_diagram_builder.file_management
import class_diagram_builder.schemas

def process_file(file_path: str, base_module_name: str) -> list:
    """
    Processes a single Python file to extract class metadata.

    Args:
        file_path (str): The path to the Python file.
        base_module_name (str): The base module name used for relative paths.

    Returns:
        list: A list of class metadata objects.
    """
    ast_tree = class_diagram_builder.ast_management.parse_ast_from_file(file_path)
    import_aliases = class_diagram_builder.ast_management.extract_import_alias(ast_tree)
    class_nodes = class_diagram_builder.ast_management.extract_class_nodes(ast_tree)
    
    class_metadata_list = []
    for class_node in class_nodes:
        class_metadata = class_diagram_builder.ast_management.get_class_metadata(class_node, import_aliases)
        class_metadata.modules = class_diagram_builder.ast_management.extract_sublist_between(
            class_diagram_builder.ast_management.split_module_path(file_path), base_module_name
        )
        class_metadata_list.append(class_metadata)
    
    return class_metadata_list

def generate_class_diagram_json(file_path: str, output_path: str = "classes.json") -> None:
    """
    Analyzes the specified Python file and generates a JSON file containing class metadata.

    Args:
        file_path (str): The path to the Python file to be analyzed.
        output_path (str): The path to the output JSON file.
    """
    base_module_name = class_diagram_builder.ast_management.split_module_path(file_path)[-2]
    class_metadata_list = process_file(file_path, base_module_name)

    # Convert class metadata to dictionary format
    class_metadata_dicts = [metadata.to_dictionary() for metadata in class_metadata_list]

    # Save the class metadata to a JSON file
    class_diagram_builder.file_management.save_data_to_json(data=class_metadata_dicts, filename=output_path)

def generate_class_diagrams_from_directory(directory_path: str, output_filename: str = "classes.json") -> None:
    """
    Analyzes all Python files in the specified directory and generates a JSON file with class metadata
    for all files combined.

    Args:
        directory_path (str): The path to the directory containing Python files.
        output_filename (str): The name of the output JSON file.
    """
    python_file_paths = class_diagram_builder.file_management.find_files_with_extension(directory_path, ".py")
    base_module_name = class_diagram_builder.ast_management.split_module_path(directory_path)[-1]

    # Collect metadata for all classes across all files
    all_class_metadata_list = []
    for file_path in python_file_paths:
        all_class_metadata_list.extend(process_file(file_path, base_module_name))

    # Convert all class metadata to dictionary format
    all_class_metadata_dicts = [metadata.to_dictionary() for metadata in all_class_metadata_list]

    # Save the combined class metadata to a JSON file
    class_diagram_builder.file_management.save_data_to_json(data=all_class_metadata_dicts, filename=output_filename)
