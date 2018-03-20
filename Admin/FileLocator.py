import os

def locate(filename):
    
    cwd = os.getcwd()
    for r,d,f in os.walk(cwd):
        for files in f:
            if files == filename:
                path = os.path.join(r,files)
    
    return(path)