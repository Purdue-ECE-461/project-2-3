from flask import Flask, request, jsonify
import responses
import requests
import json
import Package
import PackageQuery
from Error import Error
e = Error()
import firestore as Firestore

app = Flask(__name__)
class Packages(object):
    QueryArray = []
    QueryResult = []
    packageDictionary = dict()
    
    def update(self):
        from Package import Package
        package_modules, _ = Firestore.next_page()
        for package_module in package_modules:
            pack = Package()
            pack.metadata.ID = package_module['id']
            pack = pack.get_self(package_module['id'])
            self.packageDictionary[pack.metadata.get_ID()] = pack
        return self

    def add_package(self, p):
        self.packageDictionary[p.metadata.get_ID()] = p
        return
    
    def delete_package(self, id):
        if id in self.packageDictionary:
            del self.packageDictionary[id]
            return {'message': "success"}, 200
        return e.noPack()
    
    def delete_all(self):
        self.packageDictionary = dict()
        return {'message': "success"}, 200

if __name__ == "__main__" :
    from main import packagesList
    j = json.dumps({"Version": "1.2.3","Name": "*"})
    r = requests.Request('POST', "/packages/",
                       headers={"X-Authorization": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"},
                       json=j)
    request = r
    resp = 200
    with app.app_context():
         resp = packagesList(request)
    print(resp[0])
     