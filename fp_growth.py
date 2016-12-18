#!/usr/bin/python3

import os
from itertools import chain, combinations
import json, sys, csv

def load_file(file_name):

    filename, file_extension = os.path.splitext(file_name)

    if file_extension == '.json':

        with open(file_name) as data_file:    
            return json.load(data_file)

    elif file_extension == '.csv':
        output_data = []
        with open(file_name) as data_file: 
            reader = csv.reader(data_file, delimiter=',')
            for row in reader:
                output_data.append(row[1:])
        return output_data

    else:
        print("Incorrect file extension")
        return None



def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def subsets(s):
    return map(frozenset, powerset(s))

def FP_growth(transactions, minimum_support):
    confidence_threshold = 0.4

    items = {}

    transactions = list(map(sorted, transactions))

    for transaction in transactions:
        for item in transaction:
            items[item] = items[item] + 1 if item in items else 1


    items = dict((item, freq) for item, freq in items.items()
        if freq / len(transactions) >= minimum_support)

    master = Tree()
    for transaction in transactions:
        master.add(transaction)

    def suf_find(tree, suffix):
        for item, nodes in tree.items():
            support = sum(n.count for n in nodes)
            if support >= minimum_support * len(transactions) and item not in suffix:
                found_set = [item] + suffix
                yield (frozenset(found_set), support)

                condtree = conditionaltree_from_paths(tree.prefix_paths(item))
                for s in suf_find(condtree, found_set):
                    yield s

    itemsets = {}

    for itemset in suf_find(master, []):
        itemsets[itemset[0]] = itemset[1]

    associated_rules_dict = {}

    for item in itemsets.keys():
        for subset in subsets(item):
            if subset == set():
                continue
            remain_element = item.difference(subset)
            if len(remain_element) > 0:
                confidence = itemsets[item] / itemsets[subset]
                if confidence >= confidence_threshold:
                    associated_rules_dict[" -> ".join((', '.join(subset), ', '.join(remain_element)))] = confidence

    return associated_rules_dict


class Node(object):

    def __init__(self, tree, item, count=1):
        self.tree = tree
        self.item = item
        self.count = count
        self.parent = None
        self.children = {}
        self.neighbor = None

    def add(self, child):
        if not child.item in self.children:
            self.children[child.item] = child
            child.parent = self

    def search(self, item):
        if item in self.children:
            return self.children[item]
        else:
            return None


class Tree(object):
    def __init__(self):
        self.root = Node(self, None, None)
        self.path = {}

    def add(self, transaction):
        point = self.root

        for item in transaction:
            next_point = point.search(item)
            if next_point:
                next_point.count += 1
            else:
                next_point = Node(self, item)
                point.add(next_point)

                self.update_path(next_point)

            point = next_point

    def update_path(self, point):

        try:
            route = self.path[point.item]
            route[1].neighbor = point
            self.path[point.item] = (route[0], point)
        except KeyError:
            self.path[point.item] = (point, point)

    def items(self):
        for item in self.path.keys():
            yield (item, self.nodes(item))

    def nodes(self, item):
        try:
            node = self.path[item][0]
        except KeyError:
            return

        while node:
            yield node
            node = node.neighbor

    def prefix_paths(self, item):
        def collect_path(node):
            path = []
            while node and not node.item is None and not node.count is None:
                path.append(node)
                node = node.parent
            path.reverse()
            return path

        return (collect_path(node) for node in self.nodes(item))

def conditionaltree_from_paths(paths):
    tree = Tree()
    conditionitem = None
    items = set()
    for path in paths:
        if conditionitem is None:
            conditionitem = path[-1].item

        point = tree.root
        for node in path:
            next_point = point.search(node.item)
            if not next_point:
                items.add(node.item)
                count = node.count if node.item == conditionitem else 0
                next_point = Node(tree, node.item, count)
                point.add(next_point)
                tree.update_path(next_point)
            point = next_point

    assert conditionitem is not None

    for path in tree.prefix_paths(conditionitem):
        count = path[-1].count
        for node in reversed(path[:-1]):
            node.count += count

    return tree




if len(sys.argv) < 3:
    print("Usage: apriori.py <filename> <minimum support>")
else:

    transactions = load_file(sys.argv[1])

    if transactions is not None:
    
        associated_rules = FP_growth(transactions, float(sys.argv[2]))
        with open('rules_fp_growth.txt', 'w') as outfile:
            for rule, conf in associated_rules.items():
                outfile.write(rule + " : " + "%.3f" % conf + "\n")
