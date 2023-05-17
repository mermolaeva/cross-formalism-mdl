from math import log2, inf
from json import loads


def unpack_grammar(s):
	s = s.replace('"', '\\"')
	s2 = ''
	for i, c in enumerate(s):
		if c not in '{}':
			if i > 0:
				if s[i-1] == '}':
					s2 += f', "'
				elif s[i-1] == '#':
					s2 += f'", "'
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
		cost += parser(grammar, example)
	return cost


def parser(t, suffix):
	cost = 0
	current_dict = t
	while True:
		for key in current_dict:
			if len(suffix) == 0 and key == '#':
				cost += log2(len(current_dict))
				return cost
			elif suffix.startswith(key):
				cost += log2(len(current_dict))
				current_dict = current_dict[key]
				suffix = suffix[len(key):]
				break
		else:
			return inf
