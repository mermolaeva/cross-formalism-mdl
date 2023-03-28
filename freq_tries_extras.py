# from freq_tries_ug import * # is allowed to import UG functions, but doesn't have to
from mdl import read_corpus, corpus_names # TODO: separate into corpus_utils
import json


# pretty-printing; NOT part of any MDL term
def pprint_freq_trie(t):
	pprint_freq_trie_aux(t[1], sep="", inherit="", parent=f'* {t[0]}')


def pprint_freq_trie_aux(d, sep="", inherit="", parent=""):
	print("{}╴{}".format(sep, parent if parent != "" else '*'))
	if isinstance(d, dict):
		for i, key in enumerate(d):
			if i == len(d)-1: pprint_freq_trie_aux(d[key][1], inherit+" └──", inherit+"    ", f'{key} {d[key][0]}')
			else: pprint_freq_trie_aux(d[key][1], inherit+" ├──", inherit+" │  ", f'{key} {d[key][0]}')


# method of obtaining an analysis; NOT part of any MDL term
# convert a list of words into a trie with frequencies
def make_freq_trie(words):
	root = (len(words), dict())
	for word in words:
		current_dict = root[1]
		for letter in word:
			current_val = current_dict.setdefault(letter, [0, {}])
			current_val[0] += 1
			current_dict = current_val[1]
		current_dict.setdefault('#', [0, '#'])[0] += 1
	return root


# obtain an analysis from a given corpus
def corpus_to_freq_trie(corpus_name):
	words = read_corpus(corpus_name)
	freq_trie = make_freq_trie(words)
	with open(f'freq_tries_{corpus_name}.json', 'w') as outfile:
		json.dump(freq_trie, outfile, separators=(',', ':'))


if __name__ == '__main__':
	for n in corpus_names:
		corpus_to_freq_trie(n)