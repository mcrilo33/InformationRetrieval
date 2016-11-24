import numpy as np
from IRmodel import *
from Weighter import *

class Vector(IRmodel):
    
    def __init__(self, indexer, weighter=Weighter1, normalized=False):
    
        IRmodel.__init__(self, indexer)
        
        # weighter is a Weighter object
        self.weighter = weighter(indexer)
        
        # normalized is a boolean
        self.normalized = normalized
    
    def dotProduct(self, vector1, vector2):
        
        result = 0
        
        if len(vector1)>len(vector2):
            tmp = vector1
            vector1 = vector2
            vector2 = tmp
        
        for element in vector1:
            if element in vector2:
                result += vector1[element]*vector2[element]
        
        return result
                
    def norm1(self, vector):
        
        result = 0
        
        for element in vector:
            result += abs(vector[element])
        
        return result
    
    def getScores(self, query):
        
        vecQuery = self.weighter.getWeightsFromQuery(query)
        norm1VecQuery = self.norm1(vecQuery)
        
        doc = {}
        
        for id in query:
            
            if id in self.indexer.invIndex:
                for element in self.indexer.getDfFromEl(id):
                    doc[element] = 1
        doc.pop(-1)
        
        scores = np.zeros(len(doc), [('id', 'a25'), ('score', 'float64')])
        i = 0
        
        for id in doc:
            
            scores[i]['id'] = str(id)
            vecDoc = self.weighter.getWeightsFromDoc(id)
            dotProduct = self.dotProduct(vecDoc, vecQuery)
            
            if self.normalized: 
                scores[i]['score'] = dotProduct/float(self.norm1(vecDoc)*norm1VecQuery)
            else:
                scores[i]['score'] = dotProduct
            
            i += 1
        
        return np.array(scores)
        
