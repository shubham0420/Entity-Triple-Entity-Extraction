# -*- coding: utf-8 -*-

"""
Created on Mon Jun 1 00:59:21 2016

@author: Akshay Gulati
@contact: akshaygulati95600[at]gmail.com
@topic: Entity-Relation-Entity triple
"""

import io
import json
import nltk
import string
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

American_English = io.open('/usr/share/dict/american-english').read().split('\n') 
British_English = io.open('/usr/share/dict/british-english').read().split('\n') 
CrackLib_Small = io.open('/usr/share/dict/cracklib-small').read().split('\n') 

Words = American_English + British_English + CrackLib_Small
Words = set(Word.lower() for Word in Words)

def Split_String(String):
   
   Result = []
   
   def Recursive(String_Left, Words_Done):
        
        if not String_Left:
            Result.append(Words_Done)
            
        for Index in xrange(1, len(String_Left) + 1):
            if String_Left[:Index] in Words:
                Recursive(String_Left[Index:], Words_Done + [String_Left[:Index]])

   Recursive(String, [])
   
   return Result

def Read_Wikipedia_File(Index):
    
    Wikipedia_File = [Sentence.lower() for Sentence in  io.open('/home/akshay/ZIIITH_Project/database/1_wikipedia', 'r', encoding = 'utf8').read().split('\n')]
    return Wikipedia_File[:-1]

def Read_DBpedia_File(Index):
    
    DBpedia_File = io.open('/home/akshay/ZIIITH_Project/database/1_dbpedia', 'r', encoding = 'utf8').read()
    DBpedia_JSON = json.loads(DBpedia_File, encoding = 'utf-8')
    DBpedia_JSON= DBpedia_JSON["results"]["bindings"]
    return DBpedia_JSON
    
    
def Bag_of_Words():
    
    Vocabulary = []    
    Document = Read_Wikipedia_File(1)
    
    for Data in Read_DBpedia_File(1):
        
        Vocabulary_Temp = []
        
        if 'http://dbpedia.org/property/' in Data['attribute']['value']:
            if Data['value_attribute']['type'] != u'uri':
                Attribute = ''
                for Char in Data['attribute']['value'][28:]:
                    if Char in string.uppercase:
                        Attribute = Attribute + ' ' + Char
                    else:
                        Attribute = Attribute + Char
                
                Tags = [Tag.lower().encode('utf-8') for Tag in nltk.word_tokenize(Attribute) if Tag not in string.punctuation]
                for Tag in Tags:
                    Vocabulary_Temp.append(Tag)  
                
                if Data['value_attribute']['type'] == 'literal':
                    Tags = [Tag.lower().encode('utf-8') for Tag in nltk.word_tokenize(Data['value_attribute']['value'].encode('utf-8')) if Tag not in string.punctuation]
                    for Tag in Tags:
                        Vocabulary_Temp.append(Tag)                
                else:
                    Vocabulary_Temp.append(Data['value_attribute']['value'].lower().encode('utf-8'))
        
        if Vocabulary_Temp:
            Vocabulary.append(Vocabulary_Temp)

    BOW = CountVectorizer(vocabulary = Vocabulary[0])
    Result = BOW.fit_transform(Document).toarray()
    Sum = Result.sum(axis = 1)
    print Sum
    print Vocabulary[0]
    Indices = np.where(Sum == Sum.max())[0]
    
    for Index in xrange(0, len(Indices)):
        print Document[Indices[Index]], '\n'