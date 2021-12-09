import os 

class PackageAudit (object) :

    package_name = ""
    destination_folder = ""

    def __init__ (self, _package_name, _destination_folder) :
        self.package_name = _package_name
        self.destination_folder = _destination_folder

    def audit_run (self) :
        os.system("cd " + self.package_name + " & npm audit --json > auditReport.json")

if __name__ == "__main__" :
    test = PackageAudit("mocha-master", "../")
    test.audit_run()