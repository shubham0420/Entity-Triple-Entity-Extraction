# -*- coding: utf-8 -*-
from SPARQLWrapper import SPARQLWrapper, JSON
from pprint import pprint  
import urllib2
import wikipedia_crawler 
import os.path
import json

count = 0
def Sparql_commands(query):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")   
    sparql.setQuery(query) 
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results
    
query_new = """
SELECT DISTINCT ?wikiid  WHERE {
?player a <http://dbpedia.org/ontology/Artist>.
?player dbo:wikiPageID ?wikiid.
}"""

results1 =  Sparql_commands(query_new)
wikiid = []
for result in results1["results"]["bindings"]:
	  wikiid.append(result["wikiid"]["value"])    



for ID in wikiid:   
        print 'valar dohaeris' + ' ' + str(a)
        querys = '''    
        SELECT DISTINCT ?attribute ?value_attribute ?wikilink WHERE {
        ?saket dbo:wikiPageID %s;
               ?attribute ?value_attribute.
        ?saket foaf:isPrimaryTopicOf ?wikilink.
        }
        '''
        t = querys % ID
        results2 =  Sparql_commands(t)
        #pprint(results)
        wikilink=[]
        for result in results2["results"]["bindings"]:
            wikilink = result["wikilink"]["value"]    
     
	    #print wikilink
        if(len(results2["results"]["bindings"]) >0):
                try:
                    flaging = wikipedia_crawler.counting(wikilink,count)       
                    if(flaging == 1):       
                        with open(os.path.join('/home/top-coder/ZIIITH_Project/attributes/Untitled_Folder', str(count) + "_dbpedia.txt"),'w') as outfile:
                            json.dump(results2, outfile, sort_keys = True, indent=4, separators=(',', ': '))        
                        
                        count = count + 1
                except Exception as e:
                   print e
               
      

  







