import os

def correctness(filepath):

    try:
        for dirpath, dirname, filenames in os.walk(filepath):
            for dir in dirname:
                if 'test' in dir or 'tests' in dir:
                    #test directory exits
                    return 1.0


            for file in filenames:
                if file.endswith('.js'):
                    if 'test' in file or 'tests' in file:
                        #test file exits
                        return 1.0         
                
    except:
        return 0.0

    return 0.0

if __name__=='__main__':
    print(correctness('temp'))