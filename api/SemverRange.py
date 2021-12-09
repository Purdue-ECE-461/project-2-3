import package_moduleshelf
import semver


class SemverRange(object):
    #assuming object is txt file
    file1 = open('requirements.txt', 'r')
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
                verMinor = ver,minor
                verPatch = ver.patch             

        count += 1
