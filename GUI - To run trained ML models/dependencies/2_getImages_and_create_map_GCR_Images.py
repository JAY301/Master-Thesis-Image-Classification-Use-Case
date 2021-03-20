# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 10:41:10 2018



@version edit:jayatilake.s (june 13)
"""

#required liabraries
import urllib.request
import re
import pandas as pd
import os
import sys
import base64
paths_of_files=[]
#%%

#required variables for authentication
username=(sys.argv[1])
password = base64.b64decode(sys.argv[2])
password=password.decode()


top_level_url = "http://c3dbfiles.pg.com:8080/"


#password manager for authentication
password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()


#use pg credentials here
password_mgr.add_password(None, top_level_url, username, password)
handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
opener = urllib.request.build_opener(handler)
opener.open("http://c3dbfiles.pg.com:8080/")
urllib.request.install_opener(opener)

#importing dataset
dataset=pd.read_csv("dependencies\data.csv", sep='\t',  encoding='utf-8')   

#base url
link="http://c3dbfiles.pg.com:8080/view.php?id="



#itereate over each case in dataset
for case in dataset["CASE_ID"]:
   
    if not os.path.exists("dependencies\\dataset\\images\\"+case):
    #    case url
        src=link+case
    #    fetching the webpage for the case
        webpage = urllib.request.urlopen(src)
        html = webpage.read().decode('utf-8')
           
    #    getting list of images
        pattern = re.compile (r'<img [^>]*src="([^"]+)')
        images = pattern.findall(html) 
        
    #    iterate over each image in the list, download it and store in case's directory
        if images:
            
            os.makedirs("dependencies\\dataset\\images\\"+case)
            for img in images:
                img_id=img.split("file=")[-1]
                img_url=src+"&file="+img_id
                urllib.request.urlretrieve(img_url, "dependencies\\dataset\\images\\"+ case+"\\"+img_id+".jpg")

    
    #print('Images for {} are saved'.format(case))
#%%

call(["python", "dependencies/3_metadata_removal__v2"])
