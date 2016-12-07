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

class IndexerCACM(Indexer):
    
    def __init__(self, collectionPath, parser):

        Indexer.__init__(self, collectionPath, parser)
        
    def elementsFromDoc(self, doc):
        
        elements = {}
        text = doc.getText()

        # preprocessing
        text = text.lower()
        text = re.sub(r'(!|#|"|%|\$|\'|&|\)|\(|\+|\*|(^| )(-( |$))+|,|/|\.|;|:|=|<|\?|>|@|[|]|\|_|^|`|{|}|\||~)', ' ', text)
        text = re.sub(r'\n', ' ', text)
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'(^| )(\w($| ))+', ' ', text)
        text = re.sub(r' +', ' ', text)
        
        stemmer = PorterStemmer()

        return stemmer.getTextRepresentation(text)
 
