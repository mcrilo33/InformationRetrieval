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
    
class Indexer(object):
    '''Build an Index from a Collection'''
    
    def __init__(
        self, collectionPath,
        parser,
        fromCol="",
        repPath="",
        repIndexPath="",
        repInvPath="",
        repInvIndexPath="",
        repInvFromAllPath="",
        linkPath="",
        linkIndexPath=""
    ):
        
        # parser is a Parser object
        self.parser = parser
                 
        # collectionPath is a String object
        self.collectionPath = collectionPath
        end = re.search(r'\..*?$', collectionPath).group(0)
                 
        # Path names
        if repPath=="":
            self.repPath = \
                re.sub(r'\..*$', 'Rep'+end, self.collectionPath)
        else:
            self.repPath = repPath
        if fromCol=="":
            self.fromCol = \
                re.sub(r'\..*$', 'Index'+end, self.collectionPath)
        else:
            self.fromCol = fromCol
        if repIndexPath=="":
            self.repIndexPath = \
                re.sub(r'\..*$', 'Index'+end, self.repPath)
        else:
            self.repIndexPath = repindexPath
        if repInvIndexPath=="":
            self.repInvIndexPath = \
                re.sub(r'\..*$', 'InvIndex'+end, self.repPath)
        else:
            self.repInvIndexPath = repInvIndexPath
        if repInvFromAllPath=="":
            self.repInvFromAllPath = \
                re.sub(r'\..*$', 'InvFromAll'+end, self.repPath)
        else:
            self.repInvFromAllPath = repInvFromAllPath
        if repInvPath=="":
            self.repInvPath = re.sub(r'\..*$', 'Inv'+end, self.repPath)
        else:
            self.repInvPath
        if linkPath=="":
            self.linkPath = re.sub(r'\..*$', 'Link'+end, self.collectionPath)
        else:
            self.linkPath
        if linkIndexPath=="":
            self.linkIndexPath = re.sub(r'\..*$', 'LinkIndex'+end, self.collectionPath)
        else:
            self.linkIndexPath
        
        # Loads Hashtables if they exist
        if os.path.isfile(self.repIndexPath):
            repIndexFile = open(self.repIndexPath)
            self.index = pickle.load(repIndexFile)
            repIndexFile.close()
        else:
            self.index = {}
        if os.path.isfile(self.fromCol):
            fromColFile = open(self.fromCol)
            self.indexFromCol = pickle.load(fromColFile)
            fromColFile.close()
        else:
            self.indexFromCol = {}
        if os.path.isfile(self.repInvIndexPath):
            repInvIndexFile = open(self.repInvIndexPath)
            self.invIndex = pickle.load(repInvIndexFile)
            repInvIndexFile.close()
        else:
            self.invIndex = {}
        if os.path.isfile(self.repInvFromAllPath):
            repInvFromAllFile = open(self.repInvFromAllPath)
            self.repInvFromAll = pickle.load(repInvFromAllFile)
            repInvFromAllFile.close()
        else:
            self.repInvFromAll = {}
        if os.path.isfile(self.linkIndexPath):
            linkIndexFile = open(self.linkIndexPath)
            self.linkIndex = pickle.load(linkIndexFile)
            linkIndexFile.close()
        else:
            self.linkIndex = {}
            
        self.elements = {} # elements in self for optimisation reasons
        
    def __filters(self, doc):
        '''Filters applied to each document of the collection'''
        
        return True
    
    def getData(self, rep, index, id):
        '''Return Something frequencies from a rep and his index at id==id'''
        
        id = str(id)
        
        if index=={}:
            raise ValueError('Index undefined')
        if not(os.path.isfile(rep)):
            raise ValueError('Rep file does no exist')
        if not(id in index):
            raise ValueError('Bad Identifier')
             
        pos = index[id]
        repFile = open(rep, 'r')
        repFile.seek(pos[0])
        rep = repFile.read(pos[1])
        repFile.close()
        
        return rep
        
    def freqFromData(self, data):
    
        freq = {}
        total = 0
        rep = data.split(':')
        
        for i in range(0, len(rep), 2):
            added = float(rep[i+1])
            freq[rep[i]] = added
            total += added
        freq[-1] = total
        
        return freq
    
    def __updatePosElements(self, doc):
        '''Update pos and size of each element in inv index'''
        
        elements = self.elementsFromDoc(doc)
        id = len(doc.getId())
        
        for element in elements:
            
            added = id+len(str(elements[element]))+2
            if element in self.elements:
                self.elements[element] += added
            else:
                self.elements[element] = added-1
            
        return self.elements
    
    def elementsFromDoc(self, doc):
        '''Return an hashtable of the count of each element in a doc'''
        
        raise ValueError('Abstract method')
    
    def getEfFromDoc(self, id):
        '''Return the element frequencies of a doc with identifier==id'''
        
        data = self.getData(self.repPath, self.index, str(id))
        return self.freqFromData(data)
            
    def getDfFromEl(self, element):
        '''Return the document frequencies of an element'''
        
        data = self.getData(self.repInvPath, self.invIndex, str(element))
        return self.freqFromData(data)
        
    def getLinkFromDoc(self, id):
        '''Return the links of a document'''
        
        return np.unique(self.getData(self.linkPath, self.linkIndex, str(id)).split(";"))

    def getStrFromDoc(self, id):
        '''Return the string of a doc with identifier==id in Col'''
        
        return self.getData(self.collectionPath, self.indexFromCol, str(id))
    
    def getObjFromDoc(self, id):
        '''Return the object of a doc with identifier==id in Col'''
        
        return self.parser.getDocument(self.getStrFromDoc(id))
    
    def createIndex(self):
        
        self.parser.initFile(self.collectionPath)
        posCol = self.parser.file.tell()
        doc = self.parser.nextDocument()
        self.indexFromCol = {}
        
        while doc!=None:
            
            posCol2 = self.parser.file.tell()
        
            if self.__filters(doc)==True:
                # Get pos in col and size of current doc
                self.indexFromCol[doc.getId()] = [posCol, posCol2-posCol]
                
            doc = self.parser.nextDocument()
            posCol = posCol2
            
        # Indexes'hashtable of doc in col
        fromCol = open(self.fromCol, "w")
        pickle.dump(self.indexFromCol, fromCol)
        
        fromCol.close()
        
    def createRepIndex(self):
            
        self.parser.initFile(self.collectionPath)
        posCol = self.parser.file.tell()
        doc = self.parser.nextDocument()
        repFile = open(self.repPath, "w")
        pos = 0
        self.index = {}
        self.indexFromCol = {}
        
        while doc!=None:
            
            posCol2 = self.parser.file.tell()
            
            if self.__filters(doc)==True:
                # Get rep of current doc
                elements = self.elementsFromDoc(doc)
                toWrite = ''
                for element in elements:
                    toWrite += ':'+element+':'+str(elements[element])
                toWrite = toWrite[1:]
                # Get pos in index and size of current rep
                self.index[doc.getId()] = [pos, len(toWrite)]
                # Get pos in col and size of current doc
                self.indexFromCol[doc.getId()] = [posCol, posCol2-posCol]
                
                repFile.write(toWrite)
                pos += len(toWrite)
                
            doc = self.parser.nextDocument()
            posCol = posCol2
            
        repFile.close()
        
        # Indexes'hashtable of rep
        repIndexFile = open(self.repIndexPath, "w")
        pickle.dump(self.index, repIndexFile)
        # Indexes'hashtable of doc in col
        fromCol = open(self.fromCol, "w")
        pickle.dump(self.indexFromCol, fromCol)
        
        repIndexFile.close()
        fromCol.close()
        
    def createRepInvIndex(self):
        
        # First pass
        self.parser.initFile(self.collectionPath)
        doc = self.parser.nextDocument()
        self.elements = {}
        
        while doc!=None:
            
            if self.__filters(doc)==True:
                # Updates pos and size of each element in inv index
                self.__updatePosElements(doc)
                
            doc = self.parser.nextDocument()
            
        # Get pos and size of each elements from there size in inv index
        cumsum = 0
        for element in self.elements:
            tmp = self.elements[element]
            self.elements[element] = [cumsum, tmp]
            cumsum += tmp

        # Indexes'hashtable of elements in inv index
        self.invIndex = self.elements
        repInvIndexFile = open(self.repInvIndexPath, "w")
        pickle.dump(self.invIndex, repInvIndexFile)
        repInvIndexFile.close()
        
        # Second pass
        repInvFile = open(self.repInvPath, "w")
        self.parser.initFile(self.collectionPath)
        doc = self.parser.nextDocument()
        
        while doc!=None:
            
            if self.__filters(doc)==True:
                elements = self.elementsFromDoc(doc)
                toWrite = ''
                for element in elements:
                    toWrite = doc.getId()+':'+str(elements[element])+':'
                    repInvFile.seek(self.elements[element][0])
                    if (self.elements[element][1]-len(toWrite)) < 0:
                        toWrite = toWrite[:-1]
                    repInvFile.write(toWrite)
                    self.elements[element][0] += len(toWrite)
                    self.elements[element][1] -= len(toWrite)
                    
            doc = self.parser.nextDocument()

        repInvFile.close()

        repInvIndexFile = open(self.repInvIndexPath)
        self.invIndex = pickle.load(repInvIndexFile)
        repInvIndexFile.close()

    def createRepInvFromAll(self):
        
        if self.index == {}:
            raise ValueError('Rep index undefined')
            
        if self.invIndex == {}:
            raise ValueError('Rep invIndex undefined')
            
        self.repInvFromAll = {}
        
        for element in self.invIndex:
            docs = self.getDfFromEl(element)
            docs.pop(-1)
            self.repInvFromAll[element] = np.sum([docs[doc] for doc in docs])
        
        self.repInvFromAll[-1] = 0
        for id in self.index:
            freq = self.getEfFromDoc(id)
            self.repInvFromAll[-1] += freq[-1]
                
        # Indexes'hashtable of doc in col
        repInvFromAllFile = open(self.repInvFromAllPath, "w")
        pickle.dump(self.repInvFromAll, repInvFromAllFile)

        repInvFromAllFile.close()
                       
    def createLinkIndex(self):
        
        if self.index == {}:
            raise ValueError('Rep index undefined')
            
        if self.indexFromCol == {}:
            raise ValueError('Rep invIndex undefined')
        
        self.linkIndex = {}
        
        linkFile = open(self.linkPath, "w")
        pos = linkFile.tell()
        
        for id in self.index:
            
            doc = self.getObjFromDoc(id)
            links = doc.get('links')[:-1]
            linkFile.write(links)
            pos2 = linkFile.tell()
            self.linkIndex[id] = [pos, pos2-pos]
            pos = pos2
            
        linkFile.close()
        
        linkIndexFile = open(self.linkIndexPath, "w")
        pickle.dump(self.linkIndex, linkIndexFile)
        linkIndexFile.close()
 
