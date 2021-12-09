import os 

class PackageAudit (object) :

    package_filepath = ""
    destination_folder = ""

    def __init__ (self, _package_filepath, _destination_folder) :
        self.package_filepath = _package_filepath
        self.destination_folder = _destination_folder

    def audit_run (self) :
        os.system("env/bin/activate & cd " + self.package_filepath + " & npm audit --json | npm-audit-html --output " + self.destination_folder + "auditReport.html")

if __name__ == "__main__" :
    test = PackageAudit("packageTemp", "../")
    test.audit_run()
