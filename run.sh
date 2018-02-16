#!/bin/bash
#
# Use this shell script to compile (if necessary) your code and then execute it. Below is an example of what might be found in this file if your program was written in Python
echo "Running donation_analysis on input/ "
python ./src/donation_analysis.py ./input/itcont.txt ./input/percentile.txt ./output/repeat_donors.txt
# echo " "
# echo " "
# echo " "
# echo " "
# echo "Running donation_analysis on my test case in --> insight_testsuite/tests/your-own-test_1/input/"
# Testing my testcase
# python ./src/donation_analysis.py ./insight_testsuite/tests/your-own-test_1/input/itcont.txt ./insight_testsuite/tests/your-own-test_1/input/percentile.txt ./insight_testsuite/tests/your-own-test_1/output/repeat_donors.txt
