import Flask-RESTful
class Packages(Resource):
    import Package
    import PackageQuery
    import Error
    self.QueryArray = []
    self.QueryResult = []
    packageDictionary = {}
    
    def post(self): #PackagesList
        auth = None
        auth = request.headers.get("X-Authorization")
        if(auth == None):
            e = new Error()
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
                    self.QueryResult.append(jsonify({"code": "-1","message": "An unexpected error occurred"},500,))
                    return jsonify(self.QueryResult), 500
        return jsonify(self.QueryResult), 200
    
    def static add_package(p):
        packageDictionary[p.metadata.get_ID()] = p
        return
    def static get_package_by_ID(id):
        if id in packageDictionary.keys():
            return jsonify(packageDictionary[id]), 200
        else:
            return 400
    def static get_package_by_Name(Name):
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
        