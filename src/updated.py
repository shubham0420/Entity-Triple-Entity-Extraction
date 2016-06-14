# -*- coding: utf-8 -*-
from SPARQLWrapper import SPARQLWrapper, JSON
from pprint import pprint  
import urllib2
import wikipedia_crawler 
import os.path
import json
############ This file is extracting all the attributes of dbpedia page and storing them in attributes folder in attribute folder
# -*- coding: utf 8
from SPARQLWrapper import SPARQLWrapper , JSON
import os.path
import json
from pprint import pprint
count = 0

query = '''
    
    SELECT DISTINCT ?value_attribute ?wikilink ?wikiid WHERE {
    ?player a <http://dbpedia.org/ontology/Cricketer>.
    ?player foaf:isPrimaryTopicOf ?wikilink.
    ?player dbo:wikiPageID ?wikiid.
    }
    '''

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery(query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

wikilink = []
for result in results["results"]["bindings"]:
	  wikilink.append(result["wikilink"]["value"])    

wikiid = []
for result in results["results"]["bindings"]:
	  wikiid.append(result["wikiid"]["value"])   
print wikiid

count = 0
pageNumber = 0
while (count < len(wikiid)):
    query1 = '''
    
    SELECT DISTINCT ?value_attribute ?wikilink ?wikiid WHERE {
    ?player a <http://dbpedia.org/ontology/Cricketer>.
    ?player foaf:isPrimaryTopicOf ?wikilink.
    ?player dbo:wikiPageID ?wikiid.
    }
    '''

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    if(len(results["results"]["bindings"]) >0):
            try:              
                with open(os.path.join('/home/top-coder/ZIIITH_Project/attributes', str(pageNumber) + "_dbpedia.txt"),'w') as outfile:
                    json.dump(results, outfile, sort_keys = True, indent=4, separators=(',', ': '))        
                print pageNumber
                wikipedia_crawler.counting(wikilink,count)
                pageNumber = pageNumber + 1
            except Exception as e:
               print "chotu"
           

