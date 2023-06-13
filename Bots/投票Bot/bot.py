

import os
def script():
    spath = os.path.abspath("./script")
    if not(os.path.exists("./script")):
        os.mkdir(spath)
    scripts=os.listdir("./script")
    if "exit" in scripts:
        fpath=spath+"/exit"
        os.remove(fpath)
        exit()
def bot():
    pass
script()