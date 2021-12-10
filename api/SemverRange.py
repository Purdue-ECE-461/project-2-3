# import package_moduleshelf
# import semver
from ZipUnzip import ZipUnzip
import json

class SemverRange(object):

    def get_versions (self, zipname="underscore") :
        semver_unzip = ZipUnzip()
        semver_unzip.file_unzip(zipname + ".zip")
        semver_json = json.load(open("packageTemp/" + zipname + "/package.json", "r"))
        versions = list(semver_json["devDependencies"].values())

        return versions

    # while True:
    #     verMajor = None
    #     verMinor = None
    #     verPatch = None

    #     lines = file1.readlines()
    #     if not lines:
    #         break

    #     for x in lines:
    #         if lines[count][x] == "=" & lines[count][x + 1] == "=":
    #             ver = semver.Version.parse(lines[count][x:])
    #             verMajor = ver.major
    #             verMinor = ver.minor
    #             verPatch = ver.patch
                
    #     count += 1

if __name__ == "__main__" :
    test = SemverRange()
    print(test.get_versions())