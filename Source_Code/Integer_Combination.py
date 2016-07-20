# -*- coding: utf-8 -*-

"""
@author: Akshay Gulati, Nitin Gupta, Shubham Sharma 
@contact: akshaygulati95600[at]gmail.com
@topic: Entity-Relation-Entity triple extraction
@description: 	Python file for converting numeric quantities such as dates, numbers, currency etc in common natural language 	
				utterances. For ex, 1900000 is commonly represented as 1,900,000 or 1.9 million in Wikipedia Documents.
				Common Usage:

				import Integer_Combination

				I = Integer_Combination.Handling_Integer_Values()
				I.Main_Function(1900000)
				print I.Combination

				I.Main_Function('1995-02-07')
				print I.Combination
"""

import re
import inflect
import locale

class Handling_Integer_Values:

    def __init__(self):
        self.Month_Dict= {'01':'January',"02":'February',"03":'March','04':'April','05':'May','06':'June','07':'July','08':'August','09':'September','10':'October','11':'November','12':'December '}
        self.month = None
        self.date = None
        self.year = None
        self.Number = None
        self.Inflect = inflect.engine()
        self.Combination = []
                                           
    def Converting_Date_Format1(self,Date):
            if int(Date[0][2]) < 10:
                self.date = Date[0][2][1]
                self.month = self.Month_Dict[Date[0][1]]
                self.year = Date[0][0]
            else:
                self.date = Date[0][2]
                self.month = self.Month_Dict[Date[0][1]]
                self.year = Date[0][0]                
	

    def Converting_Date_Format2(self,Date):
	         
            if int(Date[0][1])<10:
                 self.date = Date[0][1][1]
                 self.month = self.Month_Dict[Date[0][0]]
            else:
                self.date = Date[0][1]
                self.month = self.Month_Dict[Date[0][0]]
     

    def Removing_E(self,Number):
        prefix= float(Number[0][0])
        suffix= int(Number[0][1])
        self.Number =  prefix*pow(10,suffix)
            
            
    def Numbers_Words(self,Number):
        return [Number,self.Inflect.ordinal(Number),self.Inflect.number_to_words(Number),self.Inflect.number_to_words(self.Inflect.ordinal(Number))]

    def Number_Without_Hyphen(self,Number):   
               return [('%s %s') %(self.Inflect.number_to_words(Number-Number%10),self.Inflect.number_to_words(Number%10)),('%s %s') %(self.Inflect.number_to_words(Number-Number%10),self.Inflect.number_to_words(self.Inflect.ordinal(Number%10))),('%s %s') %(self.Inflect.number_to_words(Number-Number%10, andword=''),self.Inflect.number_to_words(Number%10, andword='')),('%s %s') %(self.Inflect.number_to_words(Number-Number%10, andword=''),self.Inflect.number_to_words(self.Inflect.ordinal(Number%10)))]


    #slight change need to be incorporated in adding this to  ordinal as well
    def Number_Without_and(self,Number):
        return [self.Inflect.number_to_words(Number, andword=''),self.Inflect.number_to_words(self.Inflect.ordinal(Number), andword='')]

    #this function will insert comma for no above 999 else convert no into words
    #if you want to get no back then choose threshold as c-1
    def Number_With_Comma(self,Number):
        locale.setlocale(locale.LC_NUMERIC, "en_IN")
        return [self.Inflect.number_to_words(Number, threshold=999),locale.format("%d", Number, grouping=True)]


    def Number_Aliases(self,Number):
	
	Length = len(str(Number))
	millions = lambda Number: ['%0.1f million'%(float(Number)/pow(10,6)),'%d million'%(float(Number)/pow(10,6)),"%0.1f million"%(float(Number/pow(10,5))/10)]
	billions = lambda Number: ['%0.1f billion'%(float(Number)/pow(10,9)),'%d billion'%(float(Number)/pow(10,9)),"%0.1f billion"%(float(Number/pow(10,8))/10)]
	trillions = lambda Number:['%0.1f trillion'%(float(Number)/pow(10,12)),'%d trillion'%(float(Number)/pow(10,12)),"%0.1f tillion"%(float(Number/pow(10,11))/10)]
	lacs = lambda Number: ['%0.1f lakh'%(float(Number)/pow(10,5)),'%d lakh'%(float(Number)/pow(10,5)),\
				   '%0.1f lac'%(float(Number)/pow(10,5)),'%d lac'%(float(Number)/pow(10,5)),"%0.1f lac"%(float(Number/pow(10,4))/10),"%0.1f lakh"%(float(Number/pow(10,4))/10)]
	crores = lambda Number: ['%0.1f crore'%(float(Number)/pow(10,7)),'%d crore'%(float(Number)/pow(10,7)),"%0.1f crore"%(float(Number/pow(10,6))/10)]                


	if Number<=20:
            self.Combination =  self.Numbers_Words(Number)
            
        elif Length==2:
            if Number%10==0:
	    
                self.Combination = self.Numbers_Words(Number)
            else:
                self.Combination = set(self.Numbers_Words(Number) + self.Number_Without_Hyphen(Number))
                self.Combination=[w for w  in self.Combination]
                
        elif Length==3:
            
            if Number%10==0:
                
                self.Combination =  self.Numbers_Words(Number) + self.Number_Without_and(Number)
            
            else:
                
                if 11<=int(str(Number)[-2:])<=19:
                    self.Combination = self.Numbers_Words(Number)+self.Number_Without_and(Number)
                else:
                    self.Combination = self.Numbers_Words(Number) + self.Number_Without_Hyphen(Number)

           
        elif 4<=Length<=5:
            if Number%10==0:
                self.Combination = self.Number_With_Comma(Number) + self.Numbers_Words(Number)\
                + ['%d thousand'%(Number/1000),'%dk'%(Number/1000)]
            else:
                predecessor,succesor = self.Round_off(Number)
                self.Combination =  self.Number_With_Comma(Number) + self.Numbers_Words(Number)\
                + ['%d thousand'%(Number/1000),'%dk'%(Number/1000)]
            
                self.Combination +=  self.Number_With_Comma(predecessor) + self.Numbers_Words(predecessor)\
                + ['%d thousand'%(predecessor/1000),'%dk'%(predecessor/1000)]
            
                self.Combination +=  self.Number_With_Comma(succesor) + self.Numbers_Words(succesor)\
                + ['%d thousand'%(succesor/1000),'%dk'%(succesor/1000)]            
            
        elif Length==6:
            if Number%10==0:
                self.Combination = self.Number_With_Comma(Number) + self.Numbers_Words(Number)+\
                ['%d lakh'%(Number/1000),'%d lac'%(Number/1000)]
            else:
                self.Combination = self.Number_With_Comma(Number) + self.Numbers_Words(Number)+\
                ['%d lakh'%(Number/1000),'%d lac'%(Number/1000)]
                
                
        elif Length==7:
            self.Combination = self.Number_With_Comma(Number)+lacs(Number)+millions(Number)

        elif Length==8:
            self.Combination = self.Number_With_Comma(Number)+lacs(Number)+millions(Number)+crores(Number)
            
        elif Length ==9:
            self.Combination =self.Number_With_Comma(Number)+millions(Number)+crores(Number)
        elif Length==10:
            self.Combination =self.Number_With_Comma(Number)+crores(Number)+billions(Number)
        elif 11<=Length<=12:
            self.Combination =self.Number_With_Comma(Number)+billions(Number)
        elif 13<=Length<=15:
            self.Combination =self.Number_With_Comma(Number)+trillions(Number)
        else:
            print "limit exceded"      
            
    def Round_off(self,Number):
	power = pow(10,len(str(Number))-2)
	return (Number/power)*power , ((Number/power)+1)*power        

    def Main_Function(self,Number):
        Date = Number
        try:
            if re.match('(\d{4})-(\d{2})-(\d{2})',Date):     
                self.Converting_Date_Format1(re.findall('(\d{4})-(\d{2})-(\d{2})',Date))
                self.Combination = [self.date+" "+self.month+" "+self.year,self.date+" "+self.month+" "+self.year+ ",",self.month+","+" "+self.year]
                
            elif re.match('--(\d{2})-(\d{2})',Date):
                self.Converting_Date_Format2(re.findall('--(\d{2})-(\d{2})',Date))
            	self.Combination=[self.date+' '+self.month,self.date+' '+self.month+","]

            elif re.match('([0-9.]+)E([0-9.])',Number):
                Number =  re.findall('([0-9.]+)E([0-9.])',Number)
                self.Removing_E(Number)
                self.Number_Aliases(int(float(Number)))
                
            elif re.match('^[0-9.]+$',Number):
                self.Number_Aliases(int(float(Number)))
                
        except ValueError as e:
            print e
            pass