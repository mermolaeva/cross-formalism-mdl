# from tries_ug import * # is allowed to import UG functions, but doesn't have to
from mdl import read_corpus, corpus_names
import json


# pretty-printing; NOT part of any MDL term
def pprint_trie(d, sep="", inherit="", parent=""):
	print("{}╴{}".format(sep, parent if parent != "" else '*'))
	if isinstance(d, dict):
		for i, key in enumerate(d):
			if i == len(d)-1: pprint_trie(d[key], inherit+" └──", inherit+"    ", key)
			else: pprint_trie(d[key], inherit+" ├──", inherit+" │  ", key)


# methods obtaining an analysis; NOT part of any MDL term
# convert a list of words into a trie
def make_trie(words):
	root = dict()
	for word in words:
		current_dict = root
		for letter in word:
			current_dict = current_dict.setdefault(letter, {})
		current_dict['#'] = '#'
	return root


# obtain an analysis from a given corpus
def corpus_to_trie(corpus_name):
	words = read_corpus(corpus_name)
	trie = make_trie(words)
	with open(f'tries_{corpus_name}.json', 'w') as outfile:
		json.dump(trie, outfile, separators=(',', ':'))


if __name__ == '__main__':
	for n in corpus_names:
		corpus_to_trie(n)