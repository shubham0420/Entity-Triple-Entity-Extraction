# -*- coding: utf-8 -*-

from SPARQLWrapper import SPARQLWrapper, JSON

import io
import os
import shutil

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
        Wiki_IDs_File = io.open(Path_Directory + '/Data/Wiki_IDs/{0}/{1}'.format(Class, Subclass[28:]), 'w', encoding = 'utf8')
        Wiki_IDs_File.write(unicode(Wiki_IDs))
        Wiki_IDs_File.close()