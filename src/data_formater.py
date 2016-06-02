# -*- coding: utf-8 -*-

"""
Created on Mon May 30 13:10:29 2016

@author: Akshay Gulati
@contact: akshaygulati95600[at]gmail.com
@topic: Entity-Relation-Entity triple
"""

from bs4 import BeautifulSoup

import re
import nltk
import settings

Stopwords = nltk.corpus.stopwords.words('english')
Word_Stem = nltk.stem.SnowballStemmer('english')
Sentence_Tokenizer = nltk.data.load('file:' + settings.path + '/dep/tokenizer/english.pickle')

Punctuations = [',', '.', '<', '>', '/', '?', ';', ':', '\'', '``', '\'\'', '"', '`', '~', '!', '^', '@', '#', '*', '(', ')', '-', '_', '+', '=', '[', ']', '{', '}', '\\' ]

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

def Formatize_Well(Sentence):
    
    Sentence = re.sub(" ('[a-z]) ", "\g<1> ", Sentence)
    Sentence = re.sub(" ([\.;,-]) ", "\g<1> ", Sentence)
    Sentence = re.sub(" ([\.;,-?!])$", "\g<1>", Sentence)
    Sentence = re.sub(" ' ", "' ", Sentence)
    Sentence = re.sub(" _ (.+) _ ", " -\g<1>- ", Sentence)
    Sentence = re.sub("`` ", "\"", Sentence)
    Sentence = re.sub(" ''", "\"", Sentence)
    Sentence = re.sub("\s+", " ", Sentence)
    Sentence = re.sub("(\w+) n't", "\g<1>n't", Sentence)
    
    return Sentence.strip()
