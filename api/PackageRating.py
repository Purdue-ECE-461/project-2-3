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
    
    def static rate_by_ID(id):
        rateObj = new PackageRating()
        pack = Packages.packageDictionary[id]
        if pack == None:
            e = new Error()
            return e.set("Malformed request.", 400)
        url = pack.data.URL
        #TODO call scoring here
        rateObj.RampUp = None
        rateObj.Correctness = None
        rateObj.BusFactor = None
        rateObj.ResponsiveMaintainer = None
        rateObj.LicenseScore = None
        rateObj.GoodPinningPractice = None
        total = None
        
        action = new PackageHistoryEntry()
        action.Action = PackageHistoryEntry.Action.RATE
        action.PackageMetaData = pack.metadata
        action.Date = datetime.now()
        pack.history.append(action)
        
        pack.rating = total
        return jsonify(rateObj),200