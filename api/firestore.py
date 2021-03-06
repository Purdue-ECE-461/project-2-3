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

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from ZipUnzip import ZipUnzip
import base64
import zipfile
import tarfile
import shutil
import os
import time
from pathlib import Path
# Use the application default credentials
zz = ZipUnzip()
decoded = zz.base64Decode("service_account.txt")
with open("/tmp/service_account.json", 'w+b') as file:
    file.write(decoded)
cred = credentials.Certificate('/tmp/service_account.json')
firebase_admin.initialize_app(cred, {
  'projectId': "ece461-p2-t3",
})

db = firestore.client()

def document_to_dict(doc):
    if not doc.exists:
        return None
    doc_dict = doc.to_dict()
    doc_dict['id'] = doc.id
    return doc_dict


def next_page(limit=10, start_after=None):
    query = db.collection(u'package_module').limit(limit).order_by(u'Name')

    if start_after:
        # Construct a new query starting at this document.
        query = query.start_after({u'Name': start_after})

    docs = query.stream()
    docs = list(map(document_to_dict, docs))

    last_name = None
    if limit == len(docs):
        # Get the last document from the results and set as the last name.
        last_name = docs[-1][u'Name']
    return docs, last_name


def read(package_module_id):
    # [START package_moduleshelf_firestore_client]
    package_module_ref = db.collection(u'package_module').document(package_module_id)
    snapshot = package_module_ref.get()
    # [END package_moduleshelf_firestore_client]
    return document_to_dict(snapshot)


def update(data, package_module_id=None):
    if(read(package_module_id)==None):
        return None
    package_module_ref = db.collection(u'package_module').document(package_module_id)
    package_module_ref.update(data)
    return document_to_dict(package_module_ref.get())

def create(data, package_module_id=None):
    if(read(package_module_id)!=None):
        print(read(package_module_id))
        return None
    package_module_ref = db.collection(u'package_module').document(package_module_id)
    package_module_ref.set(data)
    return document_to_dict(package_module_ref.get())


def delete(id):
    package_module_ref = db.collection(u'package_module').document(id)
    package_module_ref.delete()

def delete_all_package_modules():
    while True:
        package_modules, _ = next_page(limit=50)
        if not package_modules:
            break
        for package_module in package_modules:
            delete(package_module['id'])


if __name__ == "__main__" :
    zz = ZipUnzip()
    os.remove("api/service_account.txt")
    encoded = zz.base64Encode("service_account.json")
    with open("api/service_account.txt", 'w+b') as file:
        file.write(encoded)