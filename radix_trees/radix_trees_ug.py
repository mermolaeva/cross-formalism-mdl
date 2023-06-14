from math import log2, inf


def unpack_grammar(s):
	return parse_dict(s[1:-1])


def parse_dict(s):
	d = {}
	i = 0
	while i < len(s):

		if s[i] == '#':
			d['#'] = '#'
			i += 1

		else:
			first_bracket = s[i:].index('{')
			j = i + first_bracket + 1
			counter = 1

			while True:
				if s[j] == '{': counter += 1
				elif s[j] == '}': counter -= 1
				if counter == 0: break
				j += 1

			key = s[i:i+first_bracket].replace('\\\\', '\\')
			val = s[i+first_bracket+1:j]
			i = j+1
			d[key] = parse_dict(val)

	return d


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
