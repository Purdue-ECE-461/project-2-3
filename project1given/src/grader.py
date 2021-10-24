import sys
import json
import os
from URL_info import URL_info
from metrics import Metrics
import logging
import os

def output_json(final, file_path):
    full_path  = file_path + 'LOG_FILE.json'
    with open(full_path, 'w') as fout:
        json.dump( final , fout)

def score_stdout(scores):
    for score in scores:
        print(f"{score['URL']} {score['Net Score']:.1f} {score['Ramp Up Score']:.1f} {score['Correctness Score']:.1f} {score['Bus Factor Score']:.1f} {score['Reponsiveness Score']:.1f} {score['License Score']:.1f}")

def main():
    if len(sys.argv) == 2:
        url_file_path = sys.argv[1]

        log_file = "./src/LOG_FILE.log"
        logging.basicConfig(filename = log_file, level=0)
        with open(url_file_path, 'r') as url_file:
            urls = url_file.read().splitlines()
        TOKEN = "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"
        print('URL NET_SCORE RAMP_UP_SCORE CORRECTNESS_SCORE BUS_FACTOR_SCORE RESPONSIVE_MAINTAINER_SCORE LICENSE_SCORE')
        final = []
        for url in urls:
            repo = URL_info(url=url, token=TOKEN)
            metric = Metrics(repo_data=repo)
            metric.runMetrics()
            if metric.getJsonOutput() is not None:
                final.append(metric.getJsonOutput())
        
        final.sort(key=lambda d:d['Net Score'], reverse=True)
        score_stdout(final)
        output_json(final,"")


if __name__ == '__main__':
    main()