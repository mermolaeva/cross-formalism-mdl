from math import log2, inf


def corpus_cost(grammar, corpus):
	cost = 0
	for example in corpus:
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