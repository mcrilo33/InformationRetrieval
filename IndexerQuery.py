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
from TextRepresenter import PorterStemmer

class IndexerQuery(Indexer):
    
    def __init__(self, collectionPath, parser):
        
        Indexer.__init__(self, collectionPath, parser)
        
    def elementsFromDoc(self, doc):
        
        elements = {}
        text = re.sub(r'.*?\n', '', doc.getText())
        

        '''
        stop_words = set(stopwords.words('english'))

        # preprocessing
        text = text.lower()
        text = re.sub(r'(!|#|"|%|\$|\'|&|\)|\(|\+|\*|(^| )(-( |$))+|,|/|\.|;|:|=|<|\?|>|@|[|]|\|_|^|`|{|}|\||~)', ' ', text)
        text = re.sub(r'\n', ' ', text)
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'(^| )(\w($| ))+', ' ', text)
        text = re.sub(r' +', ' ', text)
        text = text.split()

        for word in text:
            if word not in stop_words:
                word = stem(word)
                if word in elements:
                    elements[word] += 1
                else:
                    elements[word] = 1
        
        return elements
        ''' 
        stemmer = PorterStemmer()
        return stemmer.getTextRepresentation(text)
