# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from flask import current_app, flash, Flask, Markup, redirect, render_template, request, url_for
import google.cloud.logging

from Packages import Packages
pacs = Packages()
from SemverRange import SemverRange
svr = SemverRange()
from PackageHistoryEntry import PackageHistoryEntry
action = PackageHistoryEntry()
from Package import Package
pak = Package()
from Error import Error
e = Error()

import responses
import requests
import json

import firestore as Firestore

app = Flask(__name__)
app.config.update(
    SECRET_KEY='secret',
    MAX_CONTENT_LENGTH=1000000,
    ALLOWED_EXTENSIONS=set(['zip']),
    CLOUD_STORAGE_BUCKET = 'ece461-p2-t3-files'
)

app.debug = False
app.testing = False
'''
# Configure logging
if not app.testing:
    logging.basicConfig(level=logging.INFO)
    client = google.cloud.logging.Client(project='ece461-p2-t3')
    # Attaches a Google Stackdriver logging handler to the root logger
    client.setup_logging()
'''

@app.route('/authenticate/', methods=['PUT'])
def authenticate():
    return e.set("This system does not support authentication.",501)

@app.route('/package/<id>/rate/', methods=['GET'])
def rate_by_ID(id, pak = None):
    total = 0.0
    from PackageRating import PackageRating
    rateObj = PackageRating()
    from Packages import Packages
    pacs = Packages()
    pacs = pacs.update()
    if pak == None:
        try:
            pak = pacs.packageDictionary[id]
        except:
            return e.malformed()
    if pak == None:
        return e.malformed()
    url = pak.data.URL
    if not url:
        return e.set("rating of package failed", 500)
    #TODO call scoring here
    from project1given.src.busfactor import busFactor
    from project1given.src.correctness import correctness
    from project1given.src.gitclone import clone
    from project1given.src.URL_info import URL_info
    from project1given.src.licensing import licensing
    from project1given.src.metrics import Metrics
    from project1given.src.rampup import rampup
    repo = URL_info(url = url, token = "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")
    metric = Metrics(repo_data = repo)
    metric.runMetrics()
    metric.json_final_obj = str(json.dumps(metric.json_final_obj, sort_keys=True, indent=4))
    runMetrics = json.loads(metric.json_final_obj, strict=False)
    rateObj.RampUp = runMetrics['Ramp Up Score']
    rateObj.Correctness = runMetrics['Correctness Score']
    rateObj.BusFactor = runMetrics['Bus Factor Score']
    rateObj.ResponsiveMaintainer = runMetrics['Reponsiveness Score']
    rateObj.LicenseScore =  runMetrics['License Score']
    
    from ZipUnzip import ZipUnzip
    zz = ZipUnzip()
    versions = svr.get_versions()
    rateObj.GoodPinningPractice = svr.parse_versions(versions)
    metric.deleteDirectory()
    # from project1given:
    #  net_score = ((0.25 * rampup_score) + (0.15 * correctness_score)+ (0.35 * bus_factor_score) + (0.25 * responsive_maintainer_score)) * license_score
    total = runMetrics['Net Score']
    if total != 0:
        total = 0.9*total + 0.1*rateObj.GoodPinningPractice
    # new total is:
    #  total = ((0.25*0.9 * rampup_score) + (0.15*0.9 * correctness_score) + (0.35*0.9 * bus_factor_score) + (0.25*0.9 * responsive_maintainer_score) + (0.1 * goodpinningpractice)) * license_score
    action.Action = PackageHistoryEntry.ActionEnum.RATE
    action.PackageMetaData = pak.metadata
    from datetime import datetime
    action.Date = datetime.now()
    pak.history.append(action)
    
    pak.rating = total
    rateObj.NetScore = total
    return rateObj.toJSON(),200

@app.route('/reset/', methods=['DELETE'])
def registryReset():
    from Packages import Packages
    pacs = Packages()
    pacs = pacs.update()
    auth = None
    auth = request.headers.get("X-Authorization")
    if(auth == None):
        return e.set("You do not have permission to reset the registry.", 401)
    
    Firestore.delete_all_package_modules()
    return pacs.delete_all()

@app.route('/package/', methods=['POST'])
def packageCreate():
    from Packages import Packages
    pacs = Packages()
    pacs = pacs.update()
    auth = None
    auth = request.headers.get("X-Authorization")
    if(auth == None):
        return e.malformed()
    jsonResponse = request.json
    data = json.loads(str(json.dumps(jsonResponse["metadata"])), strict=False)
    id = data["ID"]
    if not id:
        return e.malformed()
    read = Firestore.read(id)
    prev = None
    if read != None:
        prev = pacs.packageDictionary[read['id']]
        if prev:
            if prev.metadata.toJSON() == data:
                return e.set("Package exists already.", 403)
            else: #id needs changed
                num = 0
                newid = id
                while Firestore.read(newid) != None:
                    newid = id + str(num)
                    num = num + 1
                data["ID"] = str(newid)
                jsonResponse["metadata"] = json.loads(str(json.dumps(data)), strict=False)
    #Firestore document created in metadata.set_data
    pak.metadata = pak.metadata.set_data(jsonResponse["metadata"])
    if (pak.metadata.Name == None or pak.metadata.Version == None):
        Firestore.delete(pak.metadata.get_ID())
        return e.malformed()
    
    #Firestore document updated in data.set_data
    pak.data = pak.data.set_data(jsonResponse["data"], pak.metadata.get_ID())
    if (pak.data == None):
        if prev:
            pak.data = pak.data.set_data(prev.data.toJSON(), pak.metadata.get_ID())
        return e.unexpected()
    if (pak.data.Content == None and pak.data.URL == None):
        if prev:
            pak.data = pak.data.set_data(prev.data.toJSON(), pak.metadata.get_ID())
        return e.malformed()
    if (pak.data.Content == None): #packageIngest
        if prev:
            pak.data.Content = prev.data.Content
        Firestore.update(pak.data.toJSON(), pak.metadata.get_ID())
    if (pak.data.URL == None): #packageIngest
        if prev:
            pak.data.URL = prev.data.URL
        Firestore.update(pak.data.toJSON(), pak.metadata.get_ID())
    
    action.Action = PackageHistoryEntry.ActionEnum.CREATE
    action.PackageMetaData = pak.metadata
    from datetime import datetime
    action.Date = datetime.now()
    pak.history.append(action)
    if pak.data.URL != None:
        rateresponse = rate_by_ID(pak.metadata.get_ID(), pak)
        if rateresponse[1] != 200:
            Firestore.delete(pak.metadata.get_ID())
            return rateresponse
        if pak.rating < 0.5:
            #Firestore.delete(pak.metadata.get_ID())
            return e.set("package recieved bad rating", 400)
    
    pacs.add_package(pak)
    return pak.metadata.toJSON(), 201
    
@app.route('/package/<id>', methods=['GET', 'PUT', 'DELETE'])
def packagewID(id):
    if request.method == 'GET':
        return packageRetrieve(id)
    if request.method == 'PUT':
        return packageUpdate(id)
    if request.method == 'DELETE':
        return packageDelete(id)

def packageRetrieve(id):
    from Packages import Packages
    pacs = Packages()
    pacs = pacs.update()
    if id in pacs.packageDictionary.keys():
        pak = pacs.packageDictionary[id]
        if not pak:
            return e.unexpected()
        logging.warning(str(pak.metadata))
        logging.warning(str(pak.data))
        pak.metadata = pak.metadata.get_data()
        pak.data = pak.data.get_data(pak.metadata.get_ID())
        logging.warning(str(pak.metadata))
        logging.warning(str(pak.data))
        return {'metadata': pak.metadata.toJSON(), 'data': pak.data.toJSON()}, 200
    return e.unexpected()

def packageUpdate(id):
    auth = None
    auth = request.headers.get("X-Authorization")
    if(auth == None):
        return e.malformed()
    jsonResponse = request.json
        
    from Packages import Packages
    pacs = Packages()
    pacs = pacs.update()
    pak = pacs.packageDictionary[id]
    if not pak:
        return e.malformed()
    if (pak.metadata.Name != jsonResponse['metadata']["Name"]) or (pak.metadata.Version != jsonResponse['metadata']["Version"]) or (pak.metadata.ID != jsonResponse['metadata']["ID"]):
        return e.malformed()
    
    prev = pak
    delete_package_by_Name(pak.metadata.Name)#delete old version
    pak.metadata = pak.metadata.set_data(pak.metadata.toJSON())
    pak.data = pak.data.set_data(jsonResponse['data'], pak.metadata.get_ID())
    if(pak.data == None):
        pak.data = pak.data.set_data(prev.data.toJSON(), pak.metadata.get_ID())
        return e.malformed()
    
    action.Action = PackageHistoryEntry.ActionEnum.UPDATE
    action.PackageMetaData = pak.metadata
    from datetime import datetime
    action.Date = datetime.now()
    pak.history.append(action)
    pacs.add_package(pak)#add new version
    return {'message': "success"}, 201

def packageDelete(id):
    from Packages import Packages
    pacs = Packages()
    pacs = pacs.update()
    Firestore.delete(id)
    if not id in pacs.packageDictionary:
        return e.set("Package does not exist.", 400)
    return pacs.delete_package(id)

@app.route('/packages/', methods = ['POST'])    
def packagesList():
    auth = None
    auth = request.headers.get("X-Authorization")
    if(auth == None):
        return e.malformed()
        
    from Packages import Packages
    pacs = Packages()
    pacs = pacs.update()
    pacs.QueryArray = request.json
    pacs.QueryResult = []
    err = False
    for query in pacs.QueryArray:
        if query["Name"] == "*":
            return json.dumps(pacs.packageDictionary, default=lambda o: o.__dict__, sort_keys=True, indent=4), 200
        else:
            s = len(pacs.QueryResult)
            for pack in pacs.packageDictionary.values():
                if pack.metadata.Name == query["Name"]:
                    pacs.QueryResult.append(pack.toJSON())
                    break
            if s == len(pacs.QueryResult):
                pacs.QueryResult.append({"code": -1,"message": "An unexpected error occurred"})
                err = True
    if err:
        return json.dumps(pacs.QueryResult, default=lambda o: o.__dict__, sort_keys=True, indent=4), 500
    return json.dumps(pacs.QueryResult, default=lambda o: o.__dict__, sort_keys=True, indent=4), 200

@app.route('/package/byName/<Name>', methods=['GET', 'DELETE'])
def packagewName(Name):
    if request.method == 'GET':
        return get_package_by_Name(Name)
    if request.method == 'DELETE':
        return delete_package_by_Name(Name)

def get_package_by_Name(Name):
    from Packages import Packages
    pacs = Packages()
    pacs = pacs.update()
    for id,pack in pacs.packageDictionary.items():
        if (pack.metadata.Name == Name):
            return json.dump(pack.history, default=lambda o: o.__dict__, 
                sort_keys=True, indent=4), 200
    return e.malformed()

def delete_package_by_Name(Name):
    from Packages import Packages
    pacs = Packages()
    pacs = pacs.update()
    i = None
    for id,pack in pacs.packageDictionary.items():
        if (pack.metadata.Name == Name):
            i = id
            break
    if i:
        return packageDelete(i)
    return e.set("Package does not exist.", 400)

if __name__ == '__main__':
    app.run()