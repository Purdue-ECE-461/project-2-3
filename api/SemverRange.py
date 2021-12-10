import package_moduleshelf
import semver
from ZipUnzip import ZipUnzip

class SemverRange(object):
    #assuming object is txt file
    zipun = ZipUnzip()
    zipun.file_unzip("underscore-master.zip")
    file1 = open('packageTemp/underscore/package.json', 'r')
    count = 0 #line number

    while True:
        verMajor = None
        verMinor = None
        verPatch = None

        lines = file1.readlines()
        if not lines:
            break

        for x in lines:
            if lines[count][x] == "=" & lines[count][x + 1] == "=":
                ver = semver.Version.parse(lines[count][x:])
                verMajor = ver.major
                verMinor = ver.minor
                verPatch = ver.patch
                
        count += 1
