import json
import os, sys

def parse_coverage_json(filepath):
    try:
        # with open(os.path.join(sys.path[0], 'coverage.json'), 'r') as f:
        with open(filepath, 'r') as f:
            coverage_result = json.load(f)
    except Exception as e:
        print(f"Error: {e}")
        print("include coverage.json") 

    return coverage_result['totals']['percent_covered_display']

def parse_test_json(filepath):
    try:
        with open(filepath,'r') as f:
            data = json.load(f)
        return data['summary']['passed'], data['summary']['total']
    except:
        return 0, 0

def main():
    percent_code = 0
    pass_tests = 0
    num_tests = 0
    if len(sys.argv) == 3:
        percent_code = parse_coverage_json(sys.argv[1])
        pass_tests, num_tests = parse_test_json(sys.argv[2])
 
    
    print("Total: {}".format(num_tests))
    print("Passed: {}".format(pass_tests))
    print("Coverage: {}%".format(percent_code))
    print("{}/{} test cases passed. {}% line coverage achieved.".format(num_tests,pass_tests, percent_code))
main()