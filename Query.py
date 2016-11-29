class Query(object):

    def __init__(self, id, text="", el=None, relevants=None):
        
        self.id = id
        self.text = text
        self.el = el
        self.relevants = relevants
        
def query(id, queriesIndexer, relevantIndexer):
    
    id = str(id)
    text = None
    el = None
    relevants = None

    if id in queriesIndexer.indexFromCol:
        text = queriesIndexer.getObjFromDoc(id).getText()
    if id in queriesIndexer.index:
        el = queriesIndexer.getEfFromDoc(id)
    if id in relevantIndexer.indexFromCol:
        relevants = relevantIndexer.getObjFromDoc(id).get('tab')
    
    return Query(id, text, el, relevants)
