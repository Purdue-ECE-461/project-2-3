from flask import Flask
from flask_classful import FlaskView
app = Flask(__name__)
class PackageRating(FlaskView):
    import Packages
    import Package
    import PackageHistoryEntry
    import project1given
    from project1given import Metrics
    from project1given import URL_info

    self.RampUp = None
    self.Correctness = None
    self.BusFactor = None
    self.ResponsiveMaintainer = None
    self.LicenseScore = None
    self.GoodPinningPractice = None
    
    @route('/package/<id>/rate')
    def rate_by_ID(self, id):
        rateObj = PackageRating()
        pack = Packages.packageDictionary[id]
        if pack == None:
            e = Error()
            return e.set("Malformed request.", 400)
        url = pack.data.URL
        #TODO call scoring here
        repo = URL_info(url = url, token = None)
        metric = Metrics(repo_data = repo)
        #metric.runMetrics()

        rateObj.RampUp = metric.runMetrics().rampup_score
        rateObj.Correctness = metric.runMetrics().correctness_score
        rateObj.BusFactor = metric.runMetrics().busfactor_score
        rateObj.ResponsiveMaintainer = metric.runMetrics().responsive_maintainer_score
        rateObj.LicenseScore =  metric.runMetrics().license_score
        rateObj.GoodPinningPractice = None
        total = None
        
        action = PackageHistoryEntry()
        action.Action = PackageHistoryEntry.Action.RATE
        action.PackageMetaData = pack.metadata
        action.Date = datetime.now()
        pack.history.append(action)
        
        pack.rating = total
        return jsonify(rateObj),200