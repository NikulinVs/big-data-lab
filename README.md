# big-data-lab
Coursework for department of Applied Mathematics of Peter the Great St. Petersburg Polytechnic University

Simple python script for search associated rules.
Usage: 
./apriory.py "filename" "minimal support"
./fp_growth.py "filename" "minimal support"

Input data should be a file in .json or .csv format.

There are also few test files. 
test.sh script applies python script to all .json files in tests folder and tries to compare them with a .out files which have the same name as appropriate .json file.

Also associated rules for every file in dataset folder is calculated by different algorithms and results are compared (they should be the same)
