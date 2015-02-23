#-*- coding: utf-8 -*-

import collections
import nltk


# Install punkt package first using next line (13Mb).
# 2nltk.download()
 
filename_english_text = "./data/english_sample.txt"
filename_russian_text = "./data/russian_samples.txt"

f = open(filename_russian_text)
lines = f.readlines()
f.close()


stemmer = nltk.stem.SnowballStemmer("russian")

translate_google = []
translate_micros = []
translate_yandex = []


translations = [translate_google, translate_micros, translate_yandex]
i = 0

for line in lines:
    current_list = translations[i]
    if line[0] == "#":
        continue
    
    if len(line) == 1:
        i += 1
    else:
        current_list += [line] 

# Checking correctness of input data.
a = len(translate_google)
b = len(translate_micros)
c = len(translate_yandex)

if (a != b) or (a != c):
    print "Can not read input data:\n    google -- %d line(s).\n    bing   -- %d"\
        " line(s).\n    yandex -- %d line(s)." % (a, b, c) 
    assert(False)

dicts = [[], [], []]

translations_tokenized = [[], [], []]
# i -- number of sentence.
for i in xrange(a):
    # j -- number of translate engine.
    for j in xrange(len(translations)):
        dicts[j] = collections.Counter()
        line = translations[j][i]
        
        for item in nltk.word_tokenize(line):
            dicts[j][stemmer.stem(item.decode("utf-8"))] = 1
    
    full_dict = collections.Counter()
    
    for dict in dicts:
        for item in dict:
            full_dict[item] += 1
    
    line_google = nltk.word_tokenize(translations[0][i])
    line_micros = nltk.word_tokenize(translations[1][i])
    line_yandex = nltk.word_tokenize(translations[1][i])
    
    line = []
    for t in xrange(max(
                    [len(line_google), len(line_yandex), len(line_micros)])):
        
        printed = False
        non_printed_words = ""
        
        if len(line_yandex) > t:
            if full_dict[stemmer.stem(line_yandex[t].decode("utf-8"))] > 1:
                full_dict[stemmer.stem(line_yandex[t].decode("utf-8"))] = 0
                printed = True
                print line_yandex[t],
            else:
                non_printed_words += line_yandex[t] + " "
            #line += [line_yandex[t]]
        if len(line_google) > t:
            if full_dict[stemmer.stem(line_google[t].decode("utf-8"))] > 1:
                full_dict[stemmer.stem(line_google[t].decode("utf-8"))] = 0    
                printed = True
                print line_google[t],
            else:
                non_printed_words += line_google[t] + " "
            
            #line += [line_google[t]]
        if len(line_micros) > t:
            if full_dict[stemmer.stem(line_micros[t].decode("utf-8"))] > 1:
                full_dict[stemmer.stem(line_micros[t].decode("utf-8"))] = 0
                printed = True
                print line_micros[t],
            else:
                non_printed_words += line_micros[t] + " "
            
            #line += [line_micros[t]]
        if not printed:
            print "_:(%s)" % (non_printed_words),
    #for word in line:
    #    print word
            
    for word in line:
    #    print word
        if full_dict[stemmer.stem(word.decode("utf-8"))] > 1:
            print word,
            full_dict[stemmer.stem(word.decode("utf-8"))] = 0
         
    print "\n" + "-" * 80