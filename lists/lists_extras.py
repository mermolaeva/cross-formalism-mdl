import os, sys
sys.path.append(os.path.abspath('.'))

from mdl import read_corpus, corpus_names
import json


# obtain an analysis from a given corpus
def corpus_to_list(corpus_name):
	words = read_corpus(corpus_name)

	with open(f'lists/lists_{corpus_name}.json', 'w', encoding='utf-8') as outfile:
		json.dump(list(set(words)), outfile, separators=(',', ':'), ensure_ascii=False)

	with open(f'lists/lists_{corpus_name}.txt', 'w', encoding='utf-8') as outfile:
		outfile.write(' '.join(set(words)))


if __name__ == '__main__':
	for n in corpus_names:
		corpus_to_list(n)