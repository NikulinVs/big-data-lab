#!/bin/bash

for test_file in tests/*.json
do
	./apriori.py "$test_file" 0.3

	DIFF=$(diff <(sort "rules.txt") <(sort "${test_file%.json}.cmp")) 
	if [ "$DIFF"  == "" ] ; 
	then
		echo "TEST $test_file PASSED"
	else
		echo "TEST $test_file FAILED"
	fi
done

rm "rules.txt"