# How make tokens in all_tokens lowercase (so "the" equals "The")?  
# JTG: 'as' returns lines for 'has'
# JTG: searching uses regualar expressions. 
#	What if a characer in the snippet needs to be escaped?
# Future: if snippet cross line boundaries, list includes both lines
# store reults to JSON?
# if token is 'd' or 's', remove it

import requests
import nltk
import string
import re
import json
import pandas as pd

# transforms tokens into snippets
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

# takes a list of tokens and generates a list of snippets
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

# allosw the user to choose one snippet from a list
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

# for now, default to I Sing the Body Electric
# To Do:
#	Allow user to enter author and title
#	poetrydb can return multiple poems, allow user to pick one
#	read poem from JSON file (same format as poetrydb.org
def select_poem():
    list_of_poems = []

    # Load Whitman's 'I Sing the Body Electric'
    req = requests.get ('http://poetrydb.org/title/I%20Sing%20the%20Body%20Electric/lines,author,title')
    if req.status_code == 200:
        poems = req.json()
        poem = poems[0]
        list_of_poems.append (poem)

    if len(list_of_poems) == 0:
        return None
    if len(list_of_poems) == 1:
        return list_of_poems[0]

# JTG: for one-word tokens, token can be part of another word
# so if 1-word token, regex -> 'space|punctuaion snippet space|punctuation'
#
# for a set of snippets, create list of index values mapping to the poem
# lines that snippet is found in
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

# keep_tags -> based on grammar type, keep this snippet
# call nltk.help.upenn_tagset('.*') for a complete list of tags
# CD: numeral, cardinal
# FW: foreign word
# JJ: adjective or numeral, ordinal
# JJR: adjective, comparative
# JJS: adjective, superlative
# NN: noun, common, singular or mass
# NNP: noun, proper, singular
# NNPS: noun, proper, plural
# NNS: noun, common, plural
# RB: adverb
# RBR: adverb, comparative
# RBS: adverb, superlative
# RP: particle
# UH: interjection
# VB: verb, base form
# VBD: verb, past tense
# VBG: verb, present participle or gerund
# VBN: verb, past participle
# VBP: verb, present tense, not 3rd person singular
# VBZ: verb, present tense, 3rd person singular
#
# don't keep to be verbs
#
# remove tokens based on grammar
def grammar_parse(token):
    # keep snippets if tokens have these tags
    keep_tags = ['CD', 'FW', 'JJ', 'JJR', 'JJS',  'NN', 'NNP', 'NNPS', 'NNS',  'RB', 'RBR', 'RBS',  'RP', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBZ']
    to_be_verbs = ['am', 'are', 'is', 'was', 'were']

    if token[1] not in keep_tags:
        return False
    if token[0] in to_be_verbs:
        return False
    return True

# removing tokens
def parse_down_tokens(tokens):
    tokens_to_keep = []
    tagged_tokens = nltk.pos_tag(tokens)
    for token in tagged_tokens:
        keep_token = True

        # JTG: the grammar_parse may remove these
        if token[0] in string.punctuation:
            keep_token = False

        if grammar_parse(token) == False:
            keep_token = False

        # part of apostrophe issue with word tokenizer function
        if token[0] == '’':
            keep_token = False

        # part of apostrophe issue with word tokenizer function
        if token[0] == 's' or token[0] == 'd':
            keep_token = False

        if keep_token == True:
            tokens_to_keep.append(token[0])
    return tokens_to_keep 

# remove tokens
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
            if snippet[0] == 's' or snippet[2] == 's':
                keep_snippet = False
            if snippet[0] == 'd' or snippet[2] == 'd':
                keep_snippet = False
        else:
            for token in snippet:
                if token == '’':
                    keep_snippet = False
                if token == 's':
                    keep_snippet = False
                if token == 'd':
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
    print()
    print ("What do you want to do?")
    print ("1. pick a frequent token")
    print ("2. pick a frequent bigram")
    print ("3. pick a frequent trigram")
    print ("4. pick a frequent bigram or trigram")
    print ("5. enter a search string as a regular expression")
    print ("6. store tokens that return the same lines to a file to a file")
    print ("7. store frequency distributions for each snippet")
    #print ("8. parse down tokens that return the same lines")
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
            if selection >= 1 and selection <=7:
                return selection
            print ('enter a number to selecct an option or enter q to quit')

# for each index in line_idxs, print its corresponding line in the poem
def print_poem_lines (line_idxs, poem_lines):
    if len(line_idxs):
        for idx in line_idxs:
            print ('\t {0}: {1}'.format(idx, poem_lines[idx]))
        return True
    return False

# use a regular expression to print context (surrouding text) for a snippet
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

# write the frequency distribution of each token to a file
def store_snippet_freqdist(tokens):
    fdist_snippets = nltk.FreqDist(tokens)
    most_common = fdist_snippets.most_common(len(fdist_snippets))

    dist_list = []
    for dist in most_common:
        l = [make_snippet(dist[0]), dist[1]]
        dist_list.append(l)
    distDF = pd.DataFrame(dist_list)
    distDF.rename(columns={0:'Snippet', 1:'Frequency Distribution'}, inplace=True)
    pd.set_option('display.max_rows', len(dist_list))
    f_out = open("freqdist.txt", 'w')
    print (distDF, file=f_out)

    print('frequency distribution printed to freqdist.txt')

# allow user to select a snippet
# if snippet_idx_map has line indices for that snippet, print the 
# corresponding lines
# else print the context (surrounding text) of that snippet
def print_context(poem_tokens, snippet_idx_map, poem_lines, poem):
    fdist_snippets = nltk.FreqDist(poem_tokens)
    snippet = pick_snippet(fdist_snippets.most_common(20))
    if snippet == None:
        return
    lines = snippet_idx_map[snippet]
    if not print_poem_lines(lines, poem_lines):
        print_poem_context(snippet, poem)

# find all snippets that appear on the same lines
# O(n-squared)
def find_all_snippets_on_same_lines(snippet_idx_map):
    # list of lists
    # each sublist contains matching snippets
    all_matches = []

    local_match = []

    for outer_map in snippet_idx_map:
        if len(local_match) > 1:
            if local_match not in all_matches:
                all_matches.append(local_match)
        local_match = []
        for inner_map in snippet_idx_map:
            # if index lists match
            if snippet_idx_map[outer_map] == snippet_idx_map[inner_map]:
                if inner_map not in local_match:
                    local_match.append(inner_map)
    return all_matches

# Interested if two ore more snippets appear on the same, 
# and only the same lines. If they do, store to a JSON file. 
def store_snippets_on_same_lines(snippet_idx_map):
    all_matches = find_all_snippets_on_same_lines(snippet_idx_map)

    f_out= open('matching_tokens.txt', 'w')
    for matches in all_matches:
        print(matches, file=f_out)
    f_out.close()

    f_out = open('matching_tokens_json.txt', 'w')
    print(json.dumps(all_matches), file=f_out)
    f_out.close()

    print ('snippets from same line output to matching_tokens.txt and matching_tokens_json.txt')

# JTG: Future functionality
# of all snippets that appear on the same lines, keep longest snippet
# nope: need poem_tokens, poem_bigrams, or poem_trigrams because
#   those are variables frequency dist is calculated on
#   would wantot make class OO for access to variables
def parse_down_snippets_on_same_lines(snippet_idx_map, snippets):
    all_matches = find_all_snippets_on_same_lines(snippet_idx_map)
    removes = []

    for matches in all_matches:
        longest = ''
        for snippet in matches:
            if len(snippet) > len(longest):
                if len(longest):
                    removes.append(longest)
                longest = snippet
            elif len(longest) > len(snippet):
                    removes.append(snippet)
    for snippet in removes:
        snippets.remove(snippet)       
        snippet_idx_map.pop(snippet)

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
# main driving function of the application
def quest_for_meaning ():

    # get a poem
    poem_json = select_poem ()

    if poem_json:
        # initialize variables

        poem_lines = poem_json['lines']
        poem = parse_poem_from_json (poem_json)

        # tokens: one linguistic unit (work, punctuation)
        # word_tokenize returns all possible tokens for the input
        poem_tokens = nltk.word_tokenize(poem)

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

        # snippets range from 1 to 3 words only because those are
        # easy to generate using NLTK functions
        snippets = poem_tokens + bigram_snippets + trigram_snippets

        snippet_idx_map = get_poem_lines_for_snippets(snippets, poem_lines)

        while True:
            # JTG: map functions to index
            # allow user to select action
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
            elif selection == 6:
                store_snippets_on_same_lines(snippet_idx_map)
            elif selection == 7:
                store_snippet_freqdist(poem_tokens+poem_bigrams+poem_trigrams)
            #elif selection == 8:
                #parse_down_snippets_on_same_lines(snippet_idx_map, snippets)

# main
quest_for_meaning ()
