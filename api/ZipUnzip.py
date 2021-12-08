import base64
import zipfile
import tarfile
import shutil
import os
import time
import glob
from pathlib import Path

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
    
    def base64Encode(self, filename):
        with open(filename, 'rb') as file:
            message = file.read()
            return base64.standard_b64encode(message)
        
    def base64Decode(self, filename):
        with open(filename, 'rb') as file:
            bytes = file.read()
            #bytes = bytes.encode()
            return base64.standard_b64decode(bytes + b'==')
    
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
        os.rmdir(folder)
       
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
    test.file_zip()
    encoded = test.base64Encode("packages/underscore-master.zip")
    with open("b64test.txt", 'wb') as file:
        file.write(encoded)
    decoded = test.base64Decode("b64test.txt")
    print(decoded)
    with open("packages/underscore-master2.zip", 'wb') as file:
        file.write(decoded)
    test.file_unzip("underscore-master2.zip")
    test.file_zip()
    time.sleep(5)
    test.clean()
    
    decoded = test.base64Decode("b64apitest.txt")
    with open("packages/underscore-master3.zip", 'wb') as file:
        file.write(decoded)
    test.file_unzip("underscore-master3.zip")
    time.sleep(5)
    for file in glob.glob('packageTemp/*.zip'):
        print(file)
        os.remove(file)
    test.file_zip()
    time.sleep(5)
