class PackageRating(object):
    RampUp = None
    Correctness = None
    BusFactor = None
    ResponsiveMaintainer = None
    LicenseScore = None
    GoodPinningPractice = None
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    