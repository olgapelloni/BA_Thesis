The project is aimed to extract and classify rhymes from the poetic corpus of RNC with regard of further usage in Neo4j graph database. 
Project consists of a Python package pre_editing and two programs -- transcribe.py and rhymes.py.

------------------------------------------------------------------------------------------------------------------------------------------
STRUCTURE
------------------------------------------------------------------------------------------------------------------------------------------

The main program is rhymes.py. 
Input: path to the folder with xml files from the corpus.
Output: csv table with rhymes and their classification; database of rhymes in Neo4j (optional).

Inside the rhymes.py the program transcribe.py is executed.
Input: Russian word written with an accent sign.
Output: transcription of the word.

The program transcribe.py uses package pre_editing.
In the file __init__.py of the package the rules for transcribing in Russian are described. 
The file yo_list.txt is used here to match words which require substitution of the stressed vowel [e] to [o].
The accents in words is a crucial prerequisite for using the program.

------------------------------------------------------------------------------------------------------------------------------------------
USAGE
------------------------------------------------------------------------------------------------------------------------------------------
The program rhymes.py should be run from Python IDLE or any other Python environment.
In the line 346 change the path to the folder with input files if needed: rhymes.root_name = '.\\xx'
The folder should content the files from the poetic corpus of RNC in its original format.
Press Run, the program will print the amount of files to be parsed. During the work of the program, the rhymes will be
extracted and classified by 8 parameters: open or closed, exact or inexact, degree of exactness 
(the smaller the number, the more exact the rhyme), rich or poor, deep or not, assonance rhymes, dissonance rhymes,
rhyming type (paired, crossed, encircling), position of accent (male, female, dactyl, hyperdactyl), meter1 and meter2.
Each new pair of rhymes will be recorded into the file parsed.csv as well as will be printed. After each parsed document
there will be information about the amount of documents already parsed and their percentage.
If you want to simultaniously build a Neo4j database you should: install Neo4j, run server, uncomment all the lines needed for
writing new nodes and edges (they are all preceded with such a comment) and adjust authenticate information if needed.













