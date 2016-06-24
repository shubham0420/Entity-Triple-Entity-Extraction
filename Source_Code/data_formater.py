# -*- coding: utf-8 -*-

"""
Created on Mon May 30 11:59:21 2016

@author: Akshay Gulati, Nitin Gupta, Shubham Sharma 
@contact: 
@topic: Entity-Relation-Entity triple extraction
@description: 
"""

#SPARQL query to return 10000 Films' JSON data
#From each Film's JSON access > all the pre-selected attributes along with their values
#                             > Wiki ID of that Film
#Using Wiki ID access the Wikipedia page of that Film
#Import alias file and do   

from bs4 import BeautifulSoup
from socket import error as SocketError

import os
import re
import nltk
import errno
import httplib
import urllib2

Sentence_Tokenizer = nltk.data.load('file:/home/top-coder/Downloads/Triple_Extractor/dep/tokenizer/english.pickle')

def Sentence_Tokenize(Data):

    return Sentence_Tokenizer.tokenize(Data)

def Word_Tokenize(Sentence):
    
    return nltk.tokenize.word_tokenize(Sentence)
    
def Remove_HTML(HTML):
    
     Soup = BeautifulSoup(HTML)
     Data = ' '.join(map(lambda p: p.text, Soup.find_all('p')))
     
     return Data

def Remove_URLs(Sentence):
    
    Sentence = re.sub('http[s]? : //(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', Sentence)
    Sentence = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', Sentence)
    return Sentence

def Remove_Wikipedia_Tags(Sentence):
    
    Sentence = re.sub(r' :[0-9]+', ' ', Sentence)
    Sentence = re.sub(r':[0-9]+', ' ', Sentence)
    return Sentence

def Remove_Brackets(Sentence):
    
    Sentence_Clean = ''
    
    Pass_Bracket_1 = 0
    Pass_Bracket_2 = 0
    Pass_Bracket_3 = 0
    
    for Char in Sentence:
        if Char == '[': 
            Pass_Bracket_1 += 1
        
        elif Char == '(':
            Pass_Bracket_2 += 1
            
        elif Char == '<':
            Pass_Bracket_3 += 1
            
        elif Char == ']' and Pass_Bracket_1 > 0:
            Pass_Bracket_1 -= 1
            
        elif Char == ')' and Pass_Bracket_2 > 0:
            Pass_Bracket_2 -= 1
        
        elif Char == '>' and Pass_Bracket_3 > 0:
            Pass_Bracket_3 -= 1
            
        elif Pass_Bracket_1 == 0 and Pass_Bracket_2 == 0 and Pass_Bracket_3 == 0:
            Sentence_Clean += Char
            
    return Sentence_Clean

def Indent_Position(Sentence):
                
    Sentence = Sentence.strip()
    Sentence = re.sub('[\n\t]', ' ', Sentence)
    Sentence = re.sub('\s+', ' ', Sentence)
    
    return Sentence

def URL_to_HTML(URL):
    
    try:
        HTML = urllib2.urlopen(URL)
    
    except urllib2.HTTPError as error:
        print u'HTTPError: {0} ({1})'.format(URL, error.code)
        
    except urllib2.URLError as error:
        print u'URLError: {0} ({1})'.format(URL, error.reason)
        
    except httplib.BadStatusLine as error:
        print u'BadStatusLine: {}'.format(URL)
    
    except SocketError as error:
        if error.errno != errno.ECONNRESET:
            raise
            
        pass
    
    else:
        Charset = HTML.headers['content-type'][HTML.headers['content-type'].index('=') + 1:]
        HTML = unicode(HTML.read(), Charset)
        return HTML


class URL_to_Wikipedia():
    
    def __init__(self, Wikipedia_URL):
        
        self.HTML = ''
        self.Document = ''
        self.Wikipedia_URL = Wikipedia_URL
                
    def Access_Wikipedia(self):
        
        self.HTML = URL_to_HTML(self.Wikipedia_URL)

    def HTML_to_Data(self):
                
        self.Document = Remove_HTML(self.HTML)
        self.Document = Remove_Brackets(self.Document)
        self.Document = Indent_Position(self.Document)
        self.Document = Remove_URLs(self.Document)
        self.Document = Remove_Wikipedia_Tags(self.Document)
        self.Document = Sentence_Tokenize(self.Document)
