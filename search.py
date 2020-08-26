#!/usr/bin/python3
import re
import nltk
import sys
import getopt
import os
import pickle
from nltk.stem.porter import *
from nltk.corpus import wordnet
from collections import defaultdict
import math
stemmer = PorterStemmer()

def usage():
	print("usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results")
def intersecti(l1,l2):#intersetion of 2 list for "AND"
	i=0
	l=[]
	j=0
	while(i<len(l1) and j<len(l2)):
			if(l1[i][0]<l2[j][0]):
				i+=1
			elif(l1[i][0]>l2[j][0]):
				j+=1
			else:
				l.append((l1[i][0],l1[i][1]+l2[j][1]))
				i+=1
				j+=1
	return l

def run_search(dict_file, postings_file, queries_file, results_file):
	"""
	using the given dictionary file and postings file,
	perform searching on the given queries file and output the results to a file
	"""
	print('running search on the queries...')
	postingfile=open(postings_file,'rb')# opening the postings_file
	s=""# final output initialization

	with open(dict_file,'rb') as f:
		dict2 = pickle.load(f)# loading the dictionary of pointers to the postings_file for each word
		ranklist=pickle.load(f)# loading the pageranks
	with open(queries_file) as f:
		lines=f.readlines()
		for l in lines:
			lq1=[]
			for w in nltk.word_tokenize(l):
				
				lq1.append(w.casefold())
			x=""
				
			phrasal=0
	
			l21=[]
		
			for el in lq1:
				if(el=="``"):# phrasal type query
					phrasal=1

					
				elif(el=="''"):
					
					if(phrasal==1):
						l21.append(x[:-1])
						
					
					x=""

					phrasal=0
			
				else:
					if(phrasal==1):
					
							
						x+=el
						x+=" "


					else:
						l21.append(el)
				

			
			
			# implementation of wordnet
			synonyms = []


			for i in range(len(l21)):
				syns = wordnet.synsets(l21[i]) # to find similar words
				

				for syn in syns:
					for lx in syn.lemmas():
						elx=""
						
						for el in lx.name().split('_'):# some words are of form a_b. so we need to convert it to proper form
							elx+=stemmer.stem(el.casefold())+" "
							

						
						synonyms.append(elx[:-1])


			l31=[]
			for i in range(len(l21)):# doing the stemming after finding synonyms
				elx=""
						
				for el in l21[i].split():
					elx+=stemmer.stem(el)+" "
				l31.append(elx[:-1])
				

			queryset=list((set(l31)).union(set(synonyms)))
			


			
			querylength=len(queryset)
			outputfilelist=[] # final list of files for the query
			
			for x in range(querylength):
				var=dict2.get(queryset[x])
			
				if (var!=None):
					postingfile.seek(var)
					mylist1=pickle.load(postingfile)
					for xx in mylist1:
						
						outputfilelist.append(xx)
			outputfilelist=list(set(outputfilelist))
			
			
			done=0
			
			for i in ranklist:
				if i in outputfilelist:


					done=1
					s+=str(i)+" "

			if(done==1):
				s=s[:-1]# to remove last space
			else:
				s=s
				


	postingfile.close()
	
	with open(results_file,'w') as ff:
		ff.write(s)#removing the last newline and writing to the results_file

	

dictionary_file = postings_file = file_of_queries = output_file_of_results = None

try:
	opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError:
	usage()
	sys.exit(2)

for o, a in opts:
	if o == '-d':
		dictionary_file  = a
	elif o == '-p':
		postings_file = a
	elif o == '-q':
		file_of_queries = a
	elif o == '-o':
		file_of_output = a
	else:
		assert False, "unhandled option"
if dictionary_file == None or postings_file == None or file_of_queries == None or file_of_output == None :
	usage()
	sys.exit(2)

run_search(dictionary_file, postings_file, file_of_queries, file_of_output)
