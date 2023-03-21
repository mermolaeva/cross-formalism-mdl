from math import log2, inf
import json


# pretty-printing; NOT part of any MDL term
def pprint_trie(d, sep="", inherit="", parent=""):
	print("{}╴{}".format(sep, parent if parent != "" else '*'))
	if isinstance(d, dict):
		for i, key in enumerate(d):
			if i == len(d)-1: pprint_trie(d[key], inherit+" └──", inherit+"    ", key)
			else: pprint_trie(d[key], inherit+" ├──", inherit+" │  ", key)


def pprint_freq_trie(t):
	pprint_freq_trie_aux(t[1], sep="", inherit="", parent=f'* {t[0]}')


def pprint_freq_trie_aux(d, sep="", inherit="", parent=""):
	print("{}╴{}".format(sep, parent if parent != "" else '*'))
	if isinstance(d, dict):
		for i, key in enumerate(d):
			if i == len(d)-1: pprint_freq_trie_aux(d[key][1], inherit+" └──", inherit+"    ", f'{key} {d[key][0]}')
			else: pprint_freq_trie_aux(d[key][1], inherit+" ├──", inherit+" │  ", f'{key} {d[key][0]}')


# methods obtaining an analysis; NOT part of any MDL term
# convert a list of words into a trie
def make_trie(words, n=1):
	root = dict()
	for word in words:
		word = [word[i:i+n] for i in range(0, len(word), n)]
		current_dict = root
		for letter in word:
			current_dict = current_dict.setdefault(letter, {})
		current_dict[None] = None
	return root


# convert a list of words into a trie with frequencies
def make_freq_trie(words, n=1):
	root = (len(words), dict())
	for word in words:
		word = [word[i:i+n] for i in range(0, len(word), n)]
		current_dict = root[1]
		for letter in word:
			current_val = current_dict.setdefault(letter, [0, {}])
			current_val[0] += 1
			current_dict = current_val[1]
		current_dict.setdefault(None, [0, None])[0] += 1
	return root


# given an analysis and a word, return its cost in bits
def trie_parser(t, word, n=1):
	cost = 0
	current_dict = t
	word = [word[i:i+n] for i in range(0, len(word), n)]
	for letter in word:
		if letter in current_dict:
			cost += log2(len(current_dict))
			current_dict = current_dict[letter]
		else: return inf
	if None in current_dict:
		cost += log2(len(current_dict))
		return cost
	else:
		return inf


def freq_trie_parser(t, word, n=1):
	cost = 0
	current_sum, current_dict = t
	word = [word[i:i+n] for i in range(0, len(word), n)]
	for letter in word:
		if letter in current_dict:
			next_sum = current_dict[letter][0]
			cost += log2(1/(next_sum/current_sum))
			# print(''.join(word), letter, next_sum, current_sum, cost)
			current_sum, current_dict = next_sum, current_dict[letter][1]
		else: return inf
	if None in current_dict:
		next_sum = current_dict[None][0]
		cost += log2(1/(next_sum/current_sum))
		# print(''.join(word), None, next_sum, current_sum, cost)
		return cost
	else:
		return inf


def corpus_cost(parser, grammar, corpus):
	corpus_cost = 0
	for example in corpus:
		corpus_cost += parser(grammar, example)
	return corpus_cost


corpus = 'english990'
words = open(f'{corpus}.txt', 'r').read().strip().split('\n')[:10]
n = 1


# pprint_freq_trie(trie)

freq_trie = make_freq_trie(words, n)
trie = make_trie(words, n)

print(corpus_cost(trie_parser, trie, words))
print(corpus_cost(freq_trie_parser, freq_trie, words))

# trie = make_trie(words[:50], n)

# print(len(words))
# pprint_trie(trie)

# with open(f'{corpus}_trie_{n}.json', 'w') as outfile:
#	json.dump(trie, outfile, indent=2)

# corpus_cost = 0
# for word in words:
# 	word_cost = trie_parser(trie, word, n)
# 	corpus_cost += word_cost


# print('Corpus:', corpus_cost)