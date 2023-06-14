import os, sys
sys.path.append(os.path.abspath('.'))

from mdl import read_corpus, corpus_names
import json


# obtain an analysis from a given corpus
def get_alphabet(corpus_name):
	words = read_corpus(corpus_name)
	alphabet = list(set(''.join(words)))

	with open(f'promiscuous/promiscuous_{corpus_name}.json', 'w', encoding='utf-8') as outfile:
		json.dump(alphabet, outfile, separators=(',', ':'), ensure_ascii=False)
	
	with open(f'promiscuous/promiscuous_{corpus_name}.txt', 'w', encoding='utf-8') as outfile:
		outfile.write(''.join(alphabet))


if __name__ == '__main__':
	for n in corpus_names:
		get_alphabet(n)