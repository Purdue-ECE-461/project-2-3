class MetaData(object):
    import firestore
    from flask import request
    Name = None
    Version = None
    ID = None
    def get_data(self):
        data = firestore.read(self.ID)
        self.Name = data["Name"]
        self.Version = data["Version"]
        self.ID = data["ID"]
        return self
    def set_data(self, data):
        self.Name = data["Name"]
        self.Version = data["Version"]
        self.ID = data["ID"]
        if(firestore.create(data, self.ID) == None):
            return None
        return self
    def update(self, data):
        self.Name = data["Name"]
        self.Version = data["Version"]
        self.ID = data["ID"]
        if(firestore.update(data, self.ID) == None):
            return None
        return self
    def get_ID(self):
        return self.ID
    
    def __eq__(self, obj):
        if (self.Name == obj.Name) and (self.Version == obj.Version) and (self.ID == obj.ID):
            return True
        return False