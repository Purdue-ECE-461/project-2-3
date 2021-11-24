import zipfile
import tarfile
import shutil
import os
import time 

class ZipUnzip :
    has_zip = 1
    has_tar = 2
    has_non = 0

    def file_type_checker (self, filename) :
        if filename.endswith(".zip") :
            return self.has_zip
        elif filename.endswith(".tar.gz") :
            return self.has_tar
        else :
            return self.has_non

    # This code pulled from https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder
    def clean (self) :
        folder = 'packageTemp'

        for filename in os.listdir(folder) :
            file_path = os.path.join(folder, filename)

            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def file_zip (self) :
        for directory in os.walk("packageTemp") :
            entry = directory

        path = entry[0]
        filename = entry[0].split("\\")[-1]
    
        try :
            shutil.make_archive(filename, "zip", path)
            shutil.move(filename + ".zip", "packageTemp")
            print("Archive created!")
        except :
            print("Archive could not be created.")
            return 

    def file_unzip (self, filename) :
        filetype = self.file_type_checker(filename)

        if filetype == self.has_zip :
            unzipper = zipfile.ZipFile("packages/" + filename, "r")
            unzipper.extractall("packageTemp")
            print("Package extracted!")

            return True
        elif filetype == self.has_tar :
            print("Filetype not supported.")

            return False
        elif filetype == self.has_non :
            print("Filetype not supported.")

            return False

if __name__ == "__main__" :
    test = ZipUnzip()
    test.file_unzip("Fraction-Approximation-master.zip")
    test.file_zip()
    time.sleep(5)
    test.clean()