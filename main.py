import reader

classes_name = set()

rows = reader.getLines("teste.py")
print(rows)
for row in rows:
    if "class " in row:
        row_copy = row
        class_name = row_copy.replace(":", " ").replace("(", " ").split()[1]
        classes_name.add(class_name)
        # if()

print(classes_name)