
import base64
import zipfile
from tempfile import mkdtemp
from pathlib import Path
class ZipUnzip :
    def __file_type_checker (self, filename) :
        if filename.endswith(".zip") :
            return True
        else :
            return False
    def base64Encode(self, filename):
        with open(filename, 'rb') as file:
            message = file.read()
            bytes = base64.standard_b64encode(message)
            return bytes.decode()
    def base64Decode(self, bytes):
        bytes = bytes.encode()
        return base64.standard_b64decode(bytes)
    def zipping(self, files, name):
        with ZipFile(name + '.zip', 'w') as myzip:
            for filename in files:
                myzip.write(filename)
    def unzipping(self,zipfname):
        with zipfile.ZipFile(zipfname, 'r') as zip_ref:
            path = mkdtemp()
            zip_ref.extractall(path)
            return path
if __name__ == "__main__" :
    test = ZipUnzip()
    #test.file_type_checker("test.zip")
    #zipdirectory = test.unzipping("test.zip")
    #p = Path(zipdirectory)
    #files = []
    #for child in p: files.append(child.filename)
    #test.zipping(files, "test2")
    #decodedfile = test.base64Decode(test.base64Encode(files[0]))
    file = Path("b64test.txt")
    bytes = file.open().read()
    decodedfile = base64.standard_b64decode(bytes)
    print(decodedfile)