import os, sys
sys.path.append(os.path.abspath('.'))

from mdl import read_corpus, corpus_names
import json
from tries.tries_extras import pprint_trie, make_trie, special_chars, special_mark
import re


# # pretty-printing; NOT part of any MDL term
# def pprint_trie(d, sep="", inherit="", parent=""):
# 	print("{}╴{}".format(sep, parent if parent != "" else '*'))
# 	if isinstance(d, dict):
# 		for i, key in enumerate(d):
# 			if i == len(d)-1: pprint_trie(d[key], inherit+" └──", inherit+"    ", key)
# 			else: pprint_trie(d[key], inherit+" ├──", inherit+" │  ", key)


# # methods of obtaining an analysis; NOT part of any MDL term
# # convert a list of words into a trie
# def make_trie(words):
# 	root = dict()
# 	for word in words:
# 		current_dict = root
# 		for letter in word:
# 			current_dict = current_dict.setdefault(letter, {})
# 		current_dict['#'] = '#'
# 	return root


def process_key(k):
	return ''.join(letter if letter not in special_chars else f'{special_mark}{letter}' for letter in k)


def compress_trie(t1):
	t2 = {}
	for key, val in t1.items(): # key is string, val is dict or "#"
		if val == '#':
			key_going_up = '#'
			t2[key_going_up] = '#'

		elif len(val) == 1:
			next_val, assembled_key = compress_trie(t1[key])
			if assembled_key == '#':
				key_going_up = key
				t2[key_going_up] = next_val
			else:
				key_going_up = key + assembled_key
				t2[key_going_up] = next_val[assembled_key]

		else:
			next_val, assembled_key = compress_trie(t1[key])
			key_going_up = key
			t2[key_going_up] = next_val

	return t2, key_going_up


# obtain an analysis from a given corpus
def corpus_to_trie(corpus_name):
	words = read_corpus(corpus_name)
	trie = compress_trie(make_trie(words))[0]

	s = json.dumps(trie, separators=(',', ':'), ensure_ascii=False)
	uncompressed = s.replace(special_mark, '')

	s = s.replace(f'{special_mark}\\\"', f'{special_mark}\"') # un-escape marked double quotes

	for char in special_chars: # remove special chars unless marked
		s = re.sub(f'(?<!{special_mark}){re.escape(char)}', '', s)

	s = s.replace(special_mark, '') # remove marks
	s = s.replace('##', '#') # simplify end-of-word notation

	with open(f'radix_trees/radix_trees_{corpus_name}.txt', 'w', encoding='utf-8') as outfile: # compressed version
		outfile.write(s)
	
	with open(f'radix_trees/radix_trees_{corpus_name}.json', 'w', encoding='utf-8') as outfile: # uncompressed version
		outfile.write(uncompressed)


if __name__ == '__main__':
	for n in corpus_names:
		corpus_to_trie(n)