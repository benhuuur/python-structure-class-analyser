from py_class_extractor import generate_classes_dicts_from_file, generate_classes_dicts_from_directory
from py_class_extractor.file_management import save_data_to_json

if __name__ == "__main__":
    save_data_to_json("class.json", generate_classes_dicts_from_directory(
        r"C:\Users\Aluno\AppData\Local\Programs\Python\Python312\Lib\tkinter"))
    save_data_to_json("class.json",  generate_classes_dicts_from_file(
        r"C:\Users\Aluno\AppData\Local\Programs\Python\Python312\Lib\tkinter\simpledialog.py"))
