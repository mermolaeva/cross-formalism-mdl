from math import log2, inf

def parser(t, word):
	cost = 0
	current_dict = t
	for letter in word:
		if letter in current_dict:
			cost += log2(len(current_dict))
			current_dict = current_dict[letter]
			print(word, letter, cost)
		else: 
			print('OOPS:', word, letter, cost)
			return inf
	if '#' in current_dict:
		cost += log2(len(current_dict))
		return cost
	else:
		print('OOPS:', word, '#', cost)
		return inf