#!/usr/bin/env python
#coding=utf-8

from gensim import corpora, models, similarities
from pprint import pprint
from operator import itemgetter

import sys
import json
import time
import re

regex = re.compile(r"[^\w\s]")

f = open(sys.argv[1], 'r')

print time.time()

docs = []

for line in f:
    obj = json.loads(line, encoding="utf8")
    docs.append(regex.sub('', obj['data']['content']))

print len(docs)

stoplist = set(
    'for a of the and to in i u we they he she it my his her their our its am is are was were be has been on at upon above below javascript'.split())

texts = [[word for word in doc.lower().split() if word not in stoplist] for doc in docs]

all_tokens = sum(texts, [])

#print all_tokens
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)

texts = [[word for word in text if word not in tokens_once] for text in texts]

print time.time()
#print texts

dic = corpora.Dictionary(texts)

#dic.save('./test.dic')

#print dic

corpus = [dic.doc2bow(text) for text in texts]

#corpora.MmCorpus.serialize('./test.mm', corpus)

tfidf = models.TfidfModel(corpus)

corpus_tfidf = tfidf[corpus]

lsi = models.LsiModel(corpus_tfidf, id2word=dic, num_topics=50)

print time.time()

i = 0
for t in lsi.print_topics(50):
    print '[topic #%s]: ' % i, t
    i += 1

index = similarities.MatrixSimilarity(lsi[corpus])

count = 0

for doc in docs:
    print "Num.", count
    count += 1
    print doc
    texts = [word for word in doc.lower().split() if word not in stoplist]
    vec_bow = dic.doc2bow(texts)
    vec_lsi = lsi[vec_bow]
    vec_lsi_sort = sorted(vec_lsi, key=itemgetter(1), reverse=True)
    print 'topic probability:'
    pprint(vec_lsi_sort[:10])
    sims = sorted(enumerate(index[vec_lsi]), key=itemgetter(1), reverse=True)
    print 'top 10 similary notes:'
    pprint(sims[:10])
