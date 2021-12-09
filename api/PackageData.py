class PackageData(object):
    import firestore
    from flask import request
    Content = None
    JSprogram = None
    URL = None
    
    def get_data(ID):
        data = firestore.read(ID)
        if(data == None):
            return None
        self.Content = data["content"]
        self.JSprogram = data["JSprogram"]
        self.URL = data["URL"]
        return self
    
    def set_data(data, ID):
        if(firestore.update(data, ID) == None):
            return None
        self.Content = data["content"]
        self.JSprogram = data["JSprogram"]
        self.URL = data["URL"]
        return self
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
        
        