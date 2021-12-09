from flask import Flask
from flask_classful import FlaskView

app = Flask(__name__)

class Packages(FlaskView):
    import Package
    import PackageQuery
    import Error
    self.QueryArray = []
    self.QueryResult = []
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
    
    def static add_package(p):
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
    
    def static delete_package(p):
        for ID,pack in packageDictionary.items():
            if (pack == p):
                del packageDictionary[id]
                return 200
        return 400
    def static delete_all():
        for ID,pack in packageDictionary.items():
            del packageDictionary[id]
        return 200
        