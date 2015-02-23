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

result_text = ["" for _ in xrange(a)]
result_text_debug = ["" for _ in xrange(a)] 
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
        non_printed_words = []
        for engine in engines_order:
            if len(engine_lines[engine]) > word_number:
                word = engine_lines[engine][word_number]
                stemmed_word = stemmer.stem(word.decode("utf-8"))
                if common_occurences[stemmed_word] > 1:
                    printed = True
                    common_occurences[stemmed_word] = 0
                    if punktuation[stemmed_word] > 0:
                        punktuation[stemmed_word] -= 1
                        result_text[line_number] += \
                            word + punktuation_symbol[stemmed_word] + " " 
                        result_text_debug[line_number] += \
                            word + punktuation_symbol[stemmed_word] + " "
                        #print word + punktuation_symbol[stemmed_word],
                    else:
                        result_text[line_number] += word + " "
                        result_text_debug[line_number] += word + " "
                        #print word,
                else:
                    non_printed_words += [word]
        if not printed:
            # Trash.
            if (len(non_printed_words) == 2 and 
                stemmer.stem(non_printed_words[0].decode("utf-8")) == \
                stemmer.stem(non_printed_words[1].decode("utf-8"))) \
                or (len(non_printed_words) == 3 and 
                    stemmer.stem(non_printed_words[0].decode("utf-8")) == \
                    stemmer.stem(non_printed_words[1].decode("utf-8")) and \
                    stemmer.stem(non_printed_words[1].decode("utf-8")) == \
                    stemmer.stem(non_printed_words[2].decode("utf-8"))):
                result_text_debug[line_number] += non_printed_words[0]
                result_text[line_number] += non_printed_words[0] + " "
            else:
            #print "_(%s)" % (non_printed_words),
                non_printed_words = " ".join(non_printed_words)
                result_text_debug[line_number] += \
                    "_(%s)" % (non_printed_words) + " "
            
    #print
    
f = open("./data/replace_dict")
lines = f.readlines()
f.close()

for item in result_text_debug:
    result_text_debug[0] += "Проверкой,"


# It can work really faster.
for line in lines:
    term = line.split()[0]
    replacement = line.split()[1]
    for line_number in xrange(len(result_text_debug)):
        result_text[line_number] = re.sub(term, replacement, 
                                          result_text[line_number], 
                                          flags = re.U)
        result_text_debug[line_number] = \
                                   re.sub(term, replacement, 
                                          result_text_debug[line_number], 
                                          flags = re.U)
                                  
banned_symbols = [".", ",", "?", ":", ";", "!"] 
with open("data/debug_output.txt", "w") as f:
    for item in result_text_debug:
        if item[-2] in banned_symbols:
            print >>f, item[:-2]
        else:
            print >>f, item
        
with open("data/output.txt", "w") as f:
    for item in result_text:
        if item[-2] in banned_symbols:
            print >>f, item[:-2]
        else:
            print >>f, item
        