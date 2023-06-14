from math import log2, inf


def unpack_grammar(s):
	ind = s.index('{')
	return([int(s[:ind]), parse_dict(s[ind+1:-1])])


def split_key(k):
	if k[0] == '\\': return ['\\', int(k[2:])]
	else: return (k[0], int(k[1:]))


def parse_dict(s):
	d = {}
	i = 0
	while i < len(s):

		if s[i] == '#':
			last_ind = s[i+1:].index('#')
			freq = int(s[i+1:i+last_ind+1])
			d['#'] = [freq, '#']
			i += last_ind + 2

		else:
			first_bracket = s[i:].index('{')
			j = i + first_bracket + 1
			counter = 1

			while True:
				if s[j] == '{': counter += 1
				elif s[j] == '}': counter -= 1
				if counter == 0: break
				j += 1

			key, freq = split_key(s[i:i+first_bracket])
			val = s[i+first_bracket+1:j]
			i = j+1
			d[key] = (freq, parse_dict(val))

	return d


def corpus_cost(grammar, corpus):
	cost = 0
	for example in corpus:
		cost += parser(grammar, example)
	return cost


def parser(t, word):
	cost = 0
	current_sum, current_dict = t
	for letter in word:
		if letter in current_dict:
			next_sum = current_dict[letter][0]
			cost += log2(1/(next_sum/current_sum))
			current_sum, current_dict = next_sum, current_dict[letter][1]
		else: return inf
	if '#' in current_dict:
		next_sum = current_dict['#'][0]
		cost += log2(1/(next_sum/current_sum))
		return cost
	else:
		return inf