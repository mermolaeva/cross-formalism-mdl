from math import log2, inf
from json import loads


def unpack_grammar(s):
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
	return loads(s2)


def corpus_cost(grammar, corpus):
	cost = 0
	for example in corpus:
		example = example[::-1]
		cost += parser(grammar, example)
	return cost


def parser(t, word):
	cost = 0
	current_dict = t
	for letter in word:
		if letter in current_dict:
			cost += log2(len(current_dict))
			current_dict = current_dict[letter]
		else: 
			return inf
	if '#' in current_dict:
		cost += log2(len(current_dict))
		return cost
	else:
		return inf