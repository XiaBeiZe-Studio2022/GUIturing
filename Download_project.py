import urllib.request
import os,shutil
from zipfile import ZipFile

def get_project(jsonurl,filename):
    reponse =urllib.request.urlopen(jsonurl).read()
    try:
        shutil.rmtree(".\\project")
    except:
        pass
    os.mkdir("project")
    with open('.\\project\\project.json','wb') as f:
        f.write(reponse)
    f=str(reponse).split('md5ext":"')[1:]
    for i in range(len(f)):
        f[i]=f[i][:f[i].find('"')]
    for i in f:
            url='https://ydschool-online.nosdn.127.net/svg/'+i
            urllib.request.urlretrieve(url,filename=os.getcwd()+"\project\\"+i)
            urllib.request.urlcleanup()
    with ZipFile(filename+".sb3", 'w') as myzip:
        a=os.listdir('.\\project\\')
        for i in a:
            myzip.write('.\\project\\'+i,arcname=i)
    shutil.rmtree(".\\project\\")
