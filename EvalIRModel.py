import numpy as np

class IRList(object):
    
    def __init__(self, query, scores):
        
        self.query = query
        self.scores = scores

class EvalIRModel(object):
    
    def __init__(self, models, queries, measures):
        
        self.models = models
        self.queries = queries
        self.measures = measures
        self.results()
        
    def results(self):
        
        results = np.zeros((len(self.models), len(self.queries), len(self.measures)+2))
        
        i = 0
        for model in self.models:
            j = 0
            for query in self.queries:
                k = 0
                scores = model.getScores(query.el)
                irlist = IRList(query, scores)
                for measure in self.measures:
                    measure = measure(irlist)
                    results[i,j,k] = measure.eval()
                    k += 1
                results[i,j,-2] = np.mean(results[i,j,:-2])
                results[i,j,-1] = np.var(results[i,j,:-2])
                j += 1
            i += 1
        
        self.outcome = results
    
    def getResults(self):
        
        return self.outcome
        
