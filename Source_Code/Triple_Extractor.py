# -*- coding: utf-8 -*-

"""
@author: Akshay Gulati, Nitin Gupta, Shubham Sharma 
@contact: akshaygulati95600[at]gmail.com
@topic: Entity-Relation-Entity triple extraction
@description:   Python file to form various dependency sub trees for a given relation in a sentence
                and then find the value most suiatble sub tree using frequency ranking with trained 
                dependency relational data.
"""

import os
import io
from spacy.en import English
    
Path_Directory = os.path.dirname(os.path.realpath(__file__))[:-12]

if raw_input('Do you want to load english model for dependency parser?(y/n)') == 'y':
    Dep_Parser = English()
    print 'Model Loaded.'
    
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

def Searching(Output_Values, Folder_Name, Sentence_Tuples):  
      
    maximum = -999
    Output_Pattern = ''
    Output_Value = []
    for File_Name in os.listdir(Path_Directory + '/Data/Relations_Frequency/' + Folder_Name): 
        Relation_File = io.open(Path_Directory + '/Data/Relations_Frequency/' + Folder_Name + '/{}'.format(File_Name), 'r')          
        Relations_Tuple = Relation_File.read().split('\n')
        Relation_File.close()
        
        Relations_File = []
        for Relation_Tuple in Relations_Tuple:
            Relations_File.append(Relation_Tuple.split('\t'))
            
        Relations_File = Relations_File[:-1]
            
        for Pattern in Sentence_Tuples:
            for Tuple in Relations_File:
                if str(Pattern).strip() == str(Tuple[0]).strip() and str(Tuple[0]).strip().split()[0] != 'nsubj':
                    if int(Tuple[1]) >  maximum:
                        maximum = int(Tuple[1])
                        Output_Pattern = Pattern
                        Output_Value = Output_Values[Sentence_Tuples.index(Pattern)]
    
    print maximum, Output_Pattern
    return Output_Value
    
def Tree_Clusters(word, sentence):  
    
    print sentence
    temp_sentence = sentence.split(' ')
    
    if temp_sentence[0] == 'The':
        sentence = ' '.join(temp_sentence[1:])
    elif temp_sentence[0] == 'the':
        sentence = ' '.join(temp_sentence[1:])
    elif temp_sentence[0] == 'A':
        sentence = ' '.join(temp_sentence[1:])
    elif temp_sentence[0] == 'a':
        sentence = ' '.join(temp_sentence[1:])

    Value_Array = []    
    a = dep_list = Dependency_Parser(sentence)
    count =0
    array = [[0]*3]
    index = []
    done_index = []
    for i in range(len(dep_list)):
        flag = 0
        for j in range(len(dep_list)):
            if dep_list[j][1]==dep_list[i][2]:
                flag = 1
        if flag==0:
            array.append([0]*3)
            array[count][0]= i
            array[count][1] = dep_list[i][1]
            array[count][2] = dep_list[i][2]
            index.append(i)
            count+=1
    array = array[:-1]
    Output_Values =[]
    Dependency_With_Words_Array= []
    for z in range(len(array)): 
        #if index
        count = 0   # index of a
        count_children=0    # index of children array and children_dep array
        flag = 0
        children = [[] for _ in range(25)]
        children_dep = [[] for _ in range(25)]   
        count_array = []
        write = True   
        path = []
        value = ''
        original_path = []
        prev_value = ''
        
        value = array[z][1]
        path.append(a[array[z][0]][0])
        prev_value = array[z][2]
        original_path.append(array[z][2])
        done_index.append(index[z])
        while(1):  
            if(a[count][2]==value):
                if count not in done_index:
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
            Value_Array.append(array[z][2]) 
            Dependency_With_Words_Array.append(Dependency_With_Words)
    #print Dependency_With_Words_Array       
    Sentence_List = []
    for i in range(len(Dependency_With_Words_Array)):
        for j in range(len(Dependency_With_Words_Array[i])):
            if word in Dependency_With_Words_Array[i][j]:
                Output_Values.append(Value_Array[i])
                Sentence_List.append(Dependency_With_Words_Array[i][j])
    
    Output_Value = Searching(Output_Values, word, Sentence_List)
    print Output_Value

#############################################################################
Tree_Clusters('born', u'In Mumbai was born Sachin.') 