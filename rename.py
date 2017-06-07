import os
def Test1(rootDir):
    list_dirs = os.walk(rootDir)
    for root, dirs, files in list_dirs:
        i = 0
        for f in files:
            os.rename(os.path.join(root, f),os.path.join(root, "makeimage"+str(i)+".png"))
            i = i+1
Test1("image")
