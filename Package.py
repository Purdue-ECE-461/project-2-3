from flask_restful import Resource, request, reqparse
class Package(Resource):
    import MetaData
    import PackageData
    import Error
    import firestore
    data = new PackageData()
    metadata = new MetaData()
    
    def get(self):
        metadata = metadata.get_data()
        data = data.get_data()
        return {'MetaData': metadata, 'PackageData': data}, 200
    
    def post(self): #PackageCreate
        auth = None
        auth = request.headers.get("X-Authorization")
        if(auth == None):
            e = new Error()
            return e.set("Malformed request.", 400)
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('metadata', required=True)  # add args
        parser.add_argument('data', required=True)
        args = parser.parse_args()  # parse arguments to dictionary
        
        metadata = metadata.set_data(args['metadata'])
        if(metadata == None):
            e = new Error()
            return e.set("Package exists already.", 403)
        if(metadata.Name == None || metadata.Version == None || metadata.get_ID() == None):
            e = new Error()
            return e.set("Malformed request.", 400)
        
        data = data.set_data(args['data'], metadata.get_ID())
        if(data == None):
            e = new Error()
            return e.set("Package does not exist.", 403)
        if(data.Content == None || data.JSPackage == None):
            e = new Error()
            return e.set("Malformed request.", 400)
        
        return {'MetaData': metadata, 'PackageData': data}, 201
    