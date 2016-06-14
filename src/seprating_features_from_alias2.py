# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 23:23:14 2016

@author: top-coder
"""

import io
import sys
import ast

reload(sys)
sys.setdefaultencoding("utf8")

Aliases_File = io.open('/home/top-coder/ZIIITH_Project/Aliases_File/Aliases_File', 'r', encoding = 'utf8')
Aliases_List = Aliases_File.read()
Aliases_List = Aliases_List.split('\n')
Aliases_File.close()

count = 0
array=[]

for Alias in Aliases_List:
    if len(Alias.split('\t')) == 3:
        array1 = []
        array1.append(Alias.split('\t')[0])
        #print Alias.split('\t')[1]
        [array1.append(i) for i in ast.literal_eval(Alias.split('\t')[2])]
        array.append(array1)

wiki_file = io.open('/home/top-coder/ZIIITH_Project/cricket_wikipedia/final_file.txt', 'r', encoding = 'utf8')
wiki_list = wiki_file.read()
wiki_sentence_array = wiki_list.split('\n')
ans = []
#print wiki_list
'''
it will take more time
[ans.append(sentence) for i in array for synonym in i for sentence in \
wiki_sentence_array if synonym.encode('ascii') in sentence]

Feeling Happy after decreasing time by a lot amount
'''

array_of_dictionary = []
temp_word_array = []

''' 
    Below for loop wil give us array_of_dictionary.
    First we will split the sentence into words and then store the words in 
    those sentences in dictionary.
    array_of_dictionary contains all the sentences stored in dictionary format.
'''

for sentence in wiki_sentence_array:
    temp_word_array = sentence.split(' ')
    temp_dictionary = {}
    for word in temp_word_array:
        temp_dictionary[word] = word
    array_of_dictionary.append(temp_dictionary)

'''
    We are now going to search the words stored in array
    in the array_of_dictionary.
    This function searches for word in a sentence if that word is found then 
    the sentence is added.
    Cons: Same sentence may be added multiple time.
'''
final_sentence_array = []
print len(array_of_dictionary)
#print array
for sub_array in array:
    flag = 0
    word1 = None
    for word in sub_array:
        for index in range(len(array_of_dictionary)):
            try:
                array_of_dictionary[index][word]
                final_sentence_array.append(' '.join(array_of_dictionary[index]))
                if not word1:
                    word1 = word
                flag = 1
            except:
                my_word = 'as'
    if flag == 1:
        output_file = open(word1,'w')
        for sentence in final_sentence_array:
            output_file.write(sentence)
            output_file.write('\n')
        output_file.close()           

#print array_of_dictionary[0]['Shakoor']
#print final_sentence_array

