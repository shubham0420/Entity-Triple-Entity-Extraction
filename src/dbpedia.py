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
for pageNumber in range(57570, 87800,10):
    querys = '''
    
    SELECT DISTINCT ?attribute ?value_attribute ?wikilink WHERE {
    ?saket dbo:wikiPageID %s;
           ?attribute ?value_attribute.
    ?saket foaf:isPrimaryTopicOf ?wikilink.
    }
    '''
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    #sparql = SPARQLWrapper("http://10.3.1.91:8890/sparql")
    t = querys %str(pageNumber)
    sparql.setQuery(t) 
    

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    for result in results["results"]["bindings"]:
        wikilink = result["wikilink"]["value"]    

    if(len(results["results"]["bindings"]) >0):
        try:
          
            with open(os.path.join('/home/top-coder/ZIIITH_Project/attributes', str(count) + "_dbpedia.txt"),'w') as outfile:
                json.dump(results, outfile, sort_keys = True, indent=4, separators=(',', ': '))        
            print pageNumber
            wikipedia_crawler.counting(wikilink,count)
            count = count + 1
        except Exception as e:
           print "chotu"
       
    


#raw_input()







