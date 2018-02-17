from bs4 import BeautifulSoup
from collections import Counter
from datetime import datetime
from numpy import mean
from os import listdir
from os.path import dirname, realpath                                                                                                                           
from re import search, sub
from requests import get, post
from xml.etree import ElementTree

start = datetime.now()

print("starting create stopwords from downloaded metadata")

# should I lowercase everything??
def tokenize(text):
    punctuation = ["%3A","%3B","%3C","%3D","%3E","%3F","{","}","-","_","/",":","_",".","\\",">","<","&amp;","=","+","'",'"',"&","#","%2C",")","(","@","?",":","!",";",","]
    for p in punctuation:
        text = text.replace(p, " ")
    terms = text.split()
    terms = [term for term in terms if not search("\d", term)]
    return terms

PATH_TO_DIRECTORY_OF_THIS_FILE = dirname(realpath(__file__))  

stopwords = set()
with open(PATH_TO_DIRECTORY_OF_THIS_FILE + "/manually_added_tags.txt") as f:
    tags = set(f.read().strip().split("\n"))
document_count = Counter()
term_tfidf = {}
document_terms = []
term_frequencies = []
number_of_documents = 0

path_to_metadata = PATH_TO_DIRECTORY_OF_THIS_FILE + "/metadata"
for metatype in listdir(path_to_metadata):
    path_to_metatype = path_to_metadata + "/" + metatype
    if metatype == "ESRI":
        # need to add in parsing of b's in html
        for filename in listdir(path_to_metatype):
            try:
                number_of_documents += 1
                term_count = Counter()
                path_to_file = path_to_metatype + "/" + filename
                with open(path_to_file) as f:
                    text = f.read()
                for b in BeautifulSoup(text).findAll("b"):
                    tags.add(b.text)
                terms = tokenize(text)
                term_count.update(terms)
                number_of_terms = len(terms)
                term_frequency = dict([(term, float(count)/number_of_terms) for term, count in list(term_count.items())])
                term_frequencies.append(term_frequency)
                document_count.update(set(terms))

            except Exception as e:
                print("CAUGHT EXCEPTION for file", path_to_file)
                print(e)
    else:
        for filename in listdir(path_to_metatype):
            try:
                number_of_documents += 1
                term_count = Counter()
                path_to_file = path_to_metatype + "/" + filename
                with open(path_to_file) as f:
                    text = f.read()
                for element in ElementTree.fromstring(text).findall(".//*"):
                    tag = element.tag
                    tags.add(tag)
                    tags.add(tag.split("}")[-1])
                terms = tokenize(text)
                #print "terms:", terms[:5], "..."
                term_count.update(terms)
                number_of_terms = len(terms)
                term_frequency = dict([(term, float(count)/number_of_terms) for term, count in list(term_count.items())])
                term_frequencies.append(term_frequency)
                document_count.update(set(terms))

            except Exception as e:
                print("CAUGHT EXCEPTION for file", path_to_file)
                print(e)

document_frequency = dict([(term, float(count)/number_of_documents) for term, count in list(document_count.items())])
print("document_frequency:", document_frequency['html'], document_frequency["ESRI"])
for term_frequency in term_frequencies:
    #print "term_frequency:", term_frequency
    for key in term_frequency:
        tf = float(term_frequency[key])
        df = float(document_frequency[key])
        tfidf = tf / df
        if key in term_tfidf:
            term_tfidf[key].append(tfidf)
        else:
            term_tfidf[key] = [tfidf]

avg_tfidf = dict([ (term, mean(tfidfs)) for term, tfidfs in list(term_tfidf.items())])

lowest_to_highest = sorted(list(avg_tfidf.items()), key=lambda tup: tup[1])
#print "lowest:", sorted(x, key=lambda tup: -1*tup[1])[:10]
stopwords = [key for key, tfidf in lowest_to_highest if tfidf < 1]
with open(PATH_TO_DIRECTORY_OF_THIS_FILE + "/stopwords.txt", "wb") as f:
    f.write("\n".join(stopwords))

with open(PATH_TO_DIRECTORY_OF_THIS_FILE + "/tags.txt", "wb") as f:
    f.write("\n".join(sorted(tags)))

                                                                                                                                                               
print("tags:", tags)
