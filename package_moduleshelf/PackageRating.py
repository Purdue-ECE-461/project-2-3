class PackageRating(object):
    import Packages
    import Package
    import PackageHistoryEntry
    import project1given
    self.RampUp = None
    self.Correctness = None
    self.BusFactor = None
    self.ResponsiveMaintainer = None
    self.LicenseScore = None
    self.GoodPinningPractice = None
    self.packageID = None
    
    def static rate_by_ID(id):
        rateObj = new PackageRating()
        rateObj.packageID = id
        pack = Packages.get_package_by_ID(id)
        #TODO call scoring here
        rateObj.RampUp = None
        rateObj.Correctness = None
        rateObj.BusFactor = None
        rateObj.ResponsiveMaintainer = None
        rateObj.LicenseScore = None
        rateObj.GoodPinningPractice = None
        
        action = new PackageHistoryEntry()
        action.Action = PackageHistoryEntry.Action.RATE
        action.PackageMetaData = pack.metadata
        action.Date = datetime.now()
        pack.history.append(action)
        return rateObj
    
    def get_data():
        return self
    def set_data(data):
        self.RampUp = data["RampUp"]
        self.Correctness = data["Correctness"]
        self.BusFactor = data["BusFactor"]
        self.ResponsiveMaintainer = data["ResponsiveMaintainer"]
        self.LicenseScore = data["LicenseScore"]
        self.GoodPinningPractice = data["GoodPinningPractice"]
        return self
    def get_RampUp():
        return self.RampUp
    def get_Correctness():
        return self.Correctness
    def get_BusFactor():
        return self.BusFactor
    def get_ResponsiveMaintainer():
        return self.ResponsiveMaintainer
    def get_LicenseScore():
        return self.LicenseScore
    def get_GoodPinningPractice():
        return self.GoodPinningPractice