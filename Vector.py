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
                
    def norm2(self, vector):
        
        result = 0
        
        for element in vector:
            result += float(np.power(vector[element], 2))
        
        return float(np.sqrt(result))
    
    def getScores(self, query):
        
        vecQuery = self.weighter.getWeightsFromQuery(query)
        vecQuery.pop(-1)
        norm2VecQuery = self.norm2(vecQuery)
        
        doc = {}
        
        for id in query:
            
            if id in self.indexer.invIndex:
                for element in self.indexer.getDfFromEl(id):
                    doc[element] = id
        doc.pop(-1)
        
        scores = np.zeros(self.nDoc, [('id', 'a25'), ('score', 'float64')])
        
        i = 0 
        for id in self.indexer.index:
            
            scores[i]['id'] = str(id)
            
            if id in doc:
                vecDoc = self.weighter.getWeightsFromDoc(id)
                vecDoc.pop(-1)
                dotProduct = self.dotProduct(vecDoc, vecQuery)

                if self.normalized: 
                    scores[i]['score'] = dotProduct/(self.norm2(vecDoc)*norm2VecQuery)
                else:
                    scores[i]['score'] = dotProduct

            else:
                scores[i]['score'] = 0
                
            i += 1
        
        return np.array(scores)
        
