from flask import Flask, request
import responses
import requests
from flask_classful import FlaskView, route

app = Flask(__name__)

class Packages(FlaskView):
    import Package
    import PackageQuery
    import Error
    QueryArray = []
    QueryResult = []
    packageDictionary = {}
    
    @route('/packages/')
    def post(self): #PackagesList
        auth = None
        auth = request.headers.get("X-Authorization")
        if(auth == None):
            e = Error()
            return e.set("Malformed request.", 400)
        self.QueryArray = request.get_json()
        self.QueryResult = []
        for query in self.QueryArray:
            if query.Name == "*":
                return jsonify(packageDictionary), 200
            else:
                s = self.QueryResult.size()
                for pack in packageDictionary.values():
                    if pack.metadata.Name == query.Name:
                        self.QueryResult.append(jsonify(pack))
                        break
                if s == self.QueryResult.size():
                    self.QueryResult.append({"code": -1,"message": "An unexpected error occurred"})
                    return jsonify(self.QueryResult), 500
        return jsonify(self.QueryResult), 200
    
    def add_package(self, p):
        packageDictionary[p.metadata.get_ID()] = p
        return
    
    @route('/package/<id>')
    def get_package_by_ID(self, id):
        if id in packageDictionary.keys():
            return jsonify(packageDictionary[id]), 200
        else:
            return {"code": -1, "message": "An error occurred while retrieving package"}, 500
    
    @route('/package/byName/<Name>')
    def get_package_by_Name(self, Name):
        for id,pack in packageDictionary.items():
            if (pack.metadata.Name == Name):
                return jsonify(pack.history), 200
        return 400
    
    def delete_package(self, p):
        for ID,pack in packageDictionary.items():
            if (pack == p):
                del packageDictionary[id]
                return 200
        return 400
    def delete_all(self):
        for ID,pack in packageDictionary.items():
            del packageDictionary[id]
        return 200

Packages.register(app)
client = app.test_client()
if __name__ == "__main__" :
    test = Packages()
    resp = client.post("/packages/",
                       headers={"X-Authorization": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"},
                       json={"Version": "1.2.3","Name": "*"})
    print(resp)
     