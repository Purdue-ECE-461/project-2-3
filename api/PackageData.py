import json
class PackageData(object):
    from flask import request
    Content = None
    JSProgram = None
    URL = None
    
    def get_data(self, ID):
        import firestore as Firestore
        data = Firestore.read(ID)
        if(data == None):
            return None
        self.Content = data["Content"]
        self.JSProgram = data["JSProgram"]
        self.URL = data["URL"]
        return self
    
    def set_data(self, data, ID):
        import firestore as Firestore
        data = json.loads(str(data), strict=False)
        if(Firestore.update(data, ID) == None):
            return None
        try:
            self.Content = data["Content"]
        except:
            pass
        try:
            self.JSProgram = data["JSProgram"]
        except:
            pass
        try:
            self.URL = data["URL"]
        except:
            pass
        return self
    
    def toJSON(self):
        j = json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
        return json.loads(str(j), strict=False)
        
        