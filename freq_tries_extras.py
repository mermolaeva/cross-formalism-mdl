from mdl import read_corpus, corpus_names # TODO: separate into corpus_utils
import json
import re
from tries_extras import special_chars, special_mark


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
	s = re.sub(r'#([0-9]+)#', r'#\1', s) # simplify end-of-word notation



	s = s.replace('"', '\\"')
	s2 = ''
	for i, c in enumerate(s):
		if c not in '{}':
			if i > 0:
				if not s[i-1] in '{\\': 
					if s[i-1] != '}': s2 += '"'
					s2 += f', "'
				elif s[i-1] == '{': s2 += '"'
			s2 += c
			if c == '#': s2 += '": "#'
			if i < len(s)-1:
				if s[i+1] == '{': s2 += '": '
				elif s[i+1] == '}': s2 += '"'
		else: s2 += c
	
	uncompressed = s2



	with open(f'freq_tries_{corpus_name}.txt', 'w', encoding='utf-8') as outfile: # compressed version
		outfile.write(s)

	with open(f'freq_tries_{corpus_name}.json', 'w', encoding='utf-8') as outfile: # uncompressed version
		outfile.write(uncompressed)

	# with open(f'freq_tries_{corpus_name}.json', 'w') as outfile:
	# 	json.dump(freq_trie, outfile, separators=(',', ':'))


if __name__ == '__main__':
	for n in corpus_names:
		corpus_to_freq_trie(n)