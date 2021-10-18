import json
import requests
import os
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

from gitclone import clone, cleartemp
from rampup import rampup
from busfactor import busFactor
from responseMaintainer import responseMaintainer
from licensing import licensing
from correctness import correctness

import logging

class Metrics():

    gitsrc = None
    repo = None
    filepath = os.path.join(script_dir, "./temp")

    def __init__(self, repo_data):
        self.repo = repo_data
        self.gitsrc = repo_data.data
        self.json_final_obj = None
        self.compatible_license = {
                        "GPL-2.0-only": True,
                        "GPL-2.0-or-later": True,
                        "GPL-3.0-only": True,
                        "LGPL-2.1-only": True,
                        "LGPL-2.1-or-later": True,
                        "LGPL-3.0-only": True, 
                        "BSL-1.0": True, 
                        "CECILL-2.0": True, 
                        "ClArtistic": True, 
                        "EUDatagrid": True, 
                        "EFL-2.0": True,
                        "Intel": True,
                        "Vim": True,
                        "Zlib": True,
                        "iMatix": True,
                        "BSD-3-Clause-Modification": True,
                        "OLDAP-2.7": True,
                        "SMLNJ": True,
                        "Ruby": True,
                        "W3C": True,
                        "X11": True,
                        "MIT": True,
                        "ZPL-2.0": True,
                        "eCos-2.0": True,
                        "Apache-2.0": True
                    }

    def runMetrics(self):

        if (self.gitsrc == None):
            logging.warning("Github source not found, moving on...")
            return
        # test ################
        self.createDirectory()
        rampup_score = self.runRampup()
        # rampup_score = 0.0
        correctness_score = self.runCorrectness() 
        bus_factor_score = self.runBusFactor()
        responsive_maintainer_score = self.runResponseMaintainer()
        license_score = self.runLicensing()

        net_score = self.runNetScore(rampup_score, correctness_score, bus_factor_score, responsive_maintainer_score, license_score)
        # print("bus factor: {}".format(busfactorscore))
        # print(f'{self.repo.url} {net_score:.1f} {rampup_score:.1f} {correctness_score} {bus_factor_score:.1f} {responsive_maintainer_score:.1f} {license_score:.1f}')
        self.json_final_obj = {
                'URL':self.repo.url, 
                'Net Score': net_score, 
                'Ramp Up Score': rampup_score, 
                'Correctness Score': correctness_score, 
                'Bus Factor Score': bus_factor_score,
                'Reponsiveness Score': responsive_maintainer_score,
                'License Score': license_score
                }
        self.deleteDirectory()
       ############################# 

    def createDirectory(self):
        try:
            os.makedirs(self.filepath)
        except FileExistsError:
            # directory already exists
            pass
        clone(self.gitsrc["clone_url"], self.filepath)

    def deleteDirectory(self):
        cleartemp(self.filepath)

    def runRampup(self):
        return rampup(self.filepath)

    def runCorrectness(self):
        return correctness(self.filepath)

    def runBusFactor(self):
        return busFactor(self.repo.num_contributors)

    def runResponseMaintainer(self):
        return responseMaintainer(self.repo.issues)

    def runLicensing(self):
        return licensing(self.repo.license, self.compatible_license)

    def getJsonOutput(self):
        return self.json_final_obj

    def runNetScore(self, rampup_score, correctness_score, bus_factor_score, responsive_maintainer_score, license_score):
        '''
        Net Score
        '''
        net_score =  ((0.25 * rampup_score) + (0.15 * correctness_score)+ (0.35 * bus_factor_score) + (0.25 * responsive_maintainer_score)) * license_score #license is 0 or 1
        return net_score


# if __name__ == "__main__":
#     gitsrc = "{\"id\":275763026,\"node_id\":\"MDEwOlJlcG9zaXRvcnkyNzU3NjMwMjY=\",\"name\":\"react-native-app\",\"full_name\":\"Abhi-Balijepalli\/react-native-app\",\"private\":false,\"owner\":{\"login\":\"Abhi-Balijepalli\",\"id\":57305830,\"node_id\":\"MDQ6VXNlcjU3MzA1ODMw\",\"avatar_url\":\"https:\/\/avatars.githubusercontent.com\/u\/57305830?v=4\",\"gravatar_id\":\"\",\"url\":\"https:\/\/api.github.com\/users\/Abhi-Balijepalli\",\"html_url\":\"https:\/\/github.com\/Abhi-Balijepalli\",\"followers_url\":\"https:\/\/api.github.com\/users\/Abhi-Balijepalli\/followers\",\"following_url\":\"https:\/\/api.github.com\/users\/Abhi-Balijepalli\/following{\/other_user}\",\"gists_url\":\"https:\/\/api.github.com\/users\/Abhi-Balijepalli\/gists{\/gist_id}\",\"starred_url\":\"https:\/\/api.github.com\/users\/Abhi-Balijepalli\/starred{\/owner}{\/repo}\",\"subscriptions_url\":\"https:\/\/api.github.com\/users\/Abhi-Balijepalli\/subscriptions\",\"organizations_url\":\"https:\/\/api.github.com\/users\/Abhi-Balijepalli\/orgs\",\"repos_url\":\"https:\/\/api.github.com\/users\/Abhi-Balijepalli\/repos\",\"events_url\":\"https:\/\/api.github.com\/users\/Abhi-Balijepalli\/events{\/privacy}\",\"received_events_url\":\"https:\/\/api.github.com\/users\/Abhi-Balijepalli\/received_events\",\"type\":\"User\",\"site_admin\":false},\"html_url\":\"https:\/\/github.com\/Abhi-Balijepalli\/react-native-app\",\"description\":\"React Native App (Authentication, navigation, simple UI)\",\"fork\":false,\"url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\",\"forks_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/forks\",\"keys_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/keys{\/key_id}\",\"collaborators_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/collaborators{\/collaborator}\",\"teams_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/teams\",\"hooks_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/hooks\",\"issue_events_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/issues\/events{\/number}\",\"events_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/events\",\"assignees_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/assignees{\/user}\",\"branches_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/branches{\/branch}\",\"tags_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/tags\",\"blobs_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/git\/blobs{\/sha}\",\"git_tags_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/git\/tags{\/sha}\",\"git_refs_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/git\/refs{\/sha}\",\"trees_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/git\/trees{\/sha}\",\"statuses_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/statuses\/{sha}\",\"languages_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/languages\",\"stargazers_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/stargazers\",\"contributors_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/contributors\",\"subscribers_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/subscribers\",\"subscription_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/subscription\",\"commits_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/commits{\/sha}\",\"git_commits_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/git\/commits{\/sha}\",\"comments_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/comments{\/number}\",\"issue_comment_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/issues\/comments{\/number}\",\"contents_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/contents\/{+path}\",\"compare_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/compare\/{base}...{head}\",\"merges_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/merges\",\"archive_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/{archive_format}{\/ref}\",\"downloads_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/downloads\",\"issues_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/issues{\/number}\",\"pulls_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/pulls{\/number}\",\"milestones_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/milestones{\/number}\",\"notifications_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/notifications{?since,all,participating}\",\"labels_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/labels{\/name}\",\"releases_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/releases{\/id}\",\"deployments_url\":\"https:\/\/api.github.com\/repos\/Abhi-Balijepalli\/react-native-app\/deployments\",\"created_at\":\"2020-06-29T07:35:20Z\",\"updated_at\":\"2021-05-16T18:45:09Z\",\"pushed_at\":\"2021-05-16T18:41:42Z\",\"git_url\":\"git:\/\/github.com\/Abhi-Balijepalli\/react-native-app.git\",\"ssh_url\":\"git@github.com:Abhi-Balijepalli\/react-native-app.git\",\"clone_url\":\"https:\/\/github.com\/Abhi-Balijepalli\/react-native-app.git\",\"svn_url\":\"https:\/\/github.com\/Abhi-Balijepalli\/react-native-app\",\"homepage\":\"\",\"size\":2869,\"stargazers_count\":0,\"watchers_count\":0,\"language\":\"JavaScript\",\"has_issues\":true,\"has_projects\":true,\"has_downloads\":true,\"has_wiki\":true,\"has_pages\":false,\"forks_count\":0,\"mirror_url\":null,\"archived\":false,\"disabled\":false,\"open_issues_count\":0,\"license\":null,\"allow_forking\":true,\"forks\":0,\"open_issues\":0,\"watchers\":0,\"default_branch\":\"master\",\"temp_clone_token\":null,\"network_count\":0,\"subscribers_count\":1}"
#     metrics = Metrics(gitsrc)

#     # metrics.runMetrics()
#     # metrics.deleteDirectory()

#     metrics.runBusFactor()
