import os.path
import time
import urllib2
import data_formater
import  re

class Wiki_to_Document():
    
    def __init__(self,wikilink):
        
        self.Wikipedia_URL = wikilink
        self.Document = ''
        self.HTML = ''
                
    def Access_Wikipedia(self):
        
        try:
            Page = urllib2.urlopen(self.Wikipedia_URL)
            Charset = str(Page.headers['content-type'][Page.headers['content-type'].index('=') + 1:])
            self.HTML = Page.read().decode(Charset)

        except Exception as Error:
            print(str(Error))
    
    def HTML_to_Data(self):
                
        self.Document = data_formater.Remove_HTML(self.HTML)
        
        self.Document = data_formater.Remove_Brackets(self.Document)
        self.Document = data_formater.Indent_Position(self.Document)
        self.Document = data_formater.Remove_URLs(self.Document)
        self.Document = data_formater.Remove_Wikipedia_Tags(self.Document)
        
        self.Document = data_formater.Sentence_Tokenize(self.Document)   
        
         

def counting(wikilink,count):
            
            tmp = Wiki_to_Document(wikilink)           
            tmp.Access_Wikipedia()           
            tmp.HTML_to_Data()
            wiki_document = []         
            for Sentence in tmp.Document:
                    #print Sentence
                    wiki_document.append(Sentence)           

