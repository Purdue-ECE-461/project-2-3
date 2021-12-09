class PackageHistoryEntry(object):
    import User
    import MetaData
    import PackageData
    
    static Action = Enum('Action', 'CREATE UPDATE DOWNLOAD RATE')
    
    self.User = User()
    self.Date = None
    self.PackageMetadata = MetaData()
    self.Action = Action.CREATE
    def get_data():
        return self
    def set_data(data):
        self.User = data["User"]
        self.Date = data["Date"]
        self.PackageMetadata = data["PackageMetadata"]
        self.Action = data["Action"]
        return self