# -*- coding: utf-8 -*-
"""
Created on Tue May 31 20:51:39 2016

@author: akshay
@contact: akshaygulati95600[at]gmail.com
@topic: Entity-Relation-Entity triple
"""
from bs4 import BeautifulSoup
from pprint import pprint
import urllib

class DBpedia_to_Attributes():

    def __init__(self, DBpedia_URL):
        self.DBpedia_URL = DBpedia_URL
        self.Attributes = []
    
    def Get_Attributes(self):
        HTML = urllib.urlopen(self.DBpedia_URL).read()
        Soup = BeautifulSoup(HTML)
        Search_Results = Soup.find_all('a', attrs = {'class':'uri'})
        pprint (Search_Results)
        
D = DBpedia_to_Attributes('http://dbpedia.org/page/Sachin_Tendulkar')
D.Get_Attributes()
