import json
class MetaData(object):
    from flask import request
    Name = None
    Version = None
    ID = None
    def get_data(self):
        import firestore as Firestore
        data = json.loads(str(Firestore.read(self.ID)))
        self.Name = data["Name"]
        self.Version = data["Version"]
        self.ID = data["ID"]
        return self
    def set_data(self, data):
        print(data)
        data = json.loads(str(data))
        self.Name = data['Name']
        self.Version = data['Version']
        self.ID = data['ID']
        import firestore as Firestore
        if(Firestore.create(data, self.ID) == None):
            return None
        return self
    def update(self, data):
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
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    def __eq__(self, obj):
        if (self.Name == obj.Name) and (self.Version == obj.Version) and (self.ID == obj.ID):
            return True
        return False