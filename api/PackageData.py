class PackageData(object):
    import firestore
    from flask import request
    self.Content = None
    self.JSprogram = None
    self.URL = None
    
    def get_data(ID):
        data = firestore.read(ID)
        if(data == None)
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
        
        
        