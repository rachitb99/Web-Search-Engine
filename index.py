#!/usr/bin/python3
import os
import urllib.request
from bs4 import BeautifulSoup
import math
from collections import defaultdict
import re
import nltk
import sys
import getopt
import csv
from nltk.stem.porter import *

import pickle
def usage():
	print("usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file")


input_directory = output_file_dictionary = output_file_postings = None

try:
	opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError:
	usage()
	sys.exit(2)


for o, a in opts:
	if o == '-i': # input directory
		input_directory = a
	elif o == '-d': # dictionary file
		output_file_dictionary = a
	elif o == '-p': # postings file
		output_file_postings = a
	else:
		assert False, "unhandled option"

if input_directory == None or output_file_postings == None or output_file_dictionary == None:
	usage()
	sys.exit(2)

if (not(os.path.isdir(input_directory))):# if directory-of-documents not present create it

	os.mkdir(input_directory)

seed="http://www.w3schools.com"

urllist=[]
fetchedurls=[]# list of fetched urls
urllist.append(seed)
c=1
alpha=0.1#teleportation
x=[1/2000]*2000 # initial probability vector

A0=[0]*2000
A1=[A0]*2000# to store the transition probability matrix
A=defaultdict(dict)# initially storing the transition probability matrix in form of dictionary
B=defaultdict(int)# storing the id corresponding to each url

while urllist:
	myurl=urllist[0]# obtain the first url
	urllist.pop(0) 

	if(len(fetchedurls)==2000):
		break
	if myurl not in fetchedurls: # no duplication
		

		childurls = []# the links referred in the page 
		
		try:
			
			with urllib.request.urlopen(myurl) as response:#fetch the url
			   the_page = response.read()

			soup = BeautifulSoup(the_page,'html.parser') # parsing of fetched page

			anchor_tag_links = soup("a") # get the links in the page
			for link in anchor_tag_links:
				if link.has_attr("href"):
					tempurl = urllib.parse.urljoin(myurl, link["href"])
					childurls.append(tempurl)
			
			text = soup.get_text() # get the text content in the page

			lines = (line.strip() for line in text.splitlines())
			chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
			text = '\n'.join(chunk for chunk in chunks if chunk)

			with open ("pages/"+str(c),'w',encoding="utf-8") as f:# store the pages into files
				f.write(text)

			for link in childurls:# store the count of each link in a page to find probability
				if A[myurl].get(link)==None:
					A[myurl][link]=1
				else:
					A[myurl][link]+=1

				urllist.append(link)
			B[myurl]=c# storing the id corresponding to each url
			c+=1

			fetchedurls.append(myurl)# append in fetched urls
		except:
			pass




for el in A:
	sum=0
	for l in A[el]:# converting dictionary in form of matrix
		if B.get(l)!=None:
			A1[B[el]-1][B[l]-1]=A[el][l]
			sum+=A[el][l]
	for l in A[el]:
		if B.get(l)!=None:
			A1[B[el]-1][B[l]-1]/=sum # to calculate probability from count
			A1[B[el]-1][B[l]-1]*=(1-alpha) # take teleportation into account
			A1[B[el]-1][B[l]-1]+=(alpha)/2000


prevcheckdiff=1
iii=100
while(iii>0):
	newx=[0]*2000
	for i in range(2000): # matrix multiplication xA
		for j in range(2000):
			newx[i]+=x[j]*A1[j][i]
	checkdiff=0
	for i in range (2000):
		checkdiff+=(newx[i]-x[i])*(newx[i]-x[i])
	
	
	
	iii-=1
	prevcheckdiff=checkdiff
	y=0
	for i in range(2000):
		y+=newx[i]
	for i in range (2000):
		x[i]=newx[i]/y

finalrank=[0]*2000
finalrank1=[0]*2000

for i in range(2000):
	finalrank[i]=(-1*x[i],i+1)
finalrank.sort(key =lambda tup:tup[0])
for i in range(2000):# keeping the document ids in order of rank
	finalrank1[i]=finalrank[i][1]



stemmer = PorterStemmer()



def build_index(in_dir, out_dict, out_postings):
	"""
	build index from documents stored in the input directory,
	then output the dictionary file and postings file
	"""
	print('indexing...')
	dict1={}# dictionary containing the word as the key and posting list as the value

	c=1
	for file in os.listdir(in_dir):
		
		thefile=in_dir+file# adding the path of directory
		with open(thefile) as f:
			
			c+=1
			f=f.read()
			
			fileind=file

			for t in nltk.sent_tokenize(f):# for 2-words
				liss=nltk.word_tokenize(t)
				for w in range(len(liss)-1):
				
					w1=stemmer.stem(liss[w].casefold())# casefolding and stemming
					w2=stemmer.stem(liss[w+1].casefold())
					w3=w1+" "+w2
					if(dict1.get(w3)==None):
						
						dict1[w3]={}
						dict1[w3][fileind]=1
					else:
						

						if(dict1[w3].get(fileind)!=None):# check whether present file already present for that 2-word
							dict1[w3][fileind]+=1
							
						else:
							dict1[w3][fileind]=1
				

				for w in range(len(liss)-2): # for 3-words
					
					w1=stemmer.stem(liss[w].casefold())# casefolding and stemming
					w2=stemmer.stem(liss[w+1].casefold())
					w4=stemmer.stem(liss[w+2].casefold())
					w3=w1+" "+w2+" "+w4
					if(dict1.get(w3)==None):
	
						dict1[w3]={}
						dict1[w3][fileind]=1
					else:
						

						if(dict1[w3].get(fileind)!=None):# check whether present file already present for that 3-word
							dict1[w3][fileind]+=1
							
						else:
							dict1[w3][fileind]=1
				

				for w in nltk.word_tokenize(t):#for normal words
					
					w=stemmer.stem(w.casefold())# casefolding and stemming
					if(dict1.get(w)==None):
						
						dict1[w]={}
						dict1[w][fileind]=1
					else:
						

						if(dict1[w].get(fileind)!=None):# check whether present file already present for that word
							dict1[w][fileind]+=1
							
						else:
							dict1[w][fileind]=1

							

	dict2={}
	with open(output_file_postings,'wb') as f:
		for x in dict1:
			
			dict2[x]=(f.tell())# using f.tell() to tell the position of that list object in out_postings corresponding to the word in the out_dict. Also storing the document frequency in out_dir
			
			lis=[]
			for y in dict1[x]:
				lis.append(int(y))
			lis.sort()#sorting

			pickle.dump(lis,f)# pickle the object to out_postings
	with open(output_file_dictionary,'wb') as f:
		pickle.dump(dict2,f)# pickle the dictionary to out_dict
		pickle.dump(finalrank1,f)
	


	



build_index(input_directory, output_file_dictionary, output_file_postings)


