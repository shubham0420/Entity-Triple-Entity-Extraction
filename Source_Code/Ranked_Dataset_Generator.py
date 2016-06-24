# -*- coding: utf-8 -*-

import re
import os
import io
import ast
import sys
import nltk 
import string
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

reload(sys)
sys.setdefaultencoding('utf8')
class Ranked_Dataset_Generator:
    def generating_sentence(self,category,DBpedia_File,Wikipedia_Document):
        Path = os.path.dirname(os.path.realpath(__file__))[:-3] + 'data/Film/'

        Attributes = ['director', 'language', 'country', 'starring', 'producer', 'runtime', 'cinematography', 
                      'writer', 'music', 'distributor', 'editing', 'gross', 'screenplay', 'budget']

        Aliases_List = [['director', 'directed by', 'film director', 'movie director'],
                        ['written in'],
                        ['shot at', 'shot in'],
                        ['film starring', 'actor', 'actress', 'starring', 'cast', 'in lead', 'film stars', 'movie stars', 'stars'],
                        ['producer', 'produced by', 'producer of'],
                        ['run time', 'runtime'],
                        ['cinematographer', 'cinematographery'],
                        ['writer', 'written by'],
                        ['music', 'composed', 'composer', 'music director'],
                        ['distributor', 'distributed by', 'is distributed', 'distributed'],
                        ['editing', 'editor', 'edited by', 'edited'],
                        ['grossed', 'collected', 'collection', 'grosser', 'box-office', 'box office', 'worldwide'],
                        ['screenplay'],
                        ['total budget', 'costed a total of', 'costed a sum of', 'budget']]

        Index_Max = 10000
                      
        for Index in xrange(0, Index_Max,Wiki_Document):
            DBpedia_JSON = DBpedia_File.read().split('}},')[:-1]
            DBpedia_JSON = [(JSON + u'}}') for JSON in DBpedia_JSON]
            for Data in DBpedia_JSON:
                Data = ast.literal_eval(Data)
                if u'http://dbpedia.org/property/' in Data['attribute']['value']:
                    Attribute = Data['attribute']['value'][28:].lower()
                    if Attribute in Attributes:
                        Values = Data['value_attribute']['value'].lower()
                        try:
                            Values = Values[:Values.index('_(')]
                        except:
                            pass
                        #Sentence = re.findall('http[s]? : //(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', Values)
                        Flag = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', Values)                    
                        if Flag:
                            Values = Values[-1*Values[::-1].index('/'):]
                            Values = Values.split('_')
                        else:
                            Values = Values.split('\n')
                            Values_Temp = []
                            for Value in Values:
                                VAlues = nltk.word_tokenize(re.sub('\*','',Value))
                                for VAlue in VAlues:
                                    if VAlue not in string.punctuation:
                                        Values_Temp.append(VAlue)

                        Values = set(Values_Temp)
                        if len(Values) > 0:
                            #BOW = CountVectorizer(vocabulary = Aliases_List[Attributes.index(Attribute)], ngram_range = (1,2))
                            BOW = CountVectorizer(vocabulary = Values, ngram_range = (1,4))
                            Result = BOW.fit_transform(Wikipedia_Document).toarray()
                            Sum = Result.sum(axis = 1)
                            try:
                                if Sum.max() > 0:
                                    Sum = np.where(Sum==Sum.max())[0]
                                    for INdex in Sum:
                                        #Sentences = [Sentence for Sentence in Sentences for Value in Values if Value in Sentence]
                                        # Check for values
                                        Attributes_File = io.open(os.path.dirname(os.path.realpath(__file__))[:-3] + 'data/'+category+'/' '{}'.format(Attribute), 'a', encoding = 'utf8')
                                        Attributes_File.write(unicode(Wikipedia_Document[INdex]))
                                        Attributes_File.write(u'\n')
                                        Attributes_File.close()
                            except:
                                pass
