'''
Created on 6 sept. 2016

@author: SL
'''
from Parser import Parser
from Document import Document
#===============================================================================
# /**
#  * 
#  * Format of input files :
#  * .I <id>
#  * .T 
#  * <Title>
#  * .A <Author>
#  * .K
#  * <Keywords>
#  * .W
#  * <Text>
#  * .X
#  * <Links> 
#  *
#  */
#===============================================================================
class ParserCACM(Parser):
    def __init__(self):
        '''
        Constructor
        '''
        Parser.__init__(self,".I")

    def getDocument(self,text):
        other={};
        modeT=False;
        modeA=False;
        modeK=False;
        modeW=False;
        modeX=False;
        info=""
        identifier=""
        author=""
        kw=""
        links=""
        title=""
        texte=""
        
        st=text.split("\n");
        s=""
        for s in st:
            if(s.startswith(".I")):
                identifier=s[3:]
                continue
            
            if(s.startswith(".")):
                if(modeW):
                    texte=info
                    info=""
                    modeW=False
                
                if(modeA):
                    author=info
                    info=""
                    modeA=False
                
                if(modeK):
                    kw=info;
                    info="";
                    modeK=False;
                
                if(modeT):
                    title=info;
                    info="";
                    modeT=False
                
                if(modeX):
                    other["links"]=links;
                    info="";
                    modeX=False;
                
            
            
            if(s.startswith(".W")):
                modeW=True;
                info=s[2:];
                continue;
            
            if(s.startswith(".A")):
                modeA=True;
                info=s[2:];
                continue;
            
            if(s.startswith(".K")):
                modeK=True;
                info=s[2:];
                continue;
            
            if(s.startswith(".T")):
                modeT=True;
                info=s[2:];
                continue;
            
            if(s.startswith(".X")):
                modeX=True
                continue;
            
            if(modeX):
                l=s.split("\t");
                if(l[0]!=identifier):
                    if(len(l[0])>0):
                        links+=l[0]+";";
                
                continue;
            
            if((modeK) or (modeW) or (modeA) or (modeT)):
                info+=" "+s
            
        
    
        if(modeW):
            texte=info;
            info="";
            modeW=False;
        
        if(modeA):
            author=info;
            info="";
            modeA=False;
        
        if(modeK):
            kw=info;
            info="";
            modeK=False;
        
        if(modeX):
            other["links"]=links;
            info=""
            modeX=False;
        
        if(modeT):
            title=info;
            info="";
            modeT=False;
        
        other["title"]=title
        other["text"]=texte
        other["author"]=author
        other["keywords"]=kw
        
        doc=Document(identifier,title+" \n "+author+" \n "+kw+" \n "+texte,other);
        
        return doc

#===============================================================================


#===============================================================================
# a=ParserCACM()
# a.initFile("../../data/cacm/cacm.txt")
# x1=a.nextDocument()
# print x1
# x2=a.nextDocument()
# print x2
# x3=a.nextDocument()
# print x3
# x4=a.nextDocument()
# print x4
#===============================================================================
