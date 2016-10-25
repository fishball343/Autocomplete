#!/usr/bin/env python
"""
The following code is my implementation of Autocomplete using a trie, a tree 
data structure that efficiently allows you to look up terms based on their 
prefixes. The Autocomplete algorithm is the process of finding words in a 
dictionary that starts with a given prefix. The goal of Autocomplete is to 
make this process extremely fast, thus performing a trie traversal is 
necessary. For this project, relevance of each word is based on the frequency 
of which it appears in the dictionary. The class Trie represents my 
implementation of the Trie data structure. Each node is given 4 instances, the 
children,  the maximum weight of its children, and if the node is the end of a 
word, the word itself and the weight of that word. The function insert() takes 
input and adds it to the tree where each node consists of one character. The 
function find_subtrie() find the subtrie starting at the root node of the 
given prefix. Lastly topk() returns a list of weight and word values of the 
top k matches to the provided prefix sorted by weight. 
"""

import sys
from Queue import PriorityQueue
import cProfile


class Trie:

	def __init__(self):
		self.children = {}	
		self.word_name = None
		self.weight = -float('inf') 
		self.child_weight = -float('inf') 

	def insert(self, weight, word, constant):
		"""
		The function insert() adds a word and its respective weight to the 
		trie. It also updates the weights and the maximum weight of the 
		children for each node. Lastly it delineates which nodes that end the 
		word by setting the instance self.word_name to the word itself. 
		Essentially, this function recursively adds nodes to the trie. The 
		base case occurs when the length of the word is equal to 0, during 
		which we update the weight and the word_name of that node, signaling 
		that this node represents a word from the dictionary.
		"""

		# Base case set the instance word_name and weight to be the values 
		# provided. Update the child weights accordingly.
		if len(word) == 0:
			self.word_name = constant
			self.weight = max(self.weight, weight)
			if (self.child_weight < self.weight):
				self.child_weight = self.weight
			return

		# Key is the first character of the word. rest is the remaining 
		# characters of the word.
		key = word[0]
		rest = word[1:]

		# Update the max child_weight of each node if the newly encountered 
		# word has a greater weight.
		if (weight > self.child_weight):
			self.child_weight = weight

		# Recursively insert the rest of the word into the Trie. If the next 
		# character is not a current child, then create new node and add to 
		# the trie. 
		if self.children.has_key(key):
			self.children[key].insert(weight, rest, constant)
		else:
			node = Trie()
			self.children[key] = node
			node.insert(weight, rest, constant)

	def find_subtrie(self, prefix):
		"""
		The function find_subtrie() recursively find the subtrie starting at 
		the last node of the prefix. If the prefix is not found then we return 
		NoneType.
		"""

		# Base case when the prefix is of length 0, thus we have reached the
		# end of the prefix. 
		if len(prefix) == 0:
			return self

		# Key is the first character of the prefix. rest is the remaining
		# characters of the prefix.
		key = prefix[0]
		rest = prefix[1:]

		# If the children contain the next character of the prefix, then we
		# traverse to that child and recurse on that node. Otherwise, we will
		# return a NoneType to indicate that the prefix is not found in the
		# trie.
		if (self.children.has_key(key)):
			subtrie = self.children[key]
			return(subtrie.find_subtrie(rest))

		else:
			return

	def topk(self, k, prefix):
		"""
		To find the top k matches, we will first access the subtrie and root
		node of the prefix. Then we will add all the children of the root node
		into a priority queue sorted by negative max child_weight. Our 
		implementation will iteratively pop the node with the "largest" weight 
		from the priority queue and add all children of that node to the 
		priority queue. If the popped node ends a valid word indicated by the 
		instance word_name not being a NoneType, we will add that word and its 
		weight to a sorted list of visited nodes. Once this list has k words 
		with weight greater than the largest child_weight in the priority 
		queue, we will return the visited list as our k suggestions and end 
		our function. We will also stop our algorithm if the priority queue is 
		empty, signalling that we have exhausted all nodes of the subtrie. 
		"""
		
		# Initialize variables and priority queue.
		pq = PriorityQueue()
		visited = []
		isVisited_K = False
		subtrie = self.find_subtrie(prefix)

		# If the subtrie is not None, this indicates that our prefix is valid. 
		if subtrie is not None:
			pq.put((-subtrie.child_weight, subtrie))
			while(isVisited_K == False):
				if pq.qsize() == 0:
					return visited

				top = pq.get()
				top_node = top[1]
				top_weight = top[0]
				for i in top_node.children.values():
				 	pq.put((-i.child_weight, i))
				if top_node.word_name is not None:
					visited.append((top_node.word_name, top_node.weight))
					visited = sorted(visited, key = lambda x: x[1], reverse = True)
					if sum(node >= top_weight for node in visited) >= k:
						visited = visited[:k]
						isVisited_K = True
			return(visited)

		# If the prefix is not found in the subtrie, return an empty visited 
		# list.
		else:
			return []

def read(filename):
	"""
	Parse file input into weights and string values of the word. Then insert 
	each word and weight into the trie. This step takes the longest time since 
	we are iteratively adding every entry into the trie.
	"""
	root=Trie()
	with open(filename, 'r') as file:
	     next(file)
	     for line in file:
	        if (line.rstrip('\n')):
	             weight=int(line.split(None, 1)[0])
	             word=str(line.split(None, 1)[1].strip())
	             root.insert(weight, word, word)
	        else:
	            break
	return root

def printlist(suggestions):
	"""Print the suggestions line by line to facilitate reading the results"""
	if len(suggestions) == 0:
		print("Prefix not found")
	for i in range(len(suggestions)):
		print str(i+1) + ": " + "weight: " + str(suggestions[i][1]) + "\t" + "word: " + suggestions[i][0]

def main():
    word = str(sys.argv[1])
    inFile = str(sys.argv[2])
    topk_suggestions = int(sys.argv[3])
    assert topk_suggestions > 0, "k is not an positive integer: %r" % topk_suggestions
    root = read(inFile)
    searched_list = root.topk(topk_suggestions, word)
    printlist(searched_list)

if __name__ == "__main__":
    main()