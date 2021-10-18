import os, sys
import json


def parse_coverage_json(filepath):
    try:
        # with open(os.path.join(sys.path[0], 'coverage.json'), 'r') as f:
        with open(filepath, 'r') as f:
            coverage_result = json.load(f)
    except Exception as e:
        print(f"Error: {e}")
        print("include coverage.json") 

    return coverage_result['totals']['percent_covered_display']



if len(sys.argv) == 2:
    parse_coverage_json(sys.argv[1])