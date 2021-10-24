import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
# sys.path.append('../')

from URL_info import URL_info
from metrics import Metrics
import logging
import os
import json

def output_json(final, file_path):
    full_path  = file_path + 'LOG_FILE.json'
    with open(full_path, 'w') as fout:
        json.dump( final , fout)

def score_stdout(scores):
    for score in scores:
        print(f"{score['URL']} {score['Net Score']:.1f} {score['Ramp Up Score']:.1f} {score['Correctness Score']:.1f} {score['Bus Factor Score']:.1f} {score['Reponsiveness Score']:.1f} {score['License Score']:.1f}")

if len(sys.argv) == 2:
    url_file_path = sys.argv[1]

    log_file = "./src/test/LOG_FILE.log"
    logging.basicConfig(filename = log_file, level=0)
    with open(url_file_path, 'r') as url_file:
        urls = url_file.read().splitlines()

    TOKEN = str(os.environ.get('GITHUB_TOKEN'))
    final = []
    for url in urls:
        repo = URL_info(url=url, token=TOKEN)
        metric = Metrics(repo_data=repo)
        metric.runMetrics()
        if metric.getJsonOutput() is not None:
            final.append(metric.getJsonOutput())
    
    final.sort(key=lambda d:d['Net Score'], reverse=True)
    output_json(final,"")
