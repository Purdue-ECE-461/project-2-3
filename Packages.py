from flask_restful import Resource, request, reqparse
class Packages(Resource):
    import Package
    import PackageQuery
    import Error
    self.QueryArray = []
    packageDictionary = {}
    
    def get(self): #PackagesList
        auth = None
        auth = request.headers.get("X-Authorization")
        self.QueryArray = request.get_json()
        return {},200
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
    def static delete_package_by_Name(Name):
        for id,pack in packageDictionary.items():
            if (pack.metadata.Name == Name):
                firestore.delete(id)
                del packageDictionary[id]
                return 200
        return 400
        