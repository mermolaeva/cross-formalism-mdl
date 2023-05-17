from math import log2, inf
from json import loads


def unpack_grammar(s):
	return s


def corpus_cost(grammar, corpus):
	if set(''.join(corpus)).issubset(grammar):
		return log2(len(grammar)) * (len(corpus) + len(''.join(corpus)))
	else:
		return inf