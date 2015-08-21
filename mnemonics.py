import re
import random
import nltk
import sys

class Word:
    word = ""
    pos = []
    
    def __init__(self, word, pos):
        self.word = word
        self.pos = pos

word_re = re.compile("<word>(?P<word>.*)</word><pos>(?P<pos>.*)</pos>")

class Name:
    name = ""
    initials = ""
    
    def __init__(self, name, initials):
        self.name = name
        self.initials = initials
        
def find_word(starts_with, pos, words):
    matching = []
    for word in words:
        if word.word.lower().startswith(starts_with):
            if pos.lower() == word.pos.lower():
                matching.append(word.word)
    return matching[int(random.random()*len(matching))%len(matching)]
    
def read_word_list(file):
    words = []
    for line in file:
        if line.strip() != "":
            m = word_re.search(line)
            words.append(Word(m.group("word"), m.group("pos")))
    return words
        
def find_matching_names(char1, char2, names):
    matches = []
    for name in names:
        if name.initials.lower() == char1 or name.initials.lower() == char1+char2:
            matches.append(name)
    
    return matches
    
'''def check_pos(pos):
    pos_arr = []
    if "n." in pos_string and not "pron." in pos_string:
        pos_arr.append("n.")
    if "a." in pos_string or "adj." in pos_string:
        pos_arr.append("adj.")
    if "adv." in pos_string:
        pos_arr.append("adv.")
    if "pron." in pos_string:
        pos_arr.append("pron.")
    if "v." in pos_string and not "adv." in pos_string:
        pos_arr.append("v.")
    if "prep." in pos_string:
        pos_arr.append("prep.")
    if "conj." in pos_string:
        pos_arr.append("conj.")
    
    return pos_arr'''
        
#entry_parse = re.compile(".*<ent>(?P<word>[a-zA-Z]+?)</ent>.*<pos>(?P<pos>.*?)</pos>.*")
    
#dir = ""
#file = open("adverbs.txt")
initials = open("initials.txt")
word_list = open("words.txt", "a+")

names = []
for line in initials:
    vals = line.replace("\n","").split(",")
    names.append(Name(vals[1], vals[0]))
    
'''for line in file:
    line = line.strip().replace("\n","")
    if line.endswith("e"):
        line += "d"
    else:
        line += "ed"
    word_list.write("<word>" + line + "</word><pos>RB</pos>\n")
exit(0)'''

words = []
reading = False #set to append new words to dictionary
if reading:

    num_lines = sum(1 for line in file)
    file.seek(0)
    cur_line = 1

    for line in file:
        if line == "\n":
            continue
        try:
            #print line
            print line.replace("\n","").decode("utf-8", 'ignore')
            tokens = nltk.word_tokenize(line.replace("\n","").decode("utf-8", 'ignore'))
        except:
            exit()
        pos_tags = nltk.pos_tag(tokens)
        print pos_tags
        
        for w in pos_tags:
            words.append(Word(w[0], w[1]))
            
        sys.stdout.write( str(int(float(cur_line)/float(num_lines) * 100)) + "% read\r")
        cur_line += 1
        #word_spl = line.split(" ")
        #word_spl = [g.replace("\"", "").replace(".", "").replace("!","").replace("\n", "") for g in word_spl]
        #print word_spl

        
    for word in words:
        word_list.write("<word>" + word.word + "</word><pos>" + word.pos + "</pos>\n")
else:
    words = read_word_list(word_list)

#Add articles
#words.append(Word("A", "det."))
#words.append(Word("An", "det."))
#words.append(Word("The", "det."))

'''alpha = "abcdefghijklmnopqrstuvwxyz"
for char in alpha:
    entries = []
    dict = open(dir + "gcide_" + char + ".xml")

    #print "parsing " + char + " words"
    found_word = False
    entry = ""

    for line in dict:
        if line.startswith("<p><ent>"):
            entry = line
            found_word = True
        elif found_word:
            entry += line
        if "</p>" in line and found_word:
            found_word = False
            entries.append(entry.replace("\n",""))
     
    for entry in entries:
        m = entry_parse.search(entry)
        if m != None:
            pos_string = m.group("pos")
            pos = check_pos(pos_string)
            word = Word(m.group("word"), pos)
            words.append(word)
'''
#print words[1].word
#print words[1].pos

alpha = "abcdefghijklmnopqrstuvwxyz"
str = ""
for i in range(0,12):
    index = random.random()
    str += alpha[int(index*len(alpha))%len(alpha)]
str = "testing"
str_iter = iter(str)

#Noun, adverb, pronoun, adj, verb, adverb, preposition, conjunction, article
connectors = ["and", "but", "then", "after", "when"]

state = "PN"
sentence = ""
pos_order = ""
next_state = []
had_verb = False

for i, char in enumerate(str_iter):
    index = random.random()
    
    #print state
    #there can be cases where we chose a next state that doesn't have any possible words. 
    #ex: preposition starting with g
    found_word = False
    while found_word == False:
        try:
            if state != "PN":
                word = find_word(char, state, words).capitalize()
                if word == "since":
                    #we can add another verb"
                    had_verb = False
                sentence += word + " "
            else:
                if str[i+1] != None:
                    match_names = find_matching_names(char, str[i+1], names)
                else:
                    match_names = find_matching_names(char, "", names)
                name = match_names[int(index*len(match_names))%len(match_names)]
                if len(name.initials) == 2:
                   str_iter.next()
                sentence += name.name + " "
            found_word = True
            pos_order += state + " "
        except Exception, e:
            print e
            next_state.remove(state)
            print "removed: " + state + " for letter: " + char
            if len(next_state) == 0:
                print "Cannot find any possible mnemonics"
                exit(0)
            
            state = next_state[int(index*len(next_state))%len(next_state)]
            
    
    if state == "NNS" or state == "NN" or state == "PN":
        #noun
        next_state = ["IVB", "TVB", "CC", "RB"]   
        if had_verb == True:
            sentence += ", " + connectors[int(index*len(connectors))%len(connectors)] + " "
            next_state = ["NNS", "PN", "NN"]
            #next_state = ["CC"]
            had_verb = False
        prev_state = state
        state = next_state[int(index*len(next_state))%len(next_state)]
    elif state == "RB":
        #adv
        next_state = []
        if prev_state in ["IVB", "TVB"]:
            next_state.append("IN")
        elif prev_state in ["NNS", "PRP$", "PN"]        :
            next_state.extend(["TVB", "IVB"])            
        prev_state = state
        state = next_state[int(index*len(next_state))%len(next_state)]
    elif state == "PRP$":
        #pron
        next_state = ["NNS", "NN"]
        prev_state = state
        state = next_state[int(index*len(next_state))%len(next_state)]
    elif state == "JJ":
        #adj
        next_state = ["JJ", "NNS", "PN", "NN"]
        prev_state = state
        state = next_state[int(index*len(next_state))%len(next_state)]
    elif state == "TVB":
        #verb
        had_verb = True
        next_state = ["IN", "DT", "NNS", "PN", "PRP$", "CC"]
        if prev_state != "RB":
            next_state.append("RB")
        prev_state = state
        state = next_state[int(index*len(next_state))%len(next_state)]
    elif state == "IVB":
        had_verb = True
        next_state = ["IN"]
        if prev_state != "RB":
            next_state.append("RB")
        prev_state = state
        state = next_state[int(index*len(next_state))%len(next_state)]
    elif state == "IN":
        #prep
        next_state = ["DT", "NNS", "PN", "NN"]
        prev_state = state
        state = next_state[int(index*len(next_state))%len(next_state)]
    elif state == "CC":
        #conj
        if had_verb == True:
            next_state = ["TVB", "IVB"]
        else:
            next_state = ["NNS", "DT", "PN", "NN"]
        prev_state = state
        state = next_state[int(index*len(next_state))%len(next_state)]
    elif state == "DT":
        #determiner
        next_state = ["NNS", "JJ", "NN"]
        prev_state = state
        state = next_state[int(index*len(next_state))%len(next_state)]

print pos_order
print sentence
