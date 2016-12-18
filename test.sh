#!/bin/bash

for alg in ./apriori.py ./fp_growth.py
do
    for test_file in tests/*.json
    do
        $alg $test_file 0.3

        alg_name=$(basename $alg)
        rules_name="rules_${alg_name%.py}.txt"

        DIFF=$(diff <(sort $rules_name) <(sort "${test_file%.json}.cmp")) 
        if [ "$DIFF"  == "" ] ; 
        then
            echo "TEST $test_file PASSED with $alg"
        else
            echo "TEST $test_file FAILED with $alg"
        fi
    done
done

for dataset_csv in dataset/*csv
do
    ./apriori.py $dataset_csv 0.05
    ./fp_growth.py $dataset_csv 0.05

    DIFF=$(diff <(sort "rules_apriori.txt") <(sort "rules_fp_growth.txt"))
    if [ "$DIFF"  == "" ] ; 
        then
            echo "APRIORI and FP_GROWTH produced the same result for $dataset_csv"
        else
            echo "APRIORI and FP_GROWTH produced different results for $dataset_csv"
    fi
done



rm "rules_apriori.txt"
rm "rules_fp_growth.txt"