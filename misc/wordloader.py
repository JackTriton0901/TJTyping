import os
import configparser

array = configparser.ConfigParser()
array.read("wordlist/list.ini", encoding="utf-8")
ar = array["List"]

def prod(word:str, nocap, ranged):
    if nocap is True:
        if any(i.isupper() for i in word):
            word = ""
    if ranged != [0,0]:
        least = ranged[0]
        most = ranged[1]
        if most == 0:
            if least <= len(word):
                pass
            else:
                word = ""
        else:
            if least <= len(word) <= most:
                pass
            else:
                word = ""
    return word

def wordloader(document:str, nocap=False, ranged=[0,0]):
    try:
        doc = ar[document]
    except KeyError:
        with open("wordlist/list.ini", mode="a+") as lister:
            file_path = os.path.join(os.getcwd(),"wordlist")
            for file in os.listdir(file_path):
                if file == "list.ini":
                    pass
                else:
                    for lists in os.listdir(os.path.join(file_path, file)):
                        if lists == "Info.ini":
                            pass
                        else:
                            try:
                                test = ar[lists]
                            except KeyError:
                                lister.write(lists+" = "+file+"\n")
                            if lists == document:
                                doc = file       
    document_place = os.path.join(os.getcwd(),"wordlist", doc, document)
    info = configparser.ConfigParser()
    info.read("wordlist/"+doc+"/Info.ini", encoding="utf-8")
    encode = info[document]["Encode"]
    name = info[document]["Name"]
    with open(document_place, encoding=encode) as doc:
        data = []
        line = doc.readline()
        while line:
            get = prod(line.rstrip(),nocap,ranged)
            if get != "":
                data.append(get)           
            line = doc.readline()
    return (name, data)
