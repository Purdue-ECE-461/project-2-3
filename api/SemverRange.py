from ZipUnzip import ZipUnzip
import json
import re
import glob

class SemverRange(object):

    def get_versions(self):
        filepath = glob.glob('/tmp/**/package.json', 
                   recursive = True)
        semver_json = json.load(open(filepath[0], "r"))
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