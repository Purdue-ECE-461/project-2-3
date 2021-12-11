# import package_moduleshelf
# import semver
from ZipUnzip import ZipUnzip
import json
import re

class SemverRange(object):

    def get_versions(self, zipname="underscore-master"):
        semver_unzip = ZipUnzip()
        semver_unzip.file_unzip(zipname + ".zip")
        semver_json = json.load(open("packageTemp/" + zipname + "/package.json", "r"))
        versions = list(semver_json["devDependencies"].values())
        return versions
    
    def parse_versions(self, versions):
        if not versions:
            return 1.0
        count = 0.0
        for v in versions:
            m = re.search("^(~|\^)?(\d+)(\.(\d+)(\.(\d+))?)?",v)
            if m == None:
                print("unable to parse dependency version: " + v)
                continue
            verAdvRange = m.group(1)
            verMajor = m.group(2)
            verMinor = m.group(4)
            verPatch = m.group(6)
            if (verAdvRange == "~") and (verMinor != None):
                count = count + 1
                continue
            if (verAdvRange == "^") and (verMajor == "0"):
                count = count + 1
        rating = count/len(versions)
        return rating
if __name__ == "__main__" :
    test = SemverRange()
    versions = test.get_versions()
    print(test.parse_versions(versions))