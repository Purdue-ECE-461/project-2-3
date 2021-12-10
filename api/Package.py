from flask import Flask, request, jsonify
import responses
import requests
import json
from flask_classful import FlaskView, route
app = Flask(__name__)
class Package(FlaskView):
    import firestore as Firestore
    import datetime
    from MetaData import MetaData
    from PackageData import PackageData
    import Error
    import Packages
    import PackageRating
    from PackageHistoryEntry import PackageHistoryEntry
    import PackageQuery
    data = PackageData()
    metadata = MetaData()
    history = []
    rating = None
    
    def delete(self): #packageDelete
        import firestore as Firestore
        from Packages import Packages
        Firestore.delete(self.metadata.get_ID())
        paks = Packages()
        return paks.delete_package(p = self)
    
    @route('/package/')
    def get(self): #PackageRetrieve
        self.metadata = self.metadata.get_data()
        self.data = self.data.get_data(self.metadata.get_ID())
        return {'MetaData': self.metadata, 'PackageData': self.data}, 200
    
    def post(self): #PackageCreate
        auth = None
        auth = request.headers.get("X-Authorization")
        if(auth == None):
            from Error import Error
            e = Error()
            return e.set("Malformed request.", 400)
        jsonResponse = json.loads(str(request.json), strict=False)
        
        prevmeta = self.metadata
        self.metadata = self.metadata.set_data(str(
                json.dumps(jsonResponse["metadata"])))
        if(self.metadata == None):
            from MetaData import MetaData
            self.metadata = MetaData()
            self.metadata = self.metadata.set_data(prevmeta.toJSON())
            from Error import Error
            e = Error()
            return e.set("Package exists already.", 403)
        if(self.metadata.Name == None or self.metadata.Version == None or self.metadata.get_ID() == None):
            self.metadata = self.metadata.set_data(prevmeta.toJSON())
            from Error import Error
            e = Error()
            return e.set("Malformed request.", 400)
        
        prevdata = self.data
        self.data = self.data.set_data(str(
                json.dumps(jsonResponse["data"])), self.metadata.get_ID())
        if(self.data == None):
            from PackageData import PackageData
            self.data = PackageData()
            self.data = self.data.set_data(prevdata.toJSON(), self.metadata.get_ID())
            return {"code": -1, "message": "An error occurred while retrieving package"}, 500
        if(self.data.Content == None and self.data.URL == None):
            self.data = self.data.set_data(prevdata.toJSON(), self.metadata.get_ID())
            from Error import Error
            e = Error()
            return e.set("Malformed request.", 400)
        if (self.data.Content == None): #packageIngest
            self.data.Content = prevdata.Content
            import firestore as Firestore
            Firestore.update(self.data.toJSON(), self.metadata.get_ID())
        if (self.data.URL == None): #packageIngest
            self.data.URL = prevdata.URL
            import firestore as Firestore
            Firestore.update(self.data.toJSON(), self.metadata.get_ID())
        
        from PackageHistoryEntry import PackageHistoryEntry
        action = PackageHistoryEntry()
        action.Action = PackageHistoryEntry.ActionEnum.CREATE
        action.PackageMetaData = self.metadata
        from datetime import datetime
        action.Date = datetime.now()
        self.history.append(action)
        from Packages import Packages
        pacs = Packages()
        pacs.add_package(p = self)
        if self.data.URL != None:
            from PackageRating import PackageRating
            pr = PackageRating()
            rateresponse = pr.rate_by_ID(id = self.metadata.get_ID())
            if rateresponse[1] != 200:
                self.delete()
                return rateresponse
            if self.rating < 0.5:
                self.delete()
                from Error import Error
                e = Error()
                return e.set("package recieved bad rating", 400)
            
        return self.metadata.toJSON(), 201
    
    def put(self): #PackageUpdate
        auth = None
        auth = request.headers.get("X-Authorization")
        if(auth == None):
            from Error import Error
            e = Error()
            return e.set("Malformed request.", 400)
        jsonResponse = json.loads(str(request.json), strict=False)
        
        if (self.metadata.Name != jsonResponse['metadata']["Name"]) or (self.metadata.Version != jsonResponse['metadata']["Version"]) or (self.metadata.ID != jsonResponse['metadata']["ID"]):
            return 400
        
        prevdata = self.data
        self.data = self.data.set_data(jsonResponse['data'], self.metadata.get_ID())
        if(self.data == None):
            self.data = self.data.set_data(prevdata.toJSON(), self.metadata.get_ID())
            return 400
        
        from Packages import Packages
        Packages.delete_package(self)#delete old version based on metadata
        from PackageHistoryEntry import PackageHistoryEntry
        action = PackageHistoryEntry()
        action.Action = PackageHistoryEntry.ActionEnum.UPDATE
        action.PackageMetaData = self.metadata
        from datetime import datetime
        action.Date = datetime.now()
        self.history.append(action)
        Packages.add_package(self)#add new version
        return 201
        
        def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__, 
                sort_keys=True, indent=4)

        def __eq__(self, obj):
            return self.metadata == obj.metadata
        
Package.register(app)
if __name__ == "__main__" :
    test = Package()
    jcreate = '''
    {
    	"metadata": {
    		"Name": "Underscore",
    		"Version": "1.0.0",
    		"ID": "underscore"
    	},
    	"data": {
    		"Content": "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",
    		"JSProgram": "if (process.argv.length === 7) {\nconsole.log('\''Success'\'')\nprocess.exit(0)\n} else {\nconsole.log('\''Failed'\'')\nprocess.exit(1)\n}\n"
    	}
    }'''
    jingest = '''
    {
    	"metadata": {
    		"Name": "Underscore",
    		"Version": "1.0.0",
    		"ID": "underscore"
    	},
    	"data": {
            "URL": "https://github.com/jashkenas/underscore",
    		"JSProgram": "if (process.argv.length === 7) {\nconsole.log('\''Success'\'')\nprocess.exit(0)\n} else {\nconsole.log('\''Failed'\'')\nprocess.exit(1)\n}\n"
    	}
    }'''
    
    r = requests.Request("/packages/",
                       headers={"X-Authorization": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"},
                       json=jcreate)
    request = r
    resp = 200
    with app.app_context():
         resp = test.post()
    print(resp)
    test.delete()
    r = requests.Request("/packages/",
                       headers={"X-Authorization": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"},
                       json=jingest)
    request = r
    resp = 200
    with app.app_context():
         resp = test.post()
    print(resp)
     