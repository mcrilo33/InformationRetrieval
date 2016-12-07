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
        self.loadIndex = {}
        
        
    def idf(self, elements):
        
        result = {}
        
        for element in elements:
            if element in indexer.invIndex:
                result[element] = \
                self.nDoc / float(len(indexer.getDfFromEl(element))-1)
            else:
                result[element] = 0
        
        return result
        
    def loadWeightsFromDoc(self, name):
        
        end = re.search(r'\..*?$', self.indexer.collectionPath).group(0)
        self.path = re.sub(r'\..*?$', name, self.indexer.collectionPath)+end
        self.indexPath = re.sub(r'\..*?$', 'Index', self.path)+end
        
        if os.path.isfile(self.indexPath):
            indexFile = open(self.indexPath)
            self.loadIndex = pickle.load(indexFile)
            indexFile.close()
        else:
            weightsFile = open(self.path, "w")
            pos = 0
            for id in self.indexer.index:
                toWrite = ''
                elements = self.computeWeightsFromDoc(id)
                elements.pop(-1)
                for element in elements:
                    toWrite += ':'+element+':'+str(elements[element])
                toWrite = toWrite[1:]
                # Get pos in index and size of current rep
                self.loadIndex[id] = [pos, len(toWrite)]
                
                weightsFile.write(toWrite)
                pos += len(toWrite)

            weightsFile.close()
            
            # Indexes'hashtable of doc in col
            indexFile = open(self.indexPath, "w")
            pickle.dump(self.loadIndex, indexFile)
        
            indexFile.close()
            
    def getWeightsFromDoc(self, id):
        
        data = self.indexer.getData(self.path, self.loadIndex, id)
        return self.indexer.freqFromData(data)
        
    def computeWeightsFromDoc(self, id):
        
        raise ValueError('Abstract method')
    
    def getWeightsFromQuery(self, query):
        
        raise ValueError('Abstract method')
        
            
class Weighter1(Weighter):
    
    def __init__(self, indexer):
        
        Weighter.__init__(self, indexer)
        name = 'Weighter1'
        self.loadWeightsFromDoc(name)
        
    def computeWeightsFromDoc(self, id):
        
        return indexer.getEfFromDoc(id)
    
    def getWeightsFromQuery(self, query):
        
        weights = copy(query)
        
        for element in weights:
            weights[element] = 1
        
        return weights
        
class Weighter2(Weighter):
    
    def __init__(self, indexer):
        
        Weighter.__init__(self, indexer)
        name = 'Weighter2'
        self.loadWeightsFromDoc(name)
        
    def computeWeightsFromDoc(self, id):
        
        return indexer.getEfFromDoc(id)
    
    def getWeightsFromQuery(self, query):
        
        weights = copy(query)
        
        return weights
        
class Weighter3(Weighter):
    
    def __init__(self, indexer):
        
        Weighter.__init__(self, indexer)
        name = 'Weighter3'
        self.loadWeightsFromDoc(name)
        
    def computeWeightsFromDoc(self, id):
        
        return indexer.getEfFromDoc(id)
    
    def getWeightsFromQuery(self, query):
        
        return self.idf(query)

class Weighter4(Weighter):
    
    def __init__(self, indexer):
        
        Weighter.__init__(self, indexer)
        name = 'Weighter4'
        self.loadWeightsFromDoc(name)
        
    def computeWeightsFromDoc(self, id):
        
        weights = indexer.getEfFromDoc(id)
        
        for element in weights:
            weights[element] = 1 + np.log(weights[element])
            
        return weights
    
    def getWeightsFromQuery(self, query):
        
        return self.idf(query)
                       
class Weighter5(Weighter):
    
    def __init__(self, indexer):
        
        Weighter.__init__(self, indexer)
        name = 'Weighter5'
        self.loadWeightsFromDoc(name)
        
    def computeWeightsFromDoc(self, id):
        
        weights = indexer.getEfFromDoc(id)
        
        idf = self.idf(weights)
        
        for element in weights:
            weights[element] = \
            (1 + np.log(weights[element])) * idf[element]
            
        return weights
    
    def getWeightsFromQuery(self, query):
        
        weights = copy(query)
        
        idf = self.idf(weights)
        
        for element in weights:
            weights[element] = \
            (1 + np.log(weights[element])) * idf[element]
            
        return weights
