import os
import re
import pickle
import string
import operator
import linecache as lin
import numpy as np
from ParserCACM import *
from Indexer import *
from porter import *
from copy import *
from nltk.corpus import stopwords

class RelevantParser(Parser):

    def __init__(self):
        
        Parser.__init__(self, '')
        self.curId = None
    
    def nextDocument(self):
        
        if self.curId==None:
            self.curLine = self.file.readline()
            if self.curLine!=None:
                self.curId = ((self.curLine).split())[0]
            
        id = self.curId
        text = ''
        
        while(self.curLine!=''):
            text += self.curLine
            pos = self.file.tell()
            self.curLine = self.file.readline()
            if self.curLine!='':
                self.curId = ((self.curLine).split())[0]
            if(id!=self.curId):
                self.file.seek(pos)
                break

        if text=='':
            return None
        
        return self.getDocument(text)
        
    def getDocument(self, text):
        
        tab = \
        [
            [(i.split())[1], int((i.split())[2]), int((i.split())[3])] \
            for i in text.split('\n')[:-1] \
        ]
        
        identifier = str(int(text.split()[0]))
        
        return Document(identifier, others={'tab': tab})

