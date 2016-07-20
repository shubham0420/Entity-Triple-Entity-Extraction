# -*- coding: utf-8 -*-

"""
@author: Akshay Gulati, Nitin Gupta, Shubham Sharma 
@contact: 
@topic: Entity-Relation-Entity triple extraction
@description:   Python file collect and train Triple_Extractor for any DBpedia ontology class. Training includes,
                > Collecting sub classes
                > Saving Wiki_IDs for all pages in all sub classes of main class
                > Accesing Wikipedia pages of all these Wiki_IDs (Generally in order of millions)
                > Normalizing all the Wikipedia data.
                > Saving relevant sentences from these Wikipedia pages based on DBpedia values.
                > Finding dependency tree outputs of all these sentences
                > Ranking all sentences per attribute using dependency tree outputs
                > Saving dependency sub tress along with their frequencies for each attribute
                
                Common Usage:
                
                import Train
                
                T = Train.Train_Ontology_Class('Person')    #Should be extact name as mentioned on DBpedia Ontology Map
                T.Save_Wiki_IDs()                           # Saves Wiki_ID's for all pages in a class
                T.Save_Wikipedia_DBpedia_Data()             # Saves all relevant sentences for each popular attribute in a class 
                                                            # using DBpedia values of these attributes and filtering by [1,4] ngram Bag-of-Words.
                T.Save_Value_Replaced_Data()                # Replacing 'abrakadbra' with all the values in the above sentences
                T.Save_Relation_Dependency_Data()           # Saving all possible sub dependency trees per attribute for all above sentences
                T.Save_Relation_Frequency_Data()            # Finding frequency of dependency sub trees for each attribute and saving them
                T.Save_Ranked_Sentences()                   # Saving sentences in ranked order for each attribute
"""

import io
import os
import re
import ast
import sys
import nltk
import shutil
import string
import os.path
import operator
import subprocess
import numpy as np

import Wikipedia_Crawler 

from spacy.en import English
from collections import Counter
from SPARQLWrapper import SPARQLWrapper, JSON  
from Integer_Combination import Handling_Integer_Values   
from sklearn.feature_extraction.text import CountVectorizer

reload(sys)
sys.setdefaultencoding('utf8')

Path_Directory = os.path.dirname(os.path.realpath(__file__))[:-12]
Stopwords = nltk.corpus.stopwords.words('english')

if raw_input('Do you want to load english model for dependency parser?'):
    Dep_Parser = English()
    print 'Model Loaded.'

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

def Terminal_Run(StrCmd):
    Command = subprocess.Popen(StrCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    Output = ''
    for Line in Command.stdout.readlines():
        Output += Line
    return Output
    
def Create_Folder(Path, Flag_Remove = True):
    
    if os.path.exists(Path):
        if Flag_Remove:
            shutil.rmtree(Path)
            os.makedirs(Path)
            print 'Directory: \'{}\' created.'
            return True

        else:
            print 'Directory: \'{}\' already exists.'
            return True
    
    else:
        os.makedirs(Path)
        print 'Directory: \'{}\' created.'
        return True
    
    return False

def Dependency_Parser(Sentence):

    try:
        Dep_Parser_Output = Dep_Parser(Sentence)
        Dep_Parser_Tags = []
        
        for Token in Dep_Parser_Output:
            Dep, Head, Orth = Token.dep_, Token.head.orth_, Token.orth_
            if Dep == u'ROOT':
                Dep = u'root'
                Head = u'ROOT'
                
            Dep_Parser_Tags.append([Dep, Head, Orth])
        return Dep_Parser_Tags 
    
    except Exception as e :
        print e
        return False

def SPARQL_Commands(Query):
    
    try:
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")   
        sparql.setQuery(Query) 
        sparql.setReturnFormat(JSON)
        Results = sparql.query().convert()
        return Results

    except:
        return False

class Train_Ontology_Class():
    
    def __init__(self, Class, Allowed_Attributes = None, Blocked_Attributes = None):
        
        self.Class = Class
        self.Blocked_Attributes = Blocked_Attributes
        self.Allowed_Attributes = Allowed_Attributes
        
    def Save_Wiki_IDs(self):
        
        if Create_Folder(Path_Directory + '/Data/Wiki_IDs/', Flag_Remove = False):

            Sub_Classes = []
            Wiki_IDs_File = io.open(Path_Directory + '/Data/Wiki_IDs/{}'.format(self.Class), 'w', encoding = 'utf8')
        
            Results_Sub_Classes = SPARQL_Commands(Query_Subclasses % self.Class)
            if Results_Sub_Classes:   
                for Result in Results_Sub_Classes["results"]["bindings"]:
                    Sub_Classes.append(Result["x"]["value"])
                        
            print 'Accessed Class: {}'.format(self.Class)
            print 'No. of Sub Classes: {}'.format(len(Sub_Classes))
            
            for Subclass in Sub_Classes:
                print Subclass
                Results_Wiki_ID =  SPARQL_Commands(Query_Wiki_ID % '<{}>'.format(Subclass))
                if Results_Wiki_ID:
                    for Result in Results_Wiki_ID["results"]["bindings"]:
                        Wiki_IDs_File.write(unicode(Result["wikiid"]["value"]))
                        Wiki_IDs_File.write(u'\n')
           
            Wiki_IDs_File.close()
    
    def Save_Wikipedia_DBpedia_Data(self):
        
        if Create_Folder(Path_Directory + '/Data/Attributes/', Flag_Remove = False):
            Create_Folder(Path_Directory + '/Data/Attributes/{}/'.format(self.Class) , Flag_Remove = True)
            Track = 0
        
            try:
                Wiki_IDs_File = io.open(Path_Directory + '/Data/Wiki_IDs/{}'.format(self.Class), 'r', encoding = 'utf8')
                Wiki_IDs = Wiki_IDs_File.read().split('\n')[:-1]
                Wiki_IDs_Count = len(Wiki_IDs)
                print 'Read Wiki_IDs file for class: {}'.format(self.Class)
                for Wiki_ID in Wiki_IDs:   
                    print 'Done {0} of {1} of Class {2}, Currently on Wiki_ID: {3}'.format(Track, Wiki_IDs_Count, self.Class, Wiki_ID)
                    Results_JSON =  SPARQL_Commands(Query_JSON % Wiki_ID)
                    if Results_JSON:
                        if(len(Results_JSON["results"]["bindings"]) > 0):
                            Results_JSON = Results_JSON["results"]["bindings"]
                            Wiki_Link = Results_JSON[0]["wikilink"]["value"]  
                            try:
                                Wiki_Doc = Wikipedia_Crawler.URL_to_Wikipedia(Wiki_Link) 
                                Wiki_Doc.Access_Wikipedia()           
                                Wiki_Doc.HTML_to_Data()
                            
                            except:
                                pass
                            
                            else:
                                if(Wiki_Doc.Document):       
                                    Wikipedia_Document = Wiki_Doc.Document
                                        
                                for Result in Results_JSON:
                                    if u'http://dbpedia.org/property/' in Result['attribute']['value']:
                                        Attribute = Result['attribute']['value'][28:]
                                        Flag_Pass = False
                                        
                                        if self.Blocked_Attributes:
                                            if Attribute not in self.Blocked_Attributes and '/' not in Attribute:
                                                Flag_Pass = True 
                                        
                                        if self.Allowed_Attributes:
                                            if Attribute in self.Blocked_Attributes and '/' not in Attribute:
                                                Flag_Pass = True
                                                
                                        if Flag_Pass:                                               
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
                                                        if VAlue not in string.punctuation and VAlue not in Stopwords and len(VAlue) > 2:
                                                            Values_Temp.append(VAlue)
                                                
                                                for Count in xrange(0, len(Values_Temp)):
                                                    Integer_Combination = Handling_Integer_Values()
                                                    Integer_Combination.Main_Function(Values_Temp[Count].encode('utf-8'))
                                                    for Combination in Integer_Combination.Combination:
                                                        Values_Temp.append(Combination)
                                                 
                                                Values_Temp = set(Values_Temp)
                                                Values = [Value for Value in Values_Temp]
                                                if len(Values) > 0:
                                                    BOW = CountVectorizer(vocabulary = Values, max_df = 0.666, stop_words = 'english', ngram_range = (1,4))
                                                    Result = BOW.fit_transform(Wikipedia_Document).toarray()
                                                    Sum = Result.sum(axis = 1)
                                                    if Sum.max() > 0:
                                                        Sum = np.where(Sum==Sum.max())[0]
                                                        for Index in Sum:                                                                                               
                                                            Attributes_File = io.open(Path_Directory + '/Data/Attributes/{0}/{1}'.format(self.Class, Attribute), 'a', encoding = 'utf8')
                                                            Attributes_File.write(unicode(Wikipedia_Document[Index]))
                                                            Attributes_File.write(u'\n')
                                                            Attributes_File.write(unicode(Values))
                                                            Attributes_File.write(u'\n')
                                                            Attributes_File.close() 
                    Track += 1
                                     
            except Exception as err:
                print err
                pass
        
        def Save_Value_Replaced_Data(self):
            
            if Create_Folder(Path_Directory + '/Data/Attributes_Value/', Flag_Remove = False):
                
                Create_Folder(Path_Directory + '/Data/Attributes_Value/{}/'.format(self.Class) , Flag_Remove = True)
                Attributes_File_List = os.listdir(Path_Directory + '/Data/Attributes/{}/'.format(self.Class))
                for Attribute in Attributes_File_List:
                    
                    Attribute_File = io.open(Path_Directory + '/Data/Attributes/{0}/{1}'.format(self.Class, Attribute), 'r', encoding = 'utf8' )
                    Attribute_Value_File = io.open(Path_Directory + '/Data/Attributes_Value/{0}/{1}'.format(self.Class, Attribute), 'w', encoding = 'utf8' )
                    Data = Attribute_File.read().split('\n')
                    Data = Data[:(len(Data) - len(Data)%2)]
                    for Index in xrange(0, len(Data), 2):
                        if '[' not in Data[Index] and ']' not in Data[Index]:        
                            if Data[Index + 1][0] == '[' and Data[Index + 1][-1] == ']':
                                Sentence = Data[Index]
                                Values = ast.literal_eval(Data[Index + 1])
                                
                                for Value in Values:
                                    
                                    if type(Value) == int:
                                        Value = str(Value)
                                    try:
                                        Sentence = re.sub(r'\b{}\b'.format(Value.lower()),'abrakadabra', Sentence.lower())
                                        Sentence = Sentence.replace('abrakadabra abrakadabra abrakadabra abrakadabra','abrakadabra')
                                        Sentence = Sentence.replace('abrakadabra abrakadabra abrakadabra','abrakadabra')
                                        Sentence = Sentence.replace('abrakadabra abrakadabra', 'abrakadabra')
                                        Attribute_Value_File.write(Sentence)
                                        Attribute_Value_File.write(u'\n')
                    
                                    except:
                                        pass
                                    
                    Attribute_File.close()
                    Attribute_Value_File.close()
            
            def Save_Relation_Dependency_Data(self):
                
                if Create_Folder(Path_Directory + '/Data/Attributes_Dependencies', Flag_Remove = False):
                    if Create_Folder(Path_Directory + '/Data/Atrributes_Dependencies_Sentences', Flag_Remove = False):
                        
                        Attribute_Files_List = os.listdir(Path_Directory +'/Data/Attributes_Value/{}/'.format(self.Class))
                        No_of_Attribute_Files = len(Attribute_Files_List)
                        Index = 0
                        
                        for File_Name in Attribute_Files_List: 
                            Index += 1
                            Input_File = io.open(Path_Directory + '/Data/Attributes_Value/{0}/{1}'.format(self.Class, File_Name), 'r', encoding = 'utf8')
                            Input_Sentences = Input_File.read().split('\n')
                            Input_File.close()
                            Input_Sentences = set(Input_Sentences)
                            Input_Sentences = [Sentence for Sentence in Input_Sentences] 
                            print 'Doing {0}, Total {3} sentences: {1} out of {2} Attributes'.format(File_Name, Index, No_of_Attribute_Files, len(Input_Sentences))
                            for Sentence in Input_Sentences: 
                                try:
                                    if(len(Sentence)>1): 
                                        Sentence = Sentence.strip()
                                        if Sentence[-1] == '.':
                                            Sentence = Sentence[:-1]
                                        Dep_Parser_Output = Dependency_Parser(Sentence)
                                        if Dep_Parser_Output:
                                            a = Dep_Parser_Output
                                            path = []
                                            value = ''
                                            original_path = []
                                            prev_value = ''
                                            for i in range(len(a)):
                                                if(a[i][2]=='abrakadabra'):
                                                    value = a[i][1]          
                                                    path.append(a[i][0])
                                                    prev_value = a[i][2]
                                                    original_path.append(a[i][2])
                                                    break
                                            if value:    
                                                count = 0   
                                                count_children = 0
                                                flag = 0
                                                empty_length = 0
                                                children = [[] for _ in range(25)]
                                                children_dep = [[] for _ in range(25)]   
                                                count_array = []
                                                write = True      
                                                #print sentence
                                                while(1):  
                                                    if(a[count][2]==value):
                                                        if count in count_array:
                                                            write = False
                                                            break
                                                        count_array.append(count)
                                                        path.append(a[count][0])
                                                        original_path.append(a[count][2])
                                                        for j in range(len(a)):
                                                            if (a[j][1] == value):
                                                                if(a[j][2]!= prev_value):
                                                                    children[count_children].append(a[j][2])
                                                                    children_dep[count_children].append(a[j][0])
                                                        count_children +=1
                                                        prev_value = value
                                                        value = a[count][1]
                                                        count = 0
                                                    else:
                                                        count +=1
                                                    if(value=='ROOT'):
                                                        break
                                                    
                                                if write:
                                                    Dependency_Without_Words =[]
                                                    string = ''
                                                    for i in range(len(path)):
                                                        string =string + ' '+path[i]
                                                        for j in range(len(children_dep[i])):         
                                                             Dependency_Without_Words.append(string +' '+children_dep[i][j])
                                                 
                                                    Dependency_With_Words = [] 
                                                    
                                                    string = ''
                                                    for i in range(len(path)-1):
                                                        string =string + ' '+path[i]
                                                        for j in range(len(children_dep[i])):
                                                            Dependency_With_Words.append(string +' '+original_path[i+1] +' '+children_dep[i][j])
                                                                            
                                                    output_file = open(os.path.join(Path_Directory + '/Data/Attributes_Dependencies/' + File_Name),'a')
                                                    for Patterns in Dependency_With_Words:
                                                        output_file.write(Patterns)
                                                        output_file.write('\t')
                                                    output_file.write('\n')
                                                    output_file.close()     
                                                    
                                                    output_file = open(os.path.join(Path_Directory+'/Data/Atrributes_Dependencies_Sentences/'+ File_Name),'a')           
                                                    output_file.write(Sentence)
                                                    output_file.write('\n')
                                                    output_file.close()  
                                except:
                                    print 'Unkown error.'
                                    pass
            
            def Save_Relation_Frequency_Data(self):
                
                if Create_Folder(Path_Directory + '/Data/Relations_Frequency/', Flag_Remove = False):
                    Attributes = os.listdir(Path_Directory + '/Data/Attributes_Dependencies/')
    
                    Index = 0
                    
                    for Attribute in Attributes:
                        if os.path.exists(Path_Directory + '/Data/Relations_Frequency/' + Attribute) == False:
                            print Index, Attribute
                            Index += 1
                            
                            Attrbute_File = io.open(Path_Directory + '/Data/Attributes_Dependencies/' + Attribute, 'r', encoding = 'utf8')
                            Attribute_Tuples_Data = Attrbute_File.read().split('\n')[:-1]
                            Attrbute_File.close()
                            
                            Attribute_Tuples = []
                            
                            for Attribute_Line in Attribute_Tuples_Data:
                                Attribute_Line = Attribute_Line.split('\t')
                                for Attribute_Tuple in Attribute_Line:
                                    Attribute_Tuple = Attribute_Tuple.strip()
                                    if Attribute_Tuple != '':
                                        Attribute_Tuples.append(Attribute_Tuple)
                                                
                            Sorted_Attribute_Data = sorted(Counter(Attribute_Tuples).items(),key = operator.itemgetter(1),reverse = True)
                        
                            for Attribute_Tuple in Sorted_Attribute_Data:
                                Attribute_Tuple_List = Attribute_Tuple[0].split()
                                if Attribute_Tuple_List[-2] not in string.punctuation:
                                    if Attribute_Tuple_List[-2] not in Stopwords:
                                        try:
                                            if os.path.exists(Path_Directory + '/Data/Relations_Frequency/' + Attribute_Tuple_List[-2]) == False:
                                                os.makedirs(Path_Directory + '/Data/Relations_Frequency/' + Attribute_Tuple_List[-2])
                                            
                                            Tuple_File = io.open(Path_Directory + '/Data/Relations_Frequency/{0}/{1}'.format(Attribute_Tuple_List[-2], Attribute), 'a', encoding = 'utf8')
                                            Tuple_File.write(Attribute_Tuple[0])
                                            Tuple_File.write(u'\t')
                                            Tuple_File.write(unicode(Attribute_Tuple[1]))
                                            Tuple_File.write(u'\n')
                                            Tuple_File.close()
                                            
                                        except:
                                            pass
                
                def Save_Ranked_Sentences(self):
                    
                    Create_Folder(Path_Directory+'/Data/Ranked_Value_Sentences/', Flag_Remove = False)
                    
                    list_of_files = os.listdir(Path_Directory+'/Data/Attributes_Dependencies/')
                    index = 0
                    for filename in list_of_files:
                        print index , len(list_of_files)
                        index += 1
                        
                        list_of_dictionary =[]
                        #print 'shubham'
                        if filename[-1]!= '~':
                            input_file = open(os.path.join(Path_Directory+'/Data/Attributes_Dependencies/'+filename),'r')            
                            #output_file = open(os.path.join('/home/top-coder/Triple_Extractor/Data/output1'+filename),'a')
                            input_file = input_file.read()
                            input_file = input_file.split('\n')
                            
                            input_file_sentences = open(os.path.join(Path_Directory+'/Data/Atrributes_Dependencies_Sentences/'+filename),'r')           
                            input_file_sentences = input_file_sentences.read()
                            final = []
                            for sentences in input_file:
                                final.append(sentences.split('\t'))
                            sentences_array = input_file_sentences.split('\n')
                            #print sentences_array
                            dictionary = {}
                            count = 0
                            #print final
                            for sentences in final:
                                for patterns in sentences:
                                    if patterns in dictionary:
                                        
                                        if sentences_array[count] not in dictionary[patterns]:
                                            dictionary[patterns][0] +=1                    
                                            dictionary[patterns].append(sentences_array[count])
                                    else:
                                        dictionary[patterns] = [1]
                                        dictionary[patterns].append(sentences_array[count])
                                count +=1
                         
                            sorted_x = sorted(dictionary.items(),key = operator.itemgetter(1),reverse = True)            
                            list_of_dictionary.append(sorted_x)
                            #print list_of_dictionary
                            #raw_input()
                            for Tuple in list_of_dictionary[0]:
                                if Tuple[0]!='':
                                    for index in xrange(1,len(Tuple[1])):
                                        with open(Path_Directory+'/Data/Ranked_Value_Sentences/'+filename,'a')as output_file:
                                            output_file.write(Tuple[1][index])
                                            output_file.write('\n')       