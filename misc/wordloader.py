import os

def prod(word:str, nocap, ranged):
    if nocap is True:
        if any(i.isupper() for i in word):
            word = ""
    if ranged != [0,0]:
        least = ranged[0]
        try:
            most = ranged[1]
        except:
            most = ranged[0]
        if least <= len(word) <= most:
            pass
        else:
            word = ""
    return word

def wordloader(document:str, encode="ascii", nocap=False, ranged=[0,0]):
    document_place = os.path.join(os.getcwd(),"wordlist", document)
    with open(document_place, encoding=encode) as doc:
        data = []
        line = doc.readline()
        while line:
            get = prod(line.rstrip(),nocap,ranged)
            if get != "":
                data.append(get)           
            line = doc.readline()
    return data
        
