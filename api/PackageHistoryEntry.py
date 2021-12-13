import json
class PackageHistoryEntry(object):
    import User
    from enum import Enum
    
    ActionEnum = Enum('Action', 'CREATE UPDATE DOWNLOAD RATE')
    
    User = None
    Date = None
    Action = ActionEnum.CREATE
    
    def get_data(self):
        j = dict()
        j["User"] = self.User
        j["Date"] = self.Date
        j["Action"] = str(self.Action)
        return j
    
    def set_data(self, data):
        self.User = data["User"]
        self.Date = data["Date"]
        self.Action = data["Action"]
        return self
    
    def get_self(self, ID):
        import firestore as Firestore
        packdict = Firestore.read(ID)
        return json.loads(packdict["history"])
        
    def toJSON(self):
        return json.dumps(self.get_data(), sort_keys=True, indent=4)