class PackageRating(object):
    self.RampUp = None
    self.Correctness = None
    self.BusFactor = None
    self.ResponsiveMaintainer = None
    self.LicenseScore = None
    self.GoodPinningPractice = None
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