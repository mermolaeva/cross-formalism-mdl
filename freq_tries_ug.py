from math import log2, inf

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