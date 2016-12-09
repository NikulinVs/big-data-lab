#!/usr/bin/python3

import sys
from itertools import chain, combinations
import json


def load_file(file_name):
	with open(file_name) as data_file:    
		data = json.load(data_file)

	return data


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def subsets(s):
    return map(frozenset, powerset(s))


def min_support_items(item_set, record_list, min_support, frequency_dict):
	result_item_set = set()
	local_frequency_dict = {}

	for item in item_set:
		for record in record_list:
			if item.issubset(record):
				frequency_dict[item] = frequency_dict[item] + 1 if item in frequency_dict else 1
				local_frequency_dict[item] = local_frequency_dict[item] + 1 if item in local_frequency_dict else 1

	for item, count in local_frequency_dict.items():
		if float(count) / len(record_list) >= min_support:
			result_item_set.add(item)

	return result_item_set


def Apriori(record_list, min_support):
	confidence_threshold = 0.6	

	item_set = set()
	for record in record_list:
		for item in record:
			item_set.add(frozenset([item]))

	frequency_dict = {}
	associated_rules_dict = {}

	def support(item):
		return float(frequency_dict[item]) / len(record_list)

	curr_item_set = {}

	L_set = min_support_items(item_set, record_list, min_support, frequency_dict)

	k = 2
	while L_set != set():
		curr_item_set[k - 1] = L_set
		k_item_set = set([it1.union(it2) for it1 in L_set for it2 in L_set if len(it1.union(it2)) == k])
		C_set = min_support_items(k_item_set, record_list, min_support, frequency_dict)
		L_set = C_set
		k += 1

	for key, value in curr_item_set.items():
		for item in value:
			for subset in subsets(item):
				if subset == set():
					continue
				remain_element = item.difference(subset)
				if len(remain_element) > 0:
					confidence = support(item) / support(subset)
					if confidence >= confidence_threshold:
						associated_rules_dict[" -> ".join((', '.join(subset), ', '.join(remain_element)))] = confidence

	return associated_rules_dict



if len(sys.argv) < 3:
	print("Usage: apriori.py <filename> <minimum support>")
else:
	associated_rules = Apriori(load_file(sys.argv[1]), float(sys.argv[2]))
	with open('rules.txt', 'w') as outfile:
		for rule, conf in associated_rules.items():
			outfile.write(rule + " : " + str(conf) + "\n")