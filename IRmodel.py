import numpy as np
import time

class IRmodel(object):
    
    def __init__(self, indexer):
        
        # indexer is an indexer object
        self.indexer = indexer
        self.nDoc = len(indexer.indexFromCol)
        
    def getScores(self, query):
        
        raise ValueError('Abstract method')
    
    def getRanking(self, query):
        
        start = time.time()
        
        scores = self.getScores(query)
        sorted_scores = (np.sort(scores, order='score'))[::-1]
        
        end = time.time()
        print(end - start)
        
        return sorted_scores

