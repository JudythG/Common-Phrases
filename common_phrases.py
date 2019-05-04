# How make tokens in all_tokens lowercase (so "the" equals "The")?  
# JTG: 'as' returns lines for 'has'
# JTG: searching uses regualar expressions. 
#	What if a characer in the snippet needs to be escaped?
# Future: if snippet cross line boundaries, list includes both lines
# JTG: warning if poem contains grammar not handled
# store reults to JSON?
# if token is 'd' or 's', remove it

import requests
import nltk
import string
#from nltk.text import TokenSearcher
import re

def make_snippet (tokens):
    if type(tokens) == str:
        return tokens
        #regex = '[^a-zA-Z0-9]' + tokens + '[^a-zA-Z0-9]'
        #return regex

    snippet = ''
    for token in tokens:
        # if this token is punctuation,
        # remove trailing ' ' (if any) in snippet
        if token in string.punctuation:
            if snippet.endswith(' '):
                snippet = snippet[:-1]

        snippet += token
        snippet += ' ' 
 
    # if trailing blank, remove it           
    if snippet.endswith(' '):
        snippet = snippet[:-1]

    return snippet

def make_snippets_from_text(text):
    list_of_snippets = []
    for token in text:
        list_of_snippets.append(token)
    return list_of_snippets

def make_snippets(list_of_tokens):
    list_of_snippets = []
    for token in list_of_tokens:
        snippet = make_snippet(token)
        if snippet:
            list_of_snippets.append(snippet)
    return list_of_snippets

# JTG: for now, assume one poem
# poems -> a list of poem dictionary elements
#   each of whose 'lines' key maps to a list of lines of the poem
# returns all words of the poem in one string
def parse_poem_from_json(poem_dict):
    poem = ' ' 
    for line in poem_dict['lines']:
        poem += ' ' + line
    return poem

def pick_snippet (snippets):
    idx_to_snippets = {}
    count = 0
    for s in snippets:
        idx_to_snippets[count] = s
        count += 1
        
    while True:
        print ('enter number to pick a snippet or q to quit: ')
        for d, v in idx_to_snippets.items():
            print ('{0}: {1}'.format(d, make_snippet(v[0])))

        result = input()
        if result == 'q':
            return None

        try: 
            idx = int(result)
        except: 
            print('enter a number to pick a snippet or q to quit: ')
        else:
            if idx >= 0 and idx < len(idx_to_snippets):
                return make_snippet(idx_to_snippets[idx][0])

# for now, default to Leaves of Grass
# To Do:
#	Allow user to enter author and title
#	poetrydb can return multiple poems, allow user to pick one
#	read poem from JSON file (same format as poetrydb.org
def select_poem():
    list_of_poems = []

    # Load Whitman's 'Leaves of Grass'
    req = requests.get ('http://poetrydb.org/title/I%20Sing%20the%20Body%20Electric/lines,author,title')
    if req.status_code == 200:
        poems = req.json()
        poem = poems[0]
        list_of_poems.append (poem)

    if len(list_of_poems) == 0:
        return None
    if len(list_of_poems) == 1:
        return list_of_poems[0]

# for one-word tokens, token can be part of another word
# so if 1-word token, regex -> 'space|punctuaion snippet space|punctuation'
def get_poem_lines_for_snippets(snippet_tokens, poem_lines):
    snippet_with_line_idx = {}
    for snippet in snippet_tokens:
        snippet_lines = []
        line_idx = 0
        for line in poem_lines:
            if snippet in line:
                snippet_lines.append(line_idx)
            line_idx += 1
        snippet_with_line_idx [snippet] = snippet_lines
    return snippet_with_line_idx

def grammar_parse(token):
    # keep snippets if tokens have these tags
    keep_tags = ['CD', 'FW', 'JJ', 'JJ.', 'NN', 'NN.', 'RB', 'RB.', 'RP', 'VB', 'VB.', 'UH']

    # tags we don't keep
    # keep_tags and reject_tags together used to identify tags that haven't
    #	been considered
    reject_tags = ['CC', 'DT', 'EX', 'IN', 'MD', 'PDT', 'PRP', 'PRP.', 'SYM', 'TO', 'WDT', 'WP', 'WRB']

    #if token not in keep_tags and token not in reject_tags:
        # error handling to tell user haven't considered thistoken type

    if token[1] not in keep_tags:
        return False
    return True

# parsing list of tokens
def parse_down_tokens(tokens):
    tokens_to_keep = []
    tagged_tokens = nltk.pos_tag(tokens)
    for token in tagged_tokens:
        keep_token = True

        if token[0] in string.punctuation:
            keep_token = False

        if grammar_parse(token) == False:
            keep_token = False

        if token[0] == '’':
            keep_token = False

        if keep_token:
            tokens_to_keep.append(token[0])
    return tokens_to_keep 

# parsing down list of tuples
#   use grammar to pick
#   or combine into a larger snippet? If so, test that new snippet has all
#	matches the other two did!
#   use shorter (fewer tokens) over longer
#   first if nothing else
#   possibly allow user to choose? 
#   what if three or more match? how algorithm catch?
#
# run through freq dist first so compare only those with same frequency? 
#
# input snippets are tokens (i.e. ('I', 'sing', 'the')
def parse_down_tuples(snippet_tokens):
    snippets = []


    for snippet in snippet_tokens:
        keep_snippet = True

        # word_tokenize parses '’' as a unique token
        # tokenized snippet of 'woman' '’' 's' becomes woman's which is OK
        # but '’' in any other position doesn't form a word
        if len(snippet) == 3:
            if snippet[0] == '’' or snippet[2] == '’':
                keep_snippet = False
        else:
            for token in snippet:
                if token == '’':
                    keep_snippet = False

        # if none of the tokens in the snippet are in the keep pile of 
        #	positional tokens, reject the snippet
        reject_count = 0
        snippet_with_pos_tags = nltk.pos_tag(snippet)
        for t in snippet_with_pos_tags:
            if grammar_parse(t) == False:
                reject_count += 1
        if reject_count == len(snippet_with_pos_tags):
            keep_snippet = False

        if keep_snippet:
            snippets.append(snippet)

    return snippets

# get user input - which functionality to process
def pick_function():
    print ("What do you want to do?")
    print ("1. pick a frequent token")
    print ("2. pick a frequent bigram")
    print ("3. pick a frequent trigram")
    print ("4. pick a frequent bigram or trigram")
    print ("5. enter a search string")
    print ("6. see which tokens return the same lines")
    print ("q to quit")
    
    while True:
        result = input()
        if result.lower() == 'q':
            return None

        try:
            selection = int(result)
        except: 
            print ('enter a number to selecct an option or enter q to quit')
        else:
            if selection >= 1 and selection <=6:
                return selection
            print ('enter a number to selecct an option or enter q to quit')

def print_poem_lines (line_idxs, poem_lines):
    if len(line_idxs):
        for idx in line_idxs:
            print ('\t {0}: {1}'.format(idx, poem_lines[idx]))
        return True
    return False

def print_poem_context(snippet, poem):
    reg_ex = '(' + snippet + ')'

    # JTG: what if char in snippet needs to be escaped?
    reg_ex = '([\s\w]+)' + '(' + snippet + ')' + '([\s\w]+)'

    m = re.search(reg_ex, poem)
    rest_of_poem = poem
    while m:
        #print (m.group(0))
        rest_of_poem = rest_of_poem[m.end():]
        m = re.search(reg_ex, rest_of_poem)

def print_context(poem_tokens, snippet_idx_map, poem_lines, poem):
    fdist_snippets = nltk.FreqDist(poem_tokens)
    snippet = pick_snippet(fdist_snippets.most_common(20))
    if snippet == None:
        return
    lines = snippet_idx_map[snippet]
    if not print_poem_lines(lines, poem_lines):
        print_poem_context(snippet, poem)

# Function variables   
#    poem_json: poem in JSON format 
#	list of dictionary elements
#	dict 'author' -> string with author's name
#	dict 'title' -> string with title
#	dict 'lines' -> list of strings, each list is a line of the poem
#    poem_lines: list of string where each string is a line of the poem
#    poem: whole poem as one single string
#    poem_tokens: list of strings, each string -> word of the poem
#	as returned by nltk.word_tokenize
#    snippet_tokens: list of tuples
#        each tuple ranged from 1 to 3 linguistic units 
#        if multiple linguisting units, they are consecutive in the text
#    fdist_snippets: a frequency distribution of all tokenized snippets 
def quest_for_meaning ():
    poem_json = select_poem ()
    print (poem_json)
    return

    if poem_json:
        poem_lines = poem_json['lines']
        poem = parse_poem_from_json (poem_json)

        # tokens: one linguistic unit (work, punctuation)
        # word_tokenize returns all possible tokens for the input
        poem_tokens = nltk.word_tokenize(poem)
        single_snippets = make_snippets_from_text(poem_tokens)

        # bigram: a group of two consecutive linguistic units
        # nltk returns all possible bigrams for given tokens
        poem_bigrams = list(nltk.bigrams(poem_tokens))
        poem_bigrams = parse_down_tuples(poem_bigrams)
        bigram_snippets = make_snippets(poem_bigrams)

        # trigram: a group of three consecutive linguistic units
        # nltk returns all possible trigrams for given tokens
        poem_trigrams = list(nltk.trigrams(poem_tokens))
        poem_trigrams = parse_down_tuples(poem_trigrams)
        trigram_snippets = make_snippets(poem_trigrams)

        # parse down single-word tokens AFTER used them to create
        # bigrams and trigrams
        poem_tokens = parse_down_tokens(poem_tokens)

        snippets = single_snippets + bigram_snippets + trigram_snippets
        snippet_tokens = poem_tokens + poem_bigrams + poem_trigrams

        # snippets range from 1 to 3 words only because those are
        # easy to generate using NLTK functions
        #snippet_tokens = poem_tokens + poem_bigrams + poem_trigrams 

        snippet_idx_map = get_poem_lines_for_snippets(snippets, poem_lines)
        #print (snippet_idx_map)

        # map functions to index
        selection = pick_function()
        if not selection:
            return
        elif selection == 1:
            print_context(poem_tokens, snippet_idx_map, poem_lines, poem)
        elif selection == 2:
            print_context(poem_bigrams, snippet_idx_map, poem_lines, poem)
        elif selection == 3:
            print_context(poem_trigrams, snippet_idx_map, poem_lines, poem)
        elif selection == 4:
            print_context(poem_trigrams+poem_bigrams, snippet_idx_map, poem_lines, poem)
        elif selection == 5:
            search_str = input("Enter a search string:")
            line_idx = 0
            for line in poem_lines:
                if search_str in line:
                    print ('{0}: {1}'.format(line_idx, line))
                line_idx += 1

# main
#trigrams()
quest_for_meaning ()
