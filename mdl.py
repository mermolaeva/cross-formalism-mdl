from math import log2
import json
import importlib


def corpus_cost(parser, grammar, corpus):
	cost = 0
	for example in corpus:
		cost += parser(grammar, example)
	return cost


def string_cost(s):
	chars = set(s)
	cost = len(s) * log2(len(chars))
	return cost


def total_cost(ug_name, grammar_name, corpus_name):
	ug = importlib.import_module(f'{ug_name}_ug')
	grammar = read_grammar(grammar_name)

	ug_string = read_file(f'{ug_name}_ug.py')
	grammar_string = read_file(f'{grammar_name}.json')
	
	data = read_corpus(corpus_name)

	ug_cost = string_cost(ug_string)
	grammar_cost = string_cost(grammar_string)
	data_cost = corpus_cost(ug.parser, grammar, data)
	cost = ug_cost + grammar_cost + data_cost
	
	print(f'UG: {ug_name}, dataset: {corpus_name}')
	print(f'UG cost: {ug_cost}, grammar cost: {grammar_cost}, corpus cost: {data_cost}')
	print(f'Total cost: {cost}\n')

	return cost


def read_file(file_name):
	return open(file_name, 'r').read()


def read_corpus(corpus_name):
	words = read_file(f'{corpus_name}.txt').strip().split('\n')
	return words


def read_grammar(grammar_name):
	with open(f'{grammar_name}.json', 'r') as file:
		grammar = json.load(file)
	return grammar


corpus_names = ['english990',]
ug_names = ['tries', 'freq_tries']


if __name__ == '__main__':
	for ug_name in ug_names:
		for corpus_name in corpus_names:
			grammar_name = f'{ug_name}_{corpus_name}'
			cost = total_cost(ug_name, grammar_name, corpus_name)