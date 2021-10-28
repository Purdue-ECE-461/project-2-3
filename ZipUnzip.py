
class ZipUnzip :

    def __file_type_checker (self, filename) :
        if filename.endswith(".zip") :
            return True
        else :
            return False

if __name__ == "__main__" :
    test = ZipUnzip()
    test.file_type_checker("test.zip")