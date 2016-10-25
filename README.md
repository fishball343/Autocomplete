# AutoComplete

I ran the following script on the Movies file. And did profiling to find the runtimes. I compiled the cumulative time for the functions insert() and topk(). 

python -m cProfile -s time AutoComplete.py Star movies.txt 24

-- It took 28.143 seconds to run the function insert() to build the trie with movies.txt inputs. 
-- It took 0.011 seconds to find the 24 movies that started with Star using the topk() function

To see how my performance scales with the number of words returned, I used the following scripts below. 

python -m cProfile -s time AutoComplete.py Star movies.txt 4

-- It took 28.468 seconds to run the function insert() to build the trie with movies.txt inputs. 
-- It took 0.002 seconds to find the 4 movies that started with Star using the topk() function. 

python -m cProfile -s time AutoComplete.py Star movies.txt 8

-- It took 28.101 seconds to add all the entries into the TRIE and build the tree
-- It took 0.004 seconds to find the 8 movies that started with Star

python -m cProfile -s time AutoComplete.py Star movies.txt 12

-- It took 28.151 seconds to add all the entries into the TRIE and build the tree
-- It took 0.007 seconds to find the 12 movies that started with Star

python -m cProfile -s time AutoComplete.py Star movies.txt 2000 //note only searched 294 entries 

-- It took 28,458 seconds to add all the entries into the TRIE and build the tree
-- It took 0.352 seconds to find the 294 movies that started with Star

Thus it appears that the time to add all the entries into the trie node is constant in relation to the number of words we are searching for. This makes sense since we are adding each line in movies.txt to the trie and the size of movies.txt does not change for the number of words we are looking for. 

It appears that the time to find the entries starting with a given prefix increases as the number of words we are searching for increases. This makes sense since we will have to traverse through more nodes in the trie to get all of the values. Since the runtime of this algorithm is nlog(n) where n is the number of words we need to search for, increasing n will defintely affect runtime as shown in our above examples. 

The slowest part of my code is adding each word and its respective weight into the trie data structure. I cannot think of anyway to improve this part of my code since the only way to read lines in python is to do so iteratively. Adding all values to the trie takes nlog(n) time and this is the fastest it can get with a Trie implementation. 

The fastest part of my code is finding the top k entries that start with the prefix. My code runs almost instantly, so I don't think I will need to make changes.

EXTRA NOTES:

To run the unittest type **python AutoCompleteUnitTest.py** into the command line. 

To run the AutoComplete algorithm, type the first argument as the prefix string, the second argument as the file that displays the words and the third argument as the number of words you want the algorithm to suggest

eg. python **AutoComplete.py Ch pokemon.txt 5**

If the prefix does not exist in the dictionary of words, my code should print "Prefix not found" on the console. 






