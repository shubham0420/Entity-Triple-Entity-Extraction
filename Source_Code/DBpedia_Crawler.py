# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 14:36:02 2016

@author: Akshay Gulati, Nitin Gupta, Shubham Sharma 
@contact: 
@topic: Entity-Relation-Entity triple extraction
@description: 
"""

from SPARQLWrapper import SPARQLWrapper, JSON

def SPARQL_Run(Query):
    SPARQL = SPARQLWrapper("http://dbpedia.org/sparql")   
    SPARQL.setQuery(Query) 
    SPARQL.setReturnFormat(JSON)
    return SPARQL.query().convert()

class Class_to_RDF():
    
    def __init__(self, Class):
        
        self.Query_WikiID = '''
        SELECT DISTINCT ?wikiid  WHERE {
        ?player a <http://dbpedia.org/ontology/%s>.
        ?player dbo:wikiPageID ?wikiid.
        }'''%str(Class)
        
        self.Query_RDF = '''    
        SELECT DISTINCT ?attribute ?value_attribute ?wikilink WHERE {
        ?saket dbo:wikiPageID %s;
               ?attribute ?value_attribute.
        ?saket foaf:isPrimaryTopicOf ?wikilink.
        }
        '''
            
        self.WikiIDs = []
        self.RDF_JSONs = []
        self.Wikipedia_URLs = []
        
    def Access_WikiIDs(self):

        for WikiID in SPARQL_Run(self.Query_WikiID)['results']['bindings']:
            self.WikiIDs.append(WikiID['wikiid']['value'])    
    
    def Access_DBpedia(self):
        
        for WikiID in self.WikiIDs:   
            print WikiID
            Query = self.Query_RDF % WikiID
            RDF_JSON =  SPARQL_Run(Query)['results']['bindings']
            if len(RDF_JSON) > 0:
                self.Wikipedia_URLs.append(RDF_JSON['wikilink']['value'])   
                self.RDF_JSONs.append(RDF_JSON)