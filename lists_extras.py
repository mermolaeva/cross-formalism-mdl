# from tries_ug import * # is allowed to import UG functions, but doesn't have to
from mdl import read_corpus, corpus_names
import json


# obtain an analysis from a given corpus
def corpus_to_list(corpus_name):
	words = read_corpus(corpus_name)
	with open(f'lists_{corpus_name}.json', 'w') as outfile:
		json.dump(words, outfile)


if __name__ == '__main__':
	for n in corpus_names:
		corpus_to_list(n)