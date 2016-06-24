# -*- coding: utf-8 -*-
from SPARQLWrapper import SPARQLWrapper, JSON  
import Wikipedia_Crawler 
import os.path
import io
import os
import shutil
import sys
import numpy as np
import nltk
import re
import string
from sklearn.feature_extraction.text import CountVectorizer

reload(sys)
sys.setdefaultencoding('utf8')

def SPARQL_Commands(query):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")   
    sparql.setQuery(query) 
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def Create_Folder(Path):
    
    if os.path.exists(Path):
        shutil.rmtree(Path)
    
    os.makedirs(Path)
    return True

Path_Directory = os.path.dirname(os.path.realpath(__file__))[:-12]

Classes = ['Organisation','Person','ArchitecturalStructure','CelestialBody','SocietalEvent','NaturalPlace','PopulatedPlace','Eukaryote','Genre','MusicalWork', 'WrittenWork']
Blocked_Attributes = []

Query_Subclasses = """
SELECT ?x

WHERE
  {
    {
      SELECT *
      WHERE
        {
          ?x rdfs:subClassOf ?y .
        }
    }  OPTION (transitive, t_distinct, t_in (?x), t_out (?y) ).
  FILTER (?y = <http://dbpedia.org/ontology/%s>)

}
"""

Query_Wiki_ID = """
SELECT DISTINCT ?wikiid  WHERE {
?player a %s.
?player dbo:wikiPageID ?wikiid.
}"""

Query_JSON = '''    
SELECT DISTINCT ?attribute ?value_attribute ?wikilink WHERE {
?saket dbo:wikiPageID %s;
       ?attribute ?value_attribute.
?saket foaf:isPrimaryTopicOf ?wikilink.
}
'''

for Class in Classes:
    
    Create_Folder(Path_Directory + '/Data/Wiki_IDs/{}/'.format(Class))
    
    Subclasses = []
    Results_Subclasses = SPARQL_Commands(Query_Subclasses % Class)
    for Result in Results_Subclasses["results"]["bindings"]:
	      Subclasses.append(Result["x"]["value"])  
    print 'Accessed Class: {}'.format(Class)
    print 'No. of Sub Classes: {}'.format(len(Subclasses))

    Wiki_IDs = []
    for Subclass in Subclasses:
        
        print Subclass
        Results_Wiki_ID =  SPARQL_Commands(Query_Wiki_ID % '<{}>'.format(Subclass))
        for Result in Results_Wiki_ID["results"]["bindings"]:
            Wiki_IDs.append(Result["wikiid"]["value"])
            
        set(Wiki_IDs)
        
    for Wiki_ID in Wiki_IDs:   
        print Wiki_ID
        Results_JSON =  SPARQL_Commands(Query_JSON % Wiki_ID)
        if(len(Results_JSON["results"]["bindings"]) >0):
            Results_JSON = Results_JSON["results"]["bindings"]
            Wiki_Link = Results_JSON[0]["wikilink"]["value"]  
            try:
                Wiki_Doc = Wikipedia_Crawler.URL_to_Wikipedia(Wiki_Link) 
                Wiki_Doc.Access_Wikipedia()           
                Wiki_Doc.HTML_to_Data()

                if(Wiki_Doc.Document):       
                    Wikipedia_Document = Wiki_Doc.Document
            except:
                pass
            
            else:
                    
                for Result in Results_JSON:
                    if u'http://dbpedia.org/property/' in Result['attribute']['value']:
                        Attribute = Result['attribute']['value'][28:].lower()
                        
                        if Attribute not in Blocked_Attributes:
                            Values = Result['value_attribute']['value'].lower()
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
                                BOW = CountVectorizer(vocabulary = Values)
                                Result = BOW.fit_transform(Wikipedia_Document).toarray()
                                Sum = Result.sum(axis = 1)
                                try:
                                    if Sum.max() > 0:
                                        Sum = np.where(Sum==Sum.max())[0]
                                        for Index in Sum:
                                            Attributes_File = io.open(Path_Directory + '/Data/Attributes/{}'.format(Attribute), 'a', encoding = 'utf8')
                                            Attributes_File.write(unicode(Wikipedia_Document[Index]))
                                            Attributes_File.write(u'\n')
                                            Attributes_File.close()
                                                
                                except:
                                    pass