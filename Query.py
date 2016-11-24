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

class Query(object):

    def __init__(self, id, text="", el=None, relevants=None):
        
        self.id = id
        self.text = text
        self.el = el
        self.relevants = relevants
        
def query(id, queriesIndexer, relevantIndexer):
    
    id = str(id)
    text = queriesIndexer.getObjFromDoc(id).getText()
    el = queriesIndexer.getEfFromDoc(id)
    relevants = relevantIndexer.getObjFromDoc(id).get('tab')
    
    return Query(id, text, el, relevants)
