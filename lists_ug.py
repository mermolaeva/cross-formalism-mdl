from math import log2, inf
from json import loads


def unpack_grammar(s):
	return s.split(' ')


def corpus_cost(grammar, corpus):
	if set(corpus).issubset(grammar):
		return log2(len(grammar)) * len(corpus)
	else:
		return inf