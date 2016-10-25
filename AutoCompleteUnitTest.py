#!/usr/bin/python

"""
The following unittest is for my my implementation of Autocomplete using a 
trie, a tree data structure that efficiently allows you to look up terms based 
on their prefixes. The Autocomplete algorithm  is the process of finding words 
in a dictionary that starts with a given prefix. The goal of Autocomplete is 
to make this process extremely fast, thus performing a trie traversal is 
necessary. For this project,  relevance of each word is based on the frequency 
of which it appears in the dictionary. The class Trie represents my 
implementation of the Trie data structure. Each node is given 4 instances, 
the children, the maximum weight of its children, and if the node is the end 
of a word, the word itself and the weight of that word. The function insert() 
takes input and adds it to the tree where each node consists of one character. 
The function find_subtrie() find the subtrie starting at the root node of the 
given prefix. Lastly topk() returns a list of weight and word values of the 
top k matches to the provided prefix sorted by weight. For my unittests, I 
used files pokemon.txt.
"""

from AutoComplete import Trie, read
import unittest
import random
import string


class TrieTest(unittest.TestCase):

	#Test method topk

	def testTrieMethodMatchesForPokemonText(self):
		"""Test if Trie algorithm suggestions matches an iterative search for 
		the pokemon.txt file."""
		root = read("pokemon.txt")
		search_Ch = root.topk(5, "Ch")
		search_Du = root.topk(4, "Du")
		wordlist=[]
		with open("pokemon.txt", 'r') as file:
			next(file)
			for line in file:
				if (line.rstrip('\n')):
					weight = int(line.split(None,1)[0])
					word = str(line.split(None,1)[1].strip())
					wordlist.append((word, weight))
				else:
					break
		wordlist_prefix1 = [word for word in wordlist if word[0].startswith("Ch")][:5]
		wordlist_prefix2 = [word for word in wordlist if word[0].startswith("Du")][:4]
		self.assertEqual(search_Ch, wordlist_prefix1)
		self.assertEqual(search_Du, wordlist_prefix2)

	def testTopKvaluesIsSorted(self):
		"""Test if return values are sorted."""
		root = read("pokemon.txt")
		search_Char = root.topk(5, "Char")
		search_Bo = root.topk(5, "Bo")
		self.assertEqual(search_Char, sorted(search_Char, key = lambda x: x[1], reverse = True))
		self.assertEqual(search_Bo, sorted(search_Bo, key = lambda x: x[1], reverse = True))

	def testTopKLengthIsCorrect(self):
		"""Test if topk() returns array of length k when there is enough words 
		in dictionary."""
		root = read("pokemon.txt")
		search_Char = root.topk(3, "Char")
		search_B = root.topk(6, "B")
		self.assertEqual(len(search_Char), 3)
		self.assertEqual(len(search_B), 6)

	def testTopKLengthIsCorrectForLargeK(self):
		"""Test if topk() returns list of length less than k when there is not 
		enough words in dictionary."""
		root = read("pokemon.txt")
		search_Char = root.topk(20, "Char")
		search_B = root.topk(500, "B")
		self.assertTrue(len(search_Char)<=20)
		self.assertTrue(len(search_B)<=500)

	def testInvalidPrefix(self):
		"""Test that topk() returns empty list when the prefix is invalid."""
		root = read("pokemon.txt")
		search_Charmonger = root.topk(2, "Charmonger")
		self.assertEqual(search_Charmonger, [])

	def testTopKSortsByWeightForNodesOnSameBranch(self):
		"""Test that topk() returns the word of maximum weight first if 2 or 
		more words are on the same branch, instead of the parent node which 
		also has the same maximum child_weight but lesser weight."""
		root=Trie()
		root.insert(5, "big", "big")
		root.insert(10, "biggest", "biggest")
		root.insert(20, "bigO", "bigO")
		root.insert(3, "don", "don")
		root.insert(4, "donald", "donald")
		search_big = root.topk(3, "big")
		search_don = root.topk(2, "don")
		self.assertEqual( search_big, [("bigO", 20), ("biggest", 10), ("big", 5)])
		self.assertEqual(search_don, [("donald", 4), ("don", 3)])

	#Test method insert

	def testInsertFunctionsCorrectly(self):
		"""Test if insert correctly adds children  to the root node, in which 
		children of the same character belong in one node."""
		root = Trie()
		root.insert(5, "big", "big")
		root.insert(4, "brag", "brag")
		root.insert(3, "donald", "donald")
		root.insert(1, "hillary", "hillary")
		self.assertEqual(len(root.children), 3)

	def testMaxchildweightOnInsert(self):
		"""Test if the root node has maxmimum weight of all inserted words."""
		root = Trie()
		root.insert(270, "donald", "donald")
		root.insert(270, "hillary", "hillary")
		root.insert(538, "president", "president")
		self.assertEqual(root.child_weight, 538)

	#Test method find_subtrie

	def testSubtrieOnExisitingWord(self):
		"""Test that if the instance word and weight of the subtree node 
		exists, it is equal to the inserted word and weight to the original 
		trie."""
		root = Trie()
		root.insert(20, "hillary", "hillary")
		root.insert(10, "hill", "hill")
		subtrie = root.find_subtrie("hill")
		self.assertEqual(subtrie.word_name, "hill")
		self.assertEqual(subtrie.weight, 10)

	def testSubtrieOnNonExistingWord(self):
		"""Test that the instance word and weight on the subtree node is None 
		and -inf if the prefix is not contained in the original trie."""
		root = Trie()
		root.insert(20, "donald", "donald")
		root.insert(10, "trump", "trump")
		subtrie = root.find_subtrie("don")
		self.assertIsNone(subtrie.word_name)
		self.assertEqual(subtrie.weight, -float('inf'))

	def testSubtrieIsNoneTypeIfPrefixIsInvalid(self):
		"""Test that invalid prefix returns a NoneType in find_subtrie."""
		root = Trie()
		root.insert(270, "donald", "donald")
		root.insert(270, "hillary", "hillary")
		root.insert(538, "president", "president")
		subtrie = root.find_subtrie("press")
		self.assertIsNone(subtrie)

	def testSubtrieHasCorrectChildren(self):
		"""Test that the subtrie has the correct children given the following 
		inputs."""
		root = Trie()
		root.insert(1, "apple", "apple")
		root.insert(2, "apes", "apes")
		root.insert(3, "apiary", "apiary")
		subtrie = root.find_subtrie("ap")
		self.assertTrue(sorted(list(subtrie.children.keys()))==sorted(["p", "e", "i"]))

	# Randomized Tests for correctness

	def testTrieMethodMatchesForRandomInput(self):
		"""Test if iterative approach of autocomplete matches my trie 
		implementation using  a random list of weights and words. This 
		shouldn't work on all unittest runs since some words may have the same
		weight and thus there is a chance that it may not make the top N 
		suggestion due to sorting issues."""
		root=Trie()
		wordlist=[]
		for _ in range(2500):
			weight = random.randint(1, 360)
			RandomWord = ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(3, 10)))
			wordlist.append((RandomWord, weight))
			root.insert(weight, RandomWord, RandomWord)

		wordlist = sorted(wordlist, key = lambda x: x[1], reverse = True)
		wordlist_prefix1 = [word for word in wordlist if word[0].startswith("b")][:5]
		wordlist_prefix2 = [word for word in wordlist if word[0].startswith("ji")][:3]
		wordlist_prefix3 = [word for word in wordlist if word[0].startswith("jon")][:5]
		self.assertEqual(root.topk(5, "b"), wordlist_prefix1)
		self.assertEqual(root.topk(3, "ji"), wordlist_prefix2)
		self.assertEqual(root.topk(5, "jon"), wordlist_prefix3)

	def testPrefixIsShorterThanSuggestedWords(self):
		"""Test on random input that autocomplete suggestions are longer than or of equal length of the prefix."""
		root=Trie()
		for _ in range(2500):
			weight = random.randint(1, 250)
			RandomWord = ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(3, 20)))
			root.insert(weight, RandomWord, RandomWord)
		self.assertTrue(all(len(word[0]) >= 2 for word in root.topk(10, "br")))
		self.assertTrue(all(len(word[0]) >= 3 for word in root.topk(10, "amw")))


	def testPrefixBeginsAllSuggestedWords(self):
		"""Test that the suggested words begin with the prefix."""
		root=Trie()
		for _ in range(2500):
			weight = random.randint(1, 250)
			RandomWord = ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(3, 10)))
			root.insert(weight, RandomWord, RandomWord)
		self.assertTrue(all(word[0].startswith("br") for word in root.topk(10, "br")))

if __name__ == "__main__":
    unittest.main()