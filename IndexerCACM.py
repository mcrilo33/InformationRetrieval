import os
import re
import pickle
import string
import operator
import linecache as lin
import numpy as np
from ParserCACM import *
from Indexer import *
from porter import *
from copy import *
from nltk.corpus import stopwords

class IndexerCACM(Indexer):
    
    def __init__(self, collectionPath, parser):
        
        Indexer.__init__(self, collectionPath, parser)
        
    def elementsFromDoc(self, doc):
        
        elements = {}
        text = doc.getText()
        
        # preprocessing
        text = text.lower()
        exclude = set(string.punctuation)
        exclude.remove("-")
        text = ''.join(word for word in text if word not in exclude)
        # removes digit and \n
        text = re.sub(r'\d+|\n', '', text)
        # removes one letter words
        text = re.sub(r'(^| )(\w( |$))+', ' ', text)
        text = text.split()
        
        for word in text:
            word = stem(word)
            if word in elements:
                elements[word] += 1
            else:
                elements[word] = 1
        
        return elements
        
