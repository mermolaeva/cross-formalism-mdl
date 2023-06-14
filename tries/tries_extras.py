import os, sys
sys.path.append(os.path.abspath('.'))

from mdl import read_corpus, corpus_names
import json
import re


# pretty-printing; NOT part of any MDL term
def pprint_trie(d, sep="", inherit="", parent=""):
	print("{}╴{}".format(sep, parent if parent != "" else '*'))
	if isinstance(d, dict):
		for i, key in enumerate(d):
			if i == len(d)-1: pprint_trie(d[key], inherit+" └──", inherit+"    ", key)
			else: pprint_trie(d[key], inherit+" ├──", inherit+" │  ", key)


# list of special characters; used to minimize the grammar
special_chars = ['"', ':', ',', ' ']
special_mark = '###'


# methods of obtaining an analysis; NOT part of any MDL term
# convert a list of words into a trie
def make_trie(words):
	root = dict()
	for word in words:
		current_dict = root
		for letter in word:
			key = letter if letter not in special_chars else f'{special_mark}{letter}'
			current_dict = current_dict.setdefault(key, {})
		current_dict['#'] = '#'
	return root


# obtain an analysis from a given corpus
def corpus_to_trie(corpus_name, rev=False):
	words = read_corpus(corpus_name)
	if rev: words = [w[::-1] for w in words]
	trie = make_trie(words)

	s = json.dumps(trie, separators=(',', ':'), ensure_ascii=False)
	uncompressed = s.replace(special_mark, '')

	s = s.replace(f'{special_mark}\\\"', f'{special_mark}\"') # un-escape marked double quotes

	for char in special_chars: # remove special chars unless marked
		s = re.sub(f'(?<!{special_mark}){re.escape(char)}', '', s)

	s = s.replace(special_mark, '') # remove marks
	s = s.replace('##', '#') # simplify end-of-word notation

	grammar_name = f'{"rev_" if rev else ""}tries'

	with open(f'{grammar_name}/{grammar_name}_{corpus_name}.txt', 'w', encoding='utf-8') as outfile: # compressed version
		outfile.write(s)

	with open(f'{grammar_name}/{grammar_name}_{corpus_name}.json', 'w', encoding='utf-8') as outfile: # uncompressed version
		outfile.write(uncompressed)


if __name__ == '__main__':
	for n in corpus_names:
		corpus_to_trie(n, False)
		# corpus_to_trie(n, True)