import os
import re
import pickle
import string
import operator
import linecache as lin
import numpy as np
from ParserCACM import *
from porter import *
from copy import *
from nltk.corpus import stopwords

class Weighter(object):
    
    def __init__(self, indexer):
        
        # Indexer is an Indexer object
        self.indexer = indexer
        self.nDoc = len(indexer.indexFromCol)
        
    def idf(self, elements):
        
        result = {}
        
        for element in elements:
            try:
                result[element] = \
                np.log(self.nDoc / float(len(indexer.getDfFromEl(element))-1))
            except:
                result[element] = 0
        
        return result
        
    def getWeightsFromDoc(self, id):
        
        raise ValueError('Abstract method')
    
    def getWeightsFromQuery(self, query):
        
        raise ValueError('Abstract method')
            
class Weighter1(Weighter):
    
    def __init__(self, indexer):
        
        Weighter.__init__(self, indexer)
        
    def getWeightsFromDoc(self, id):
        
        return indexer.getEfFromDoc(id)
    
    def getWeightsFromQuery(self, query):
        
        weights = copy(query)
        
        for element in weights:
            weights[element] = 1
        
        return weights
        
class Weighter2(Weighter):
    
    def __init__(self, indexer):
        
        Weighter.__init__(self, indexer)
        
    def getWeightsFromDoc(self, id):
        
        return indexer.getEfFromDoc(id)
    
    def getWeightsFromQuery(self, query):
        
        weights = copy(query)
        
        return weights
        
class Weighter3(Weighter):
    
    def __init__(self, indexer):
        
        Weighter.__init__(self, indexer)
        
    def getWeightsFromDoc(self, id):
        
        return indexer.getEfFromDoc(id)
    
    def getWeightsFromQuery(self, query):
        
        return self.idf(query)

class Weighter4(Weighter):
    
    def __init__(self, indexer):
        
        Weighter.__init__(self, indexer)
        
    def getWeightsFromDoc(self, id):
        
        weights = indexer.getEfFromDoc(id)
        
        for element in weights:
            weights[element] = 1 + np.log(weights[element])
            
        return weights
    
    def getWeightsFromQuery(self, query):
        
        return self.idf(query)
                       
class Weighter5(Weighter):
    
    def __init__(self, indexer):
        
        Weighter.__init__(self, indexer)
        
    def getWeightsFromDoc(self, id):
        
        weights = indexer.getEfFromDoc(id)
        
        for element in weights:
            weights[element] = \
            (1 + np.log(weights[element])) * self.idf([element])[element]
            
        return weights
    
    def getWeightsFromQuery(self, query):
        
        weights = copy(query)
        
        for element in weights:
            weights[element] = \
            (1 + np.log(weights[element])) * self.idf([element])[element]
            
        return weights
