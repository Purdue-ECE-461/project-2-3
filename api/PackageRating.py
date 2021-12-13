import json
class PackageRating(object):
    RampUp = None
    Correctness = None
    BusFactor = None
    ResponsiveMaintainer = None
    LicenseScore = None
    GoodPinningPractice = None
    NetScore = None
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
if __name__ == "__main__" :
    from main import rate_by_ID
    rate_by_ID('underscore')