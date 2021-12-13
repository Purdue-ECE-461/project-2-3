import json
class PackageData(object):
    from flask import request
    Content = None
    JSProgram = None
    URL = None
    
    def get_data(self, ID):
        import firestore as Firestore
        packdict = Firestore.read(ID)
        if not packdict:
            return None
        try:
            self.Content = packdict[u"Content"]
        except:
            pass
        try:
            self.JSProgram = packdict[u"JSProgram"]
        except:
            pass
        try:
            self.URL = packdict[u"URL"]
        except:
            pass
        return self
    
    def set_data(self, data, ID):
        import firestore as Firestore
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
        j = dict()
        j["Content"] = self.Content
        j["JSProgram"] = self.JSProgram
        j["URL"] = self.URL
        j = json.dumps(j, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
        return json.loads(str(j), strict=False)
        
        