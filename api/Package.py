from flask import Flask
from flask.ext.classy import FlaskView
app = Flask(__name__)
class Package(FlaskView):
    import firestore
    import datetime
    import MetaData
    import PackageData
    import Error
    import Packages
    import PackageRating
    import PackageHistoryEntry
    import PackageQuery
    self.data = new PackageData()
    self.metadata = new MetaData()
    self.history = []
    self.rating = None
    
    @route('/package/')
    def get(self): #PackageRetrieve
        self.metadata = self.metadata.get_data()
        self.data = self.data.get_data(self.metadata.get_ID())
        return {'MetaData': self.metadata, 'PackageData': self.data}, 200
    
    def post(self): #PackageCreate
        auth = None
        auth = request.headers.get("X-Authorization")
        if(auth == None):
            e = new Error()
            return e.set("Malformed request.", 400)
        parser = reqparse.RequestParser()
        parser.add_argument('metadata', required=True)
        parser.add_argument('data', required=True)
        args = parser.parse_args()
        
        prevmeta = self.metadata
        self.metadata = self.metadata.set_data(args['metadata'])
        if(self.metadata == None):
            self.metadata = self.metadata.set_data(jsonify(prevmeta))
            e = new Error()
            return e.set("Package exists already.", 403)
        if(self.metadata.Name == None || self.metadata.Version == None || self.metadata.get_ID() == None):
            self.metadata = self.metadata.set_data(jsonify(prevmeta))            
            e = new Error()
            return e.set("Malformed request.", 400)
        
        prevdata = self.data
        self.data = self.data.set_data(args['data'], self.metadata.get_ID())
        if(self.data == None):
            self.data = self.data.set_data(jsonify(prevdata), self.metadata.get_ID())
            return {"code": -1, "message": "An error occurred while retrieving package"}, 500
        if(self.data.Content == None and self.data.URL == None):
            self.data = self.data.set_data(jsonify(prevdata), self.metadata.get_ID())
            e = new Error()
            return e.set("Malformed request.", 400)
        if (self.data.Content == None): #packageIngest
            self.data.Content = prevdata.Content
            firestore.update(jsonify(self.data), self.metadata.get_ID())
        if (self.data.URL == None): #packageIngest
            self.data.URL = prevdata.URL
            firestore.update(jsonify(self.data), self.metadata.get_ID())
        action = new PackageHistoryEntry()
        action.Action = PackageHistoryEntry.Action.CREATE
        action.PackageMetaData = self.metadata
        action.Date = datetime.now()
        self.history.append(action)
        Packages.add_package(self)
        
        rateresponse = PackageRating.rate_by_ID(self.metadata.get_ID())
        if rateresponse != 200:
            self.delete()
            return rateresponse
        if self.rating < 0.5:
            self.delete()
            e = new Error()
            return e.set("package recieved bad rating", 400)
        
        return jsonify(self.metadata), 201
    
    def put(self): #PackageUpdate
        auth = None
        auth = request.headers.get("X-Authorization")
        if(auth == None):
            e = new Error()
            return e.set("Malformed request.", 400)
        parser = reqparse.RequestParser()
        parser.add_argument('metadata', required=True)
        parser.add_argument('data', required=True)
        args = parser.parse_args()
        
        if (self.metadata.Name != args['metadata']["Name"]) or (self.metadata.Version != args['metadata']["Version"]) or (self.metadata.ID != args['metadata']["ID"]):
            return 400
        
        prevdata = self.data
        self.data = self.data.set_data(args['data'], self.metadata.get_ID())
        if(self.data == None):
            self.data = self.data.set_data(jsonify(prevdata), self.metadata.get_ID())
            return 400
        
        Packages.delete_package(self)#delete old version based on metadata
        action = new PackageHistoryEntry()
        action.Action = PackageHistoryEntry.Action.UPDATE
        action.PackageMetaData = self.metadata
        action.Date = datetime.now()
        self.history.append(action)
        Packages.add_package(self)#add new version
        return 201
        
        def delete(self): #packageDelete
            firestore.delete(self.metadata.get_ID())
            return Packages.delete_package(self)
        
        @Override
        def __eq__(self, obj):
            return self.metadata == obj.metadata
        
Package.register(app)