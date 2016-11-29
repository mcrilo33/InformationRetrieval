import numpy as np

class EvalMeasure():
    
    def __init__(self, irlist):
        
        self.irlist = irlist
        
    def recall(self, i):
        
        recall = \
        np.in1d(self.irlist.scores[:i]['id'], self.irlist.query.relevants).sum()
        
        return recall/float(len(self.irlist.query.relevants))
    
    def precision(self, i):
        
        precision = \
        np.in1d(self.irlist.scores[:i]['id'], self.irlist.query.relevants).sum()
    
        return precision/float(i)
    
    def eval(self, k):
    
        raise ValueError('Abstract method')
        
class EvalPrecisionRecall(EvalMeasure):
    
    def __init__(self, irlist):
        
        EvalMeasure.__init__(self, irlist)
        
        size = len(self.irlist.scores)
        self.recalls = np.zeros(size)
        self.precisions = np.zeros(size)
        for i in range(1, size):
            self.recalls[i] = self.recall(i)
            self.precisions[i] = self.precision(i)
        self.recalls = np.array(self.recalls)
        self.precisions = np.array(self.precisions)
        
    def eval(self, k=20):
        
        measures = np.zeros((k, 2))
        
        # gives good levels between 0 and 1
        levels = [(1/float(k+1))*l for l in range(1, k+1)]
        
        i = 0
        for level in levels:
            measures[i,0] = level
            wh = self.precisions[np.where(self.recalls >= level)]
            if len(wh) > 0:
                measures[i,1] = np.max(wh)
            else:
                measures[i,1] = 0
            i += 1
            
        
        return np.mean(measures[:,1])

class EvalPrecisionAverage(EvalMeasure):
    
    def __init__(self, irlist):
        
        EvalMeasure.__init__(self, irlist)
        
    def eval(self):
        
        self.irlist.query.relevants = np.array(self.irlist.query.relevants)
        return np.mean([self.precision(i) for i in np.argwhere(np.in1d(self.irlist.scores['id'], self.irlist.query.relevants[:,0]))])
            
            
        
