import numpy as np
import pickle

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
        
        results = np.zeros((len(self.models), len(self.queries), len(self.measures)))
        resume = np.zeros((len(self.models), 2))
        descModels = []
        
        i = 0
        for model in self.models:
            print('Computing Model '+str(i)+'... ', model.__dict__)
            descModels.append(model.__dict__)
            j = 0
            for query in self.queries:
                k = 0
                scores = model.getRanking(query.el)
                irlist = IRList(query, scores)
                for measure in self.measures:
                    measure = measure(irlist)
                    results[i,j,k] = measure.eval()
                    k += 1
                j += 1
            resume[i, 0] = np.mean(results[i,:,:])
            resume[i, 1] = np.var(results[i,:,:])
            i += 1
        
        self.descModels = descModels
        self.resume = resume
        self.outcome = results
    
    def getResults(self):
        
        return self.outcome
        
    def getResume(self):
        
        return self.resume

    def getModels(self):
        
        return self.descModels

def saveResults(models, queries, measures, path):

    EM = EvalIRModel(models, queries, measures)
    results = EM.getResults()
    resume = EM.getResume()
    models = EM.getModels()

    # Save results
    resultPath = 'results/'+path+'Results.txt'
    resumePath = 'results/'+path+'Resume.txt'
    modelsPath = 'results/'+path+'Models.txt'
    resultFile = open(resultPath, 'w')
    resumeFile = open(resumePath, 'w')
    modelsFile = open(modelsPath, 'w')
    pickle.dump(results, resultFile)
    pickle.dump(resume, resumeFile)
    pickle.dump(models, modelsFile)
    resultFile.close()
    resumeFile.close()
    modelsFile.close()
