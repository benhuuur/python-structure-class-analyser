from data_class import data_class
import second_prototype.reader as reader

context = None

lines = reader.get_lines("teste.py")


for line in lines:
    identation_level = reader.get_identation_level(line)

    if(not line.strip()):
        continue
    
    if "class " in line:
        class_header = reader.get_class_header(line)
        data = data_class(class_header["name"], class_header["heritage"], identation_level)
        print(context)
        context = data
        continue

    # print(line)
    # print(identation_level)

    # try:
    #     print(identation_level > context.get_identation_level())
    #     print("\n")
    # except:
    #     pass

    if context != None and identation_level > context.get_identation_level():
        # print(line)
        pass
    # elif context != None and identation_level <= context.get_identation_level():
    #     # print(context)
    #     # print("\n")
    #     context = None
