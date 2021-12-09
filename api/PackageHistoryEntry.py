class PackageHistoryEntry(object):
    import User
    import MetaData
    import PackageData
    from enum import Enum
    
    ActionEnum = Enum('Action', 'CREATE UPDATE DOWNLOAD RATE')
    
    User = User
    Date = None
    PackageMetadata = MetaData
    Action = ActionEnum.CREATE
    def get_data(self):
        return self
    def set_data(self, data):
        self.User = data["User"]
        self.Date = data["Date"]
        self.PackageMetadata = data["PackageMetadata"]
        self.Action = data["Action"]
        return self
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)