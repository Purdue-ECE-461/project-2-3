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


from PackageRating import PackageRating
rateObj = PackageRating()
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
    return 501

@app.route('/package/<id>/rate/', methods=['GET'])
def rate_by_ID(id):
    from Packages import Packages
    pacs = Packages()
    pacs = pacs.update()
    pak = pacs.packageDictionary[id]
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
    runMetrics = json.loads(str(metric.json_final_obj), strict=False)
    rateObj.RampUp = runMetrics['Ramp Up Score']
    rateObj.Correctness = runMetrics['Correctness Score']
    rateObj.BusFactor = runMetrics['Bus Factor Score']
    rateObj.ResponsiveMaintainer = runMetrics['Reponsiveness Score']
    rateObj.LicenseScore =  runMetrics['License Score']
    versions = svr.get_versions()
    rateObj.GoodPinningPractice = svr.parse_versions(versions)
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
    pak.metadata = pak.metadata.set_data(str(json.dumps(jsonResponse["metadata"])))
    if (pak.metadata.Name == None or pak.metadata.Version == None):
        Firestore.delete(pak.metadata.get_ID())
        return e.malformed()
    
    pak.data = pak.data.set_data(str(json.dumps(jsonResponse["data"])), pak.metadata.get_ID())
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
        rateresponse = rate_by_ID(pak.metadata.get_ID())
        if rateresponse[1] != 200:
            Firestore.delete(pak.metadata.get_ID())
            return rateresponse
        if pak.rating < 0.5:
            Firestore.delete(pak.metadata.get_ID())
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
        pak.metadata = pak.metadata.get_data()
        pak.data = pak.data.get_data(pak.metadata.get_ID())
        return {'metadata': pak.metadata, 'data': pak.data}, 200
    return e.unexpected()

def packageUpdate(id):
    auth = None
    auth = request.headers.get("X-Authorization")
    if(auth == None):
        return e.malformed()
    jsonResponse = json.loads(str(request.json), strict=False)
        
    from Packages import Packages
    pacs = Packages()
    pacs = pacs.update()
    pak = pacs.packageDictionary[id]
    if not pak:
        return e.malformed()
    if (pak.metadata.Name != jsonResponse['metadata']["Name"]) or (pak.metadata.Version != jsonResponse['metadata']["Version"]) or (pak.metadata.ID != jsonResponse['metadata']["ID"]):
        return e.malformed()
    
    prev = pak
    pak.data = pak.data.set_data(jsonResponse['data'], pak.metadata.get_ID())
    if(pak.data == None):
        pak.data = pak.data.set_data(prev.data.toJSON(), pak.metadata.get_ID())
        return e.malformed()
    
    delete_package_by_Name(pak.metadata.Name)#delete old version
    
    action.Action = PackageHistoryEntry.ActionEnum.UPDATE
    action.PackageMetaData = pak.metadata
    from datetime import datetime
    action.Date = datetime.now()
    self.history.append(action)
    pacs.add_package(pak)#add new version
    return 201

def packageDelete(id):
    from Packages import Packages
    pacs = Packages()
    Firestore.delete(id)
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
            return pack.history.toJSON(), 200
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
    return e.malformed()

if __name__ == '__main__':
    app.run()