import git
import os, sys
import shutil
import logging

def clone(cloneurl, filepath, tryagain = True):
    try:
        logging.info('Cloning repo: %s...',cloneurl)
        git.Repo.clone_from(cloneurl, filepath)
        logging.info('Repo downloaded successfully: %s',cloneurl)
    except Exception as e:
        if (tryagain):
            logging.warning('Clone error: %s, Clearing temp and retrying...',(e))
            cleartemp(filepath)
            clone(cloneurl, filepath, False)
        else:
            logging.warning('Clone error: %s, Clearing temp and exiting...', (e))
            cleartemp(filepath)
            return -1

def cleartemp(filepath):
    for filename in os.listdir(filepath):
        file_path = os.path.join(filepath, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            logging.warning('Failed to delete %s. Reason: %s', file_path, e)
            return -1
