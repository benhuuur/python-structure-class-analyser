import chardet

def detect_encode(filename):
    with open(filename, 'rb') as rawdata:
        result = chardet.detect(rawdata.read())
    return result['encoding']
