import sys
import pytest
import os
import json
import requests
import pandas as pd
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

from URL_info import URL_info
from gitclone import *
from rampup import *
from busfactor import busFactor
from responseMaintainer import responseMaintainer
from licensing import licensing
from correctness import correctness

# TEST URLS
urls = [
    "https://github.com/lodash/lodash",
    "https://www.npmjs.com/package/browserify",
    "https://www.npmjs.com",
    "https://api.github.com/repos/jgthms/bulma",
    "https://piazza.com/"
]

compatible_license = {
                        "GPL-2.0-only": True,
                        "GPL-2.0-or-later": True,
                        "GPL-3.0-only": True,
                        "LGPL-2.1-only": True,
                        "LGPL-2.1-or-later": True,
                        "LGPL-3.0-only": True, 
                        "BSL-1.0": True, 
                        "CECILL-2.0": True, 
                        "ClArtistic": True, 
                        "EUDatagrid": True, 
                        "EFL-2.0": True,
                        "Intel": True,
                        "Vim": True,
                        "Zlib": True,
                        "iMatix": True,
                        "BSD-3-Clause-Modification": True,
                        "OLDAP-2.7": True,
                        "SMLNJ": True,
                        "Ruby": True,
                        "W3C": True,
                        "X11": True,
                        "MIT": True,
                        "ZPL-2.0": True,
                        "eCos-2.0": True,
                        "Apache-2.0": True
                    }
TOKEN = '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'

# URL INFO TESTS
def testGoodGit():
    repo = URL_info(url=urls[0], token=TOKEN)
    return repo.github_api_url

def testGoodNpm():
    repo = URL_info(url=urls[1], token=TOKEN)
    return repo.github_api_url

def testBadNpm():
    repo = URL_info(url=urls[2], token=TOKEN)
    return repo.github_api_url

def testBadGit():
    repo = URL_info(url=urls[3], token=TOKEN)
    return repo.github_api_url

def testBadAny():
    repo = URL_info(url=urls[4], token=TOKEN)
    return repo.github_api_url

# CLONE TESTS
def testCloneRepo():
    repo = URL_info(url=urls[0], token=TOKEN)
    filepath = os.path.join(script_dir, "./temp")
    return clone(repo.data["clone_url"], filepath)

def testDeleteRepo():
    filepath = os.path.join(script_dir, "./temp")
    return cleartemp(filepath)

# RAMP UP TESTS
def testCalcReadme():
    filepath = os.path.join(script_dir, "./testrepo")
    return calcReadme(filepath)

def testCalcComments():
    filepath = os.path.join(script_dir, "./testrepo/index.js")
    return calcComments(filepath)[2]

def testRampup():
    filepath = os.path.join(script_dir, "./testrepo")
    return rampup(filepath)

# CORRECTNESS TESTS
def testCorrectnessFile():
    filepath = os.path.join(script_dir, "./testfile")
    return correctness(filepath)

def testCorrectnessFolder():
    filepath = os.path.join(script_dir, "./testrepo")
    return correctness(filepath)

def testNoCorrectness():
    filepath = os.path.join(script_dir, "./notest")
    return correctness(filepath)

# BUS FACTOR TESTS
def testBFone():
    contributors = 1
    return busFactor(contributors)
def testBFmulti():
    contributors = 20
    return busFactor(contributors)
def testBF100plus():
    contributors = 123
    return busFactor(contributors)

# RESPONSE MAINTAINER TESTS
def test_none_maintainer():
    issues = None
    return responseMaintainer(issues)

def test_empty_maintainer():
    issues = pd.DataFrame([])
    return responseMaintainer(issues)

def test_actual_maintainer():
    url = "https://github.com/cloudinary/cloudinary_npm"
    repo = URL_info(url=url, token=TOKEN)
    return responseMaintainer(repo.issues)

# LICENSING TESTS
def testLicense():
    license = "MIT"
    return licensing(license, compatible_license)
def testNoLicense():
    license = None
    return licensing(license, compatible_license)
def testInvalidLicense():
    license = "hello"
    return licensing(license, compatible_license)

# MAIN
def main():
    # TEST URL BUILDER
    assert testGoodGit() != None
    assert testGoodNpm() != None
    assert testBadNpm() == None
    assert testBadGit() == None
    assert testBadAny() == None

    # TEST CLONE / DELETE
    assert testCloneRepo() != -1
    assert testDeleteRepo() != -1

    # TEST RAMPUP
    assert testCalcReadme() == 0.4825
    assert testCalcComments() == 7
    assert testRampup() == 0.6378

    # TEST CORRECTNESS
    assert testCorrectnessFile() == 1
    assert testCorrectnessFolder() == 1
    assert testNoCorrectness() == 0

    # TEST BUS FACTOR
    assert testBFone() == 0
    assert testBFmulti() == 0.95
    assert testBF100plus() == 1

    # TEST RESPONSE MAINTAINER
    assert test_none_maintainer() == 0
    assert test_empty_maintainer() == 0
    assert test_actual_maintainer() == 0.225

    # TEST LICENSING
    assert testLicense() == 1
    assert testNoLicense() == 0
    assert testInvalidLicense() == 0


main()