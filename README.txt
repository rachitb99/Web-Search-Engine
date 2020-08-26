This is the README file for A0214350W's submission (email - e0523366@u.nus.edu)

== Python Version ==

I'm (We're) using Python Version 3.8.2 for this assignment.

== General Notes about this assignment ==

In index.py, firstly we collect the documents and place it in the given directory of documents. If the directory with the given name is not present we create the directory. Then I used the crawling algorithm taught in the lecture to collect the documents. I used "http://www.w3schools.com" as a seed URL as this website contains alot of information about the different topics of computer science and I like this website. I append this seed into url list. We can append as many seed pages we want. While url list is not empty, I take url from the queue, then I fetch and parse the page, then I extract all URLs from the page and append them to the url list. I used Beautiful Soup library to parse the page and get the urls and the content and then properly formatted the content. I store all the text content of the page properly in a file which has document ID as it's name. To build the transition probability matrix for the page rank algorithm, firstly I store the probability to reach any page j from a page i. Then I updated the probabilities of matrix by assigning 0.1 probability for teleportation to occur. Then, I kept on multiplying the probability vector x with the transition probability matrix until it got stable. I noticed that multiplying x with the transition probability matrix 100 times is more than sufficient. Then, I used the final x to find the rank for each URL. Then, I wrote the code to create dictionary of words/2-words/3-words and respective list of files in which the word/2-word/3-word is present. The dictionary of words with pointers to the position of the list in postings.txt is kept in dictionary.txt. I stored the pointers using tell(). Basically using pickle I dumped a dictionary with words as keys and pointers as values in dictionary.txt. Then I dumped the page ranks in dictionary.txt. I implemented casefolding, stemming and tokenizing using nltk library. Index.py takes about 22 minutes in my laptop.

In search.py, I wrote the code to search for a query to get the list of files corresponding to the query rankwise according to the page rank algorithm. Using pickle I loaded the dictionary.txt but did not load postings.txt as it is a large file. I will load postings.txt only for a particular list when needed using pointers in dictionary from dictionary.txt. I checked whether the query contains phrases or not and kept the terms in the phrases together so that we can search for the phrase as a whole. Finally, I kept on storing the output of the query in a string 's' and then wrote the string into the results_file. I implemented query expansion technique in which I expanded the query by including the words/2-words (converted it into the form of 2-words when the synonym is of form x_y) similar to the words of the query using wordnet.

== Files included with this submission ==

index.py - code to collect the documents, find their ranks using page rank algorithm and to create dictionary of words/2-words/3-words and respective list of files in which the word/2-word/3-word is present
search.py - code to search for a query to get the list of files corresponding to the query rankwise according to the page rank algorithm
dictionary.txt - file to store the dictionary of words/2-words/3-words and respective list of files in which the word/2-word/3-word is present. I also store rank for each page
postings.txt - file to store respective list of files in which the word is present
q1.txt - example query
q2.txt - example query
q3.txt - example query
q4.txt - example query
q5.txt - example query
q6.txt - example query
q7.txt - example query
q8.txt - example query
bs4 folder - beautiful soup library

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[x] I/We, A0214350W, certify that I/we have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I/we
expressly vow that I/we have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I/We, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

We suggest that we should be graded as follows:

<Please fill in>

== References ==

www.w3schools.com
https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python
