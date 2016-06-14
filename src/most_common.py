# -*- coding: utf 8
import json 
from pprint import pprint
import os.path
import glob
import nltk
from nltk import FreqDist
'''import sys
sys.setdefaultencoding("utf-8")'''

read_files = glob.glob("/home/nitin/Desktop/attrib/*.json")
i=0;
total= len(glob.glob("/home/nitin/Desktop/attrib/*.json"))
l =  [[] for _ in range(total)]

for File in read_files:
	
	json_data=open(File).read()
	d = json.loads(json_data)
	data= d["results"]["bindings"]
	
	print i

	count = 0
	key=[]
	for Dict in data:
		b = []

		if u'http://dbpedia.org/property/' in Dict['attribute']['value']:
			key.append(str(data[count]["attribute"]["value"][28:].encode('utf-8')))	
		count +=1
		#b= [key,key_type,value,value_type]
	


	#print key
	l[i].append(set(key))
	i+=1
	#print '\n'
attrib = []
#print l[:20]
for a in l[:20]:
	for j in a:
		attrib+= j
		#print attrib
#print type(attrib)
freq= FreqDist(attrib)
print freq.most_common()
