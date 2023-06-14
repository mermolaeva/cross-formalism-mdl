import os, sys
sys.path.append(os.path.abspath('.'))

from mdl import read_corpus, corpus_names # TODO: separate into corpus_utils
import json
import re
from tries.tries_extras import special_chars, special_mark


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
			key = letter if letter not in special_chars else f'{special_mark}{letter}'
			current_val = current_dict.setdefault(key, [0, {}])
			current_val[0] += 1
			current_dict = current_val[1]
		current_dict.setdefault('#', [0, '#'])[0] += 1
	return root


# obtain an analysis from a given corpus
def corpus_to_freq_trie(corpus_name):

	words = read_corpus(corpus_name)

	freq_trie = make_freq_trie(words)
	
	s = json.dumps(freq_trie, separators=(',', ':'), ensure_ascii=False)
	uncompressed = s.replace(special_mark, '')

	s = s.replace(f'{special_mark}\\\"', f'{special_mark}\"') # un-escape marked double quotes

	for char in special_chars: # remove special chars unless marked
		s = re.sub(f'(?<!{special_mark}){re.escape(char)}', '', s)

	s = re.sub(r'\[([0-9]+)', r'\1', s)
	s = s.replace('[', '').replace(']', '')
	s = s.replace(special_mark, '') # remove marks

	with open(f'freq_tries/freq_tries_{corpus_name}.txt', 'w', encoding='utf-8') as outfile: # compressed version
		outfile.write(s)

	with open(f'freq_tries/freq_tries_{corpus_name}.json', 'w', encoding='utf-8') as outfile: # uncompressed version
		outfile.write(uncompressed)


# def split_key(k):
# 	if k[0] == '\\': return [k[0:1], int(k[2:])]
# 	else: return (k[0], int(k[1:]))


# def parse_dict(s):
# 	d = {}
# 	i = 0
# 	while i < len(s):

# 		if s[i] == '#': # special case; skipping to next #
# 			last_ind = s[i+1:].index('#')
# 			freq = int(s[i+1:i+last_ind+1])
# 			d['#'] = [freq, '#']
# 			i += last_ind + 2

# 		else:
# 			try:
# 				first_bracket = s[i:].index('{')
# 				j = i + first_bracket + 1
# 				counter = 1

# 				while True:
# 					if s[j] == '{': counter += 1
# 					elif s[j] == '}': counter -= 1
# 					if counter == 0: break
# 					j += 1

# 				key, freq = split_key(s[i:i+first_bracket])
# 				val = s[i+first_bracket+1:j]
# 				i = j+1
# 				d[key] = (freq, parse_dict(val))

# 			except ValueError: return None # not supposed to happen

# 	return d


if __name__ == '__main__':
	for n in corpus_names:
		corpus_to_freq_trie(n)