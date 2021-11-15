import Flask-RESTful
class Package(Resource):
    import MetaData
    import PackageData
    import Error
    import firestore
    import datetime
    self.data = new PackageData()
    self.metadata = new MetaData()
    self.history = []
    
    def get(self): #PackageRetrieve
        self.metadata = self.metadata.get_data()
        self.data = self.data.get_data()
        return {'MetaData': self.metadata, 'PackageData': self.data}, 200
    
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
        
        self.metadata = self.metadata.set_data(args['metadata'])
        if(self.metadata == None):
            e = new Error()
            return e.set("Package exists already.", 403)
        if(self.metadata.Name == None || self.metadata.Version == None || self.metadata.get_ID() == None):
            e = new Error()
            return e.set("Malformed request.", 400)
        
        self.data = self.data.set_data(args['data'], self.metadata.get_ID())
        if(self.data == None):
            e = new Error()
            return e.set("Package does not exist.", 403)
        if(self.data.Content == None || self.data.JSPackage == None):
            e = new Error()
            return e.set("Malformed request.", 400)
        
        action = new PackageHistoryEntry()
        action.Action = PackageHistoryEntry.Action.CREATE
        action.PackageMetaData = self.metadata
        action.Date = datetime.now()
        self.history.append(action)
        Packages.add_package(self)
        return {'MetaData': self.metadata, 'PackageData': self.data}, 201
    