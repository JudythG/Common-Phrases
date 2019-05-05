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
