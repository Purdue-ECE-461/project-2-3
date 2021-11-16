class MetaData(object):
    import firestore
    from flask import request
    self.Name = None
    self.Version = None
    self.ID = None
    def get_data():
        data = firestore.read(self.ID)
        self.Name = data["name"]
        self.Version = data["Version"]
        self.ID = data["ID"]
        return self
    def set_data(data):
        self.Name = data["name"]
        self.Version = data["Version"]
        self.ID = data["ID"]
        if(firestore.create(data, self.ID) == None)
            return None
        return self
    def update(data):
        self.Name = data["name"]
        self.Version = data["Version"]
        self.ID = data["ID"]
        if(firestore.update(data, self.ID) == None)
            return None
        return self
    def get_ID():
        return self.ID