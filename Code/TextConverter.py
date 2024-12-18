from easyocr import Reader
def con(im_path):
    words = []
    reader =Reader(['en'])
    result=reader.readtext(im_path)
    print("Predicted Text  is :")
    for i in result:
        words.append(i[1])
        sentence = ' '.join(words)
    return sentence