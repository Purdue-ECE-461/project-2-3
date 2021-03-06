import json
class MetaData(object):
    from flask import request
    Name = None
    Version = None
    ID = None
    
    def get_data(self):
        import firestore as Firestore
        packdict = Firestore.read(self.ID)
        self.ID = packdict['id']
        self.Name = packdict[u'Name']
        self.Version = packdict[u'Version']        
        return self
    
    def set_data(self, data):
        self.Name = data["Name"]
        self.Version = data["Version"]
        self.ID = data["ID"]
        import firestore as Firestore
        if(Firestore.create(data, self.ID) == None):
            return None
        return self
    
    def update(self, data):
        data = json.loads(data, strict=False)
        self.Name = data["Name"]
        self.Version = data["Version"]
        self.ID = data["ID"]
        import firestore as Firestore
        if(Firestore.update(data, self.ID) == None):
            return None
        return self
    
    def get_ID(self):
        return self.ID
    
    def toJSON(self):
        j = dict()
        j["Name"] = self.Name
        j["Version"] = self.Version
        j["ID"] = self.ID
        j = json.dumps(j, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
        return json.loads(str(j), strict=False)
    
    def __eq__(self, obj):
        if(obj == None):
            if (self.Name == None) and (self.Version == None) and (self.ID == None):
                return True
            else:
                return False
        if (self.Name == obj.Name) and (self.Version == obj.Version) and (self.ID == obj.ID):
            return True
        return False