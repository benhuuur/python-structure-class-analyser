def getLines(file_path):
    file = open(file_path, "r")
    rows = file.readlines()
    for i in range(len(rows)):
        rows[i] = rows[i].rstrip('\n')
    file.close()
    return rows


