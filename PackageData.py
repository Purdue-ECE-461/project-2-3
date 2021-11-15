class PackageData(object):
    import firestore
    from flask import request
    self.Content = None
    self.JSProgram = None
    self.URL = None
    def get_data(ID):
        data = firestore.read(ID)
        self.Content = data["content"]
        self.JSprogram = data["JSprogram"]
        self.URL = data["URL"]
        return self
    def set_data(data, ID):
        self.Content = data["content"]
        self.JSprogram = data["JSprogram"]
        self.URL = data["URL"]
        prevdata = firestore.read(ID)
        prevdata["content"] = self.Content
        prevdata["JSprogram"] = self.JSprogram
        prevdata["URL"] = self.URL
        if(firestore.update(data, self.ID) == None)
            return None
        return self
        
        
        