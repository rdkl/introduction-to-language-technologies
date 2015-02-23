#-*- coding: utf-8 -*-

import collections
import nltk
import re


# Install punkt package first using next line (13Mb). It is necessary for 
# stemmer's correctness.
# nltk.download()
filename_english_text = "./data/english_sample.txt"
filename_russian_text = "./data/russian_samples.txt"

f = open(filename_russian_text)
lines = f.readlines()
f.close()


# Stemmer for translated words.
stemmer = nltk.stem.SnowballStemmer("russian")

translate = {"google" : [], "bing" : [], "yandex" : []}
# Order of engines in file with translated texts.
engines_order = ["google", "bing", "yandex"]

# i is a number of engine.
i = 0
for line in lines:
    current_list = translate[engines_order[i]]
    if line[0] == "#":
        continue
    
    if len(line) == 1:
        i += 1
    else:
        # Remove last \n.
        current_list += [line.rstrip(". \n?!")]
        
# Change order.
engines_order = ["yandex", "google", "bing"]

# Now in translate[engine] we have list of lines obtainted from that engine.
# Checking correctness of input data.
a = len(translate["google"])
b = len(translate["bing"])
c = len(translate["yandex"])

if (a != b) or (a != c):
    print "Can not read input data:\n    google -- %d line(s).\n    bing   -- %d"\
        " line(s).\n    yandex -- %d line(s)." % (a, b, c) 
    assert(False)
    
# Save punktuation.
tracked_punkt_symbols = [",", ":", ";"]
# Number of occurrences of current word -- punkt symbol. 
punktuation = collections.Counter()
# Concrete symbol for word.
punktuation_symbol = collections.Counter()

for line_number in xrange(a):
    # Number of occurrences of current stemmed word in translated engine.
    occurences_dict = {engine : {} for engine in engines_order}
    common_occurences = collections.Counter()
    
    for engine in engines_order:
        line = translate[engine][line_number]
        for word in line.split():
             if word[-1] in tracked_punkt_symbols:
                 stemmed_word = stemmer.stem(word[:-1].decode("utf-8"))
                 punktuation[stemmed_word] += 1
                 punktuation_symbol[stemmed_word] = word[-1]
             else:
                 stemmed_word = stemmer.stem(word.decode("utf-8"))
                 
             occurences_dict[engine][stemmed_word] = 1

        for item in occurences_dict[engine]:
            common_occurences[item] += 1
    
    engine_lines = {engine : re.sub('[:,;]', '', 
                                    translate[engine][line_number]).split()
                    for engine in engines_order}
    
    #print engine_lines["yandex"]
    max_len = max([len(item) for item in engine_lines.values()])
    
    #for item in engine_lines["yandex"]:
    #    print item, stemmer.stem(item.decode("utf-8"))
    
    for word_number in xrange(max_len):
        printed = False
        non_printed_words = ""
        for engine in engines_order:
            if len(engine_lines[engine]) > word_number:
                word = engine_lines[engine][word_number]
                stemmed_word = stemmer.stem(word.decode("utf-8"))
                # print "\n", word, stemmed_word, common_occurences[stemmed_word]
                if common_occurences[stemmed_word] > 1:
                    printed = True
                    common_occurences[stemmed_word] = 0
                    if punktuation[stemmed_word] > 0:
                        punktuation[stemmed_word] -= 1
                        print word + punktuation_symbol[stemmed_word],
                    else:
                        print word,
                else:
                    non_printed_words += word + " "
        if not printed:
            print "_(%s)" % (non_printed_words),
    
    print