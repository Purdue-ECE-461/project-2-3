from flask import Flask, request, jsonify
import responses
import requests
import json
from flask_classful import FlaskView, route
import Package
import PackageQuery
import Error
import firestore as Firestore
app = Flask(__name__)

class Packages(FlaskView):
    QueryArray = []
    QueryResult = []
    packageDictionary = {}
    
    excluded_methods = ['next_page', 'read']

    @route('/packages/')
    def post(self): #PackagesList
        package_modules, _ = Firestore.next_page()
        for package_module in package_modules:
            self.packageDictionary[package_module['id']] = Firestore.read(package_module['id'])
        auth = None
        auth = request.headers.get("X-Authorization")
        if(auth == None):
            e = Error()
            return e.set("Malformed request.", 400)
        self.QueryArray.append(json.loads(str(request.json), strict=False))
        self.QueryResult = []
        for query in self.QueryArray:
            if query['Name'] == "*":
                return jsonify(self.packageDictionary), 200
            else:
                s = self.QueryResult.size()
                for pack in self.packageDictionary.values():
                    if pack.metadata.Name == query.Name:
                        self.QueryResult.append(pack.toJSON())
                        break
                if s == self.QueryResult.size():
                    self.QueryResult.append({"code": -1,"message": "An unexpected error occurred"})
                    return jsonify(self.QueryResult), 500
        return jsonify(self.QueryResult), 200
    
    def add_package(self, p):
        self.packageDictionary[p.metadata.get_ID()] = p
        return
    
    @route('/package/<id>')
    def get_package_by_ID(self, id):
        if id in self.packageDictionary.keys():
            return self.packageDictionary[id].toJSON(), 200
        else:
            return {"code": -1, "message": "An error occurred while retrieving package"}, 500
    
    @route('/package/byName/<Name>')
    def get_package_by_Name(self, Name):
        for id,pack in self.packageDictionary.items():
            if (pack.metadata.Name == Name):
                return pack.history.toJSON(), 200
        return 400
    
    def delete_package(self, p):
        for ID,pack in self.packageDictionary.items():
            if (pack == p):
                del self.packageDictionary[ID]
                return 200
        return 400
    
    def delete_all(self):
        for ID,pack in self.packageDictionary.items():
            del self.packageDictionary[ID]
        return 200
    
Packages.register(app)
if __name__ == "__main__" :
    test = Packages()
    j = json.dumps({"Version": "1.2.3","Name": "*"})
    r = requests.Request("/packages/",
                       headers={"X-Authorization": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"},
                       json=j)
    request = r
    resp = 200
    with app.app_context():
         resp = test.post()
    print(resp[0].json)
     