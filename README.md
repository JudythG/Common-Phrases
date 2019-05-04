# Common-Phrases
Use NLTK to search for meaningful phrases and words in poems. 
My driving question is this: how much can we automate the serach for meaning in poetry? 
I defined meaningful words or phrases as
* By frequency of the word / phrase: More frequent words / phrases are considred more meaningful. 
* Grammar: nouns, verbs, adjectives, and adverbs are considred meaningful. Words such as 'the' or 'and' are not. 

## Data Structures
### poem_json
The poem - Walt Whitman's 'Leaves of Grass' - was imported from [The Poetry DB](http://poetrydb.org). The format of the poem coresponds to the value returned by the Poetry DB API. 

The dictionary format contains three elements:
1. title key maps to a string, the title of the poem
2. author key maps to a string, the author of the poem
3. list key maps to a list of strings, each list is a line of the poem
