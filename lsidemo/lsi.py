'''
Created on May 13, 2014

@author: jinling
'''
#!/usr/bin/python
import MySQLdb
import nltk
import string
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.lancaster import LancasterStemmer
from gensim import corpora, models, similarities
import logging
import sys 

# reload(sys)
# sys.setdefaultencoding('utf-8') 

def get_tokens():
    db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="123456", # your password
                      db="sumline",
                      charset='utf8') # name of the data base
    cur = db.cursor() 
    cur.execute("select * from content_item where country='gb' limit 1000")
   
    texts=[]
#    textsTokens=[]
    for row in cur.fetchall():
        texts.append(row[7])

    return texts
#     for text in texts:
#         lowers = text.lower()
#         #remove the punctuation using the character deletion step of translate
#         no_punctuation = lowers.translate(None, string.punctuation)
#         tokens = nltk.word_tokenize(no_punctuation)
#         textsTokens.append(tokens)
#     return textsTokens
       
            
        
        
     
    
documents = get_tokens()
print documents
english_punctuations = [',','.',':',';','?', '(', ')', '[',']', '&','!', '*', '@','#', '$', '%']
english_stopwords = stopwords.words('english')

# tokenization
texts_tokenized = [[word.lower() for word in word_tokenize(document)] for document in documents]
print texts_tokenized[5]

# remove stop-words
texts_filtered_stopwords = [[word for word in document if not word in english_stopwords] for document in texts_tokenized]
print texts_filtered_stopwords[5]

# remove punctuations
texts_filtered = [[word for word in document if not word in english_punctuations] for document in texts_filtered_stopwords]
print texts_filtered[5]


# stemming using LancasterStemmer
st = LancasterStemmer()
texts_stemmed = [[st.stem(word) for word in docment] for docment in texts_filtered]
print texts_stemmed[5]


#texts = [[stem for stem in text] for text in texts_stemmed]
#remove words of frequency 1
all_stems = sum(texts_stemmed, [])
stems_once = set(stem for stem in set(all_stems) if all_stems.count(stem) == 1)
texts = [[stem for stem in text if stem not in stems_once] for text in texts_stemmed]



logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

dictionary = corpora.Dictionary(texts)

#mapping string to number
corpus = [dictionary.doc2bow(text) for text in texts]

#getting tfidf vector
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

#make lsi model based on tfidf vector
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=10) 

#index matrix based on lsi
index = similarities.MatrixSimilarity(lsi[corpus])

#query related articles for the fifth document
query = texts[5]

query_bow = dictionary.doc2bow(query)
query_lsi = lsi[query_bow]
sims = index[query_lsi]
sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])



# check the effectiveness
print "query is: "+documents[5]
print "The top 5 similar article:"

#point out the five most similar articles
for sims in sort_sims[0:5]:
    print documents[sims[0]]
    






        

    
    
 
      