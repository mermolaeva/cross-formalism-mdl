from math import log2
import json
import importlib
import re
from string import printable


ignored_chars = ['#', '{', '}', '[', ']']
max_lines = 100000


def string_cost(s, alphabet):
	cost = len(s) * log2(len(alphabet))
	return cost


def total_cost(ug_name, grammar_name, corpus_name, alphabet, compress=True):
	ug = importlib.import_module(f'{ug_name}.{ug_name}_ug')
	try:
		assert compress is True
		grammar_string = read_file(f'{ug_name}/{grammar_name}.txt', capped=False)
		grammar = ug.unpack_grammar(grammar_string)
		unpacked = True
	except:
		grammar_string = read_file(f'{ug_name}/{grammar_name}.json', capped=False)
		grammar = read_grammar(grammar_name)
		unpacked = False

	ug_string = read_file(f'{ug_name}/{ug_name}_ug.py', capped=False)
	
	data = read_corpus(corpus_name)

	ug_cost = string_cost(ug_string, alphabet)
	grammar_cost = string_cost(grammar_string, alphabet) # TODO: inside ug; separate alphabet; variable-length encoding
	data_cost = ug.corpus_cost(grammar, data)
	cost = ug_cost + grammar_cost + data_cost
	
	print(f'UG: {ug_name}, dataset: {corpus_name}, words: {len(data)} {"[optimized]" if unpacked else "[unoptimized]"}')
	print('UG cost: {0:,.3f}, grammar cost: {1:,.3f}, corpus cost: {2:,.3f}. Sum: {3:,.3f}'.format(ug_cost, grammar_cost, data_cost, cost))

	return cost


def get_chars(file_name):
	chars = set()
	lines = 0
	for line in open(file_name, 'r'):
		if lines < max_lines:
			lines += 1
			chars.update(set(line))
		else:
			break
	return chars


def read_file(file_name, capped=True):
	lines = []
	for line in open(file_name, 'r'):
		if (not capped) or (len(lines) < max_lines):
			lines.append(line)
		else:
			break
	return '\n'.join(lines)


def read_corpus(corpus_name, ext='txt'):
	text = read_file(f'corpora/{corpus_name}.{ext}').strip()
	for char in ignored_chars: text = text.replace(char, '')
	words = re.findall('[^ \n\t]+', text)
	return words


def read_grammar(grammar_name):
	with open(f'{grammar_name}.json', 'r') as file:
		grammar = json.load(file)
	return grammar


corpus_names = ['brown', 'turkish', 'swahili']
# corpus_names = ['test',]

ug_names = ['promiscuous', 'lists', 'tries', 'freq_tries', 'radix_trees']
# ug_names = ['radix_trees', ]


if __name__ == '__main__':
	alphabet = set(printable).union(*[get_chars(f'corpora/{c}.txt') for c in corpus_names])

	for ug_name in ug_names:
		total = 0
		for corpus_name in corpus_names:
			grammar_name = f'{ug_name}_{corpus_name}'
			total += total_cost(ug_name, grammar_name, corpus_name, alphabet, True)

		print('{0}\nTotal for {1}: {2:,.3f}\n{0}\n'.format("-"*40, ug_name, total))