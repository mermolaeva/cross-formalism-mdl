# from tries_ug import * # is allowed to import UG functions, but doesn't have to
from mdl import read_corpus, corpus_names
import json


# obtain an analysis from a given corpus
def get_alphabet(corpus_name):
	words = read_corpus(corpus_name)
	alphabet = list(set(''.join(words)))
	with open(f'promiscuous_{corpus_name}.json', 'w') as outfile:
		json.dump(alphabet, outfile, separators=(',', ':'))


if __name__ == '__main__':
	for n in corpus_names:
		get_alphabet(n)