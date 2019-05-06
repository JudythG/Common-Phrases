# Common-Phrases
Use NLTK to search for meaningful phrases and words in poems. 
My driving question is this: how much can we automate the serach for meaning in poetry? 
I defined meaningful words or phrases as
* By frequency of the word / phrase: More frequent words / phrases are considred more meaningful. 
* Grammar: nouns, verbs, adjectives, and adverbs are considred meaningful. Words such as 'the' or 'and' are not. 

In coding this program, I was exploring NLTK's functions. This program uses:
* word_tokenize() to generate 1-word tokens
* bigrams() to generate 2-word tokens
* trigrams() to generate 3-word tokens
* FreqDist () to calculate the frequency of tokens in the text and sort those tokens by that frequency
* pos_tag() to generate grammar type for each token in the poem

## Variables
### Variables Relating to the Poem as a Whole
#### poem_json
The poem - Walt Whitman's 'I Sing the Body Electric' - was imported from [The Poetry DB](http://poetrydb.org). The format of the poem coresponds to the value returned by the Poetry DB API. 

The dictionary format contains three elements:
1. title key maps to a string, the title of the poem
2. author key maps to a string, the author of the poem
3. list key maps to a list of strings, each list is a line of the poem

#### poem_lines
A list of strings where each string is a line of the poem.

#### poem
The whole poem as one single string. 

#### snippets
List of strings where each string is a snippet (1 to 3 word phrase) in the poem. 

#### snippet_idx_map
For each value in snippets, stores a list of numbers, the lines of the poem where that token can be found. 
Dict where the key is a snippet string and the value is a list of index numbers that indicate the lines where that snippet can be found in the poem.

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

Tasks 1 - 5 allow the user to pick or enter a snippet and then display all the poem lines that contain that snippet. The tasks mostly differ on the type of snippet (1-word, 2-words, 3-words, 2- and 3-words, user-entered word).

Task 6 stores snippets which are on the same lines of the poem, and only the same lines of the poem, to an output file. For example, the following are all snippets from the first line of the poem: ['electric', 'SING the', 'Body electric', 'electric;', 'SING the Body', 'the Body electric', 'Body electric;']. Currently the data is stored to two output files:
1. matching_tokens.txt for readability
2. matching_tokens_json.txt a JSON file

Task 7 stores a frequency distribution of each snippet to an output file: freqdist.txt

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
### Driving Function / main
#### quest_for_meaning()
The main driving function. 
* Calls select_poem () to get a poem to process.
* Initializes poem_lines, poem, poem_tokens, bigram_tokens, and trigram_tokens. After removing non-meaningful tokens from poem_tokens, bigram_tokens, and trigram_tokens, creates bigram_snippets, trigram_snippets, snippets, and snippet_idx_map. Allows the user to pick a task and calls the corresponding function. 
* Tasks 1 - 4 ask the user to pick a 1-word snippet, a 2-word snippet, a 3-word snippet, and a 2- or 3-word snippet respectivley. Each line that snippet appears in is displayed to the terminal.
* Task 5 asks the user to enter a regular expression. Each line that regex appears in is displayed to the terminal. 

### Functions That Set-up the Initial Variables
#### parse_poem_from_json(poem_dict)
Takes the input form of the poem, a dictionary, and returns a string that contains the text of the poem. 

#### get_poem_lines_for_snippets(snippet_tokens, poem_lines)
Input: 
* all snippets stored in a list of strings
* all the lines of the poem as a list of strings

Creates a mapping between snippets and the indexes to the poem lines they appear in. 

#### find_all_snippets_on_same_lines(snippet_idx_map)
Each set of snippets that appear on the same lines of the poem are stored in a list. Returns a list of all of these lists. 



### Input Functions
#### select_poem()
For now, returns Walt Whitman's 'I SIng the Body Electric'. Future development will allow the user to select a poem.

#### pick_function ()
allows the user to decide what to do

#### pick_snippet(snippets)
Given a list of snippets, the user selects one

### Functions to Reduce Number of Snippets
#### parse_down_tuples(n-grams)
Rejects snippets (lists of tuples (bigrams or trigrams))

#### parse_down_tokens(tokens)
Rejects snippets (lists of strings)

#### grammar_parse(token)
Removes or keeps snippets based on the grammar type of tokens. For example, a 1-word token that is punctuation would be removed but a 1-word noun kept. Removes 'be verb' tokens. 

### Functions that Generate Snippets
#### make_snippet(tokens)
If 1-word string, return it. For a tokenized string, put spaces between each token unless the preceeding token is punctuation. For example tokens: ',' 'the' and 'Soul' would form the snippet ", the Soul"

#### make_snippets(list_of_tokens)
Calls make_snippet () on each token in the list of tokens, appends the resulting snippets to a list of strings, and returns the list of snippets. 

#### get_poem_lines_for_snippets(snippets, poem_lines)
snippets are 1 - 3 words snippets (lists of strings)
poem_lines have all lines of the poem in lists of strings
for each snippet, store the indices of each line it appears in

### Output Functions
#### print_poem_lines(line_idxs, poem_lines)
For each index value in line_idxs, print its corresponding line in poem_lines

#### print_poem_context(snippet, poem)
Not all snippets correspond to one line in the poem. Some snippets cross line boundaries. For those snippets, use a regular expression to find that snippet's context (surrounding text) and display it. 

#### store_snippet_freqdist(tokens)
Use NLTK's FreqDist to determine the frequency distribution of each snippet. Store them to a file, freqdist.txt, from most to least frequent. 

#### print_context(tokens, snippet_idx_map, poem_lines, poem)
tokens input are list of strings or list of tuples (bigrams or trigrams)
snippet_idx_map stores list of lines snippet appears in for each snippet
poem_lines: all the lines of the poem as a list of strings
poem: whole poem as one string

User selects a token. If snippet_idx_map's list of indices is not empty, use poem_lines and indices to display lines of the poem. If list of indices is empty - happens if the snippet crosses a poem line - uses regular expressions to search the poem and print some of the surrounding context of the snippet. 

#### store_snippets_on_same_line(snippet_idx_map)
Any snippets that appear on the same line are stored into a list. Writes each of these lists of snippets to two output files:
1. matching_tokens.txt - human readable
2. matching_tokens_json.txt - JSON file
