from flask import Flask
from flask_classful import FlaskView, route
import json
app = Flask(__name__)
class PackageRating(FlaskView):
    import Packages
    import Package
    import PackageHistoryEntry
    import project1given
    import project1given.src
    import project1given.src.busfactor
    import project1given.src.correctness
    import project1given.src.gitclone
    import project1given.src.URL_info
    import project1given.src.licensing
    import project1given.src.metrics
    import project1given.src.rampup
    import project1given.src.responseMaintainer

    RampUp = None
    Correctness = None
    BusFactor = None
    ResponsiveMaintainer = None
    LicenseScore = None
    GoodPinningPractice = None
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    @route('/package/<id>/rate')
    def rate_by_ID(self, id):
        rateObj = PackageRating()
        from Packages import Packages
        pacs = Packages()
        pack = pacs.packageDictionary[id]
        if pack == None:
            from Error import Error
            e = Error()
            return e.set("Malformed request.", 400)
        url = pack.data.URL
        #TODO call scoring here
        from project1given.src.busfactor import busFactor
        from project1given.src.correctness import correctness
        from project1given.src.gitclone import clone
        from project1given.src.URL_info import URL_info
        from project1given.src.licensing import licensing
        from project1given.src.metrics import Metrics
        from project1given.src.rampup import rampup
        repo = URL_info(url = url, token = None)
        metric = Metrics(repo_data = repo)
        metric.runMetrics()
        print(metric.json_final_obj)
        runMetrics = json.loads(str(metric.json_final_obj), strict=False)
        rateObj.RampUp = runMetrics['Ramp Up Score']
        rateObj.Correctness = runMetrics['Correctness Score']
        rateObj.BusFactor = runMetrics['Bus Factor Score']
        rateObj.ResponsiveMaintainer = runMetrics['Reponsiveness Score']
        rateObj.LicenseScore =  runMetrics['License Score']
        rateObj.GoodPinningPractice = None
        total = None
        
        action = PackageHistoryEntry()
        action.Action = PackageHistoryEntry.ActionEnum.RATE
        action.PackageMetaData = pack.metadata
        action.Date = datetime.now()
        pack.history.append(action)
        
        pack.rating = total
        return rateObj.toJSON(),200