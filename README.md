# Common-Phrases
Use NLTK to search for meaningful phrases and words in poems. 
My driving question is this: how much can we automate the serach for meaning in poetry? 
I defined meaningful words or phrases as
* By frequency of the word / phrase: More frequent words / phrases are considred more meaningful. 
* Grammar: nouns, verbs, adjectives, and adverbs are considred meaningful. Words such as 'the' or 'and' are not. 

## Variables
### Variables Relating to the Poem as a Whole
#### poem_json
The poem - Walt Whitman's 'Leaves of Grass' - was imported from [The Poetry DB](http://poetrydb.org). The format of the poem coresponds to the value returned by the Poetry DB API. 

The dictionary format contains three elements:
1. title key maps to a string, the title of the poem
2. author key maps to a string, the author of the poem
3. list key maps to a list of strings, each list is a line of the poem

#### poem_lines
A list of strings where each string is a line of the poem.

#### poem
The whole poem as one single string. 

#### snippets
Every meaningful token, as a string, in the poem. All the values in poem_tokens, bigram_snippets, and trigram_snippets after they were parsed down. 

#### snippet_idx_map
For each value in snippets, stores a list of numbers, the lines of the poem where that token can be found. 

### Variables Relating to 1-Word Tokens
#### poem_tokens
poem_tokens, a list of string tokens, starts with each word of the poem as a token. Parsing later removes the non-meaningful tokens. Generated using NLTK's word_tokenize function. 

### Variables Relating to 2-Word Tokens
#### poem_bigrams
A list of tuples where each tuple is a bigram from the poem. Starts with all bigrams represented but is parsed down to remove non-meaningful bigrams. Generated using NLTK's bigrams function. 

#### bigram_snippets
A list of strings where each string is a two-word token. Basically poem_bigrams as strings rather than tuples.

### Variables Relating to 3-Word Tokens
#### poem_trigrams
A list of tuples where each tuple is a trigram from the poem. Starts with all trigrams represented but is parsed down to remove non-meaningful trigrams. Generated using NLTK's trigrams function. 

#### trigram_snippets
A list of strings where each string is a three-word token. Basically poem_trigrams as strings rather than tuples.

## Functionality
### Overview
Get the poem from the Poetry DB API. Initialize variables. Remove the non-meaningful tokens from the lists of tokens. Create snippets for all meaningful tokens. For each snippet, store the lines it appears on in the poem. Allow the user to pick a task. 
Tasks 1 - 5 allow the user to pick or enter a snippet and then display all the poem lines that contain that snippet. 

### Removing non-meaningful Tokens
For 1-word tokens:
* If the token is punctuation, it's removed.
* Remove tokens based on grammar

For 2- or 3- word tokens:
* word_tokenizes the apostrophe as a unique token so "woman's" becomes three tokens: "woman", "'", and "s". Reject tokens that fit this pattern. 
* If all the tokens in a snippet fail the grammar parse, reject the snippet

### Removing Tokens Based on Grammar
keep_tags identify grammar elements to keep; see the code for this list of grammar elements 
to_be_verbs identify tokens to reject (am, are, is, was, were)

Uses NLTK's pos_tag() function to determine grammar element of each token.

## Functions
### quest_for_meaning()
The main driving function. 
* Calls select_poem () to get a poem to process.
* Initializes poem_lines, poem, poem_tokens, bigram_tokens, and trigram_tokens. After removing non-meaningful tokens from poem_tokens, bigram_tokens, and trigram_tokens, creates bigram_snippets, trigram_snippets, snippets, and snippet_idx_map. Allows the user to pick a task and calls the corresponding function. 
* Tasks 1 - 4 ask the user to pick a 1-word snippet, a 2-word snippet, a 3-word snippet, and a 2- or 3-word snippet respectivley. Each line that snippet appears in is displayed to the terminal.
* Task 5 asks the user to enter a regular expression. Each line that regex appears in is displayed to the terminal. 

### select_poem()
For now, returns Walt Whitman's 'Leaves of Grass'. Future development will allow the user to select a poem.

### parse_down_tuples(n-grams)
Rejects snippets (lists of tuples (bigrams or trigrams))

### parse_down_tokens(tokens)
Rejects snippets (lists of strings)

#### get_poem_lines_for_snippets(snippets, poem_lines)
snippets are 1 - 3 words snippets (lists of strings)
poem_lines have all lines of the poem in lists of strings
for each snippet, store the indices of each line it appears in

### pick_function ()
allows the user to decide what to do

### print_context(tokens, snippet_idx_map, poem_lines, poem)
tokens -> list of strings or list of tuples (bigrams or trigrams)
snippet_idx_map stores list of lines snippet appears in for each snippet
poem_lines: all the lines of the poem as a list of strings
poem: whole poem as one string

User selects a token. If snippet_idx_map's list of indices is not empty, use poem_lines and indices to display lines of the poem. If list of indices is empty - happens if the snippet crosses a poem line - uses regular expressions to search the poem and print some of the surrounding context of the snippet. 
