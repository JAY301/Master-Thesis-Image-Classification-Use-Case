# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 08:36:07 2019

@author: jayatilake.s

this takes MAP_gcrCodes_images and outputs the relavent GCR code once the image name is inputted 

"""

import pandas as pd
import os
import sys

map_df = pd.read_csv('dependencies/Map_GCR_with_ImageNames.csv')
map_GCR_text_df = pd.read_csv("data.csv", sep='\t',  encoding='utf-8')  
image_name=''
gcr_code=''
complaint_text=''

#latest addition.. easy way, also put these in the data.csv.. but this is last minute, so it could be an addition 
#later
image_name =os.path.normpath(sys.argv[1])#input
#inFile =r'Fastening_Aug_Sep_Heidi.xlsx'
inFile =os.path.normpath(sys.argv[2])# input()
#reads the file
df=pd.read_excel(inFile,header=27,)

#puts "unkown" for empty values
df=df.fillna("unknown")
#merges each contact summary into one line
df["Contact Summary English1"]=[x.replace("\n"," ").replace("\t"," ") for x in df["Contact Summary English1"]]
df['Product_size']=df['Product Size']
df['Production_code']=df['Production Code']

gcr_code=map_df[map_df.loc[:,'Image_ID']==image_name].Case_ID.to_string(index=False)
complaint_text=map_GCR_text_df[map_GCR_text_df.loc[:,'CASE_ID']==gcr_code].ContactSummaryEnglish1.values[0]
Product_size=df[df.loc[:,'Internal Case Id']==gcr_code].Product_size.to_string(index=False)
Production_code=df[df.loc[:,'Internal Case Id']==gcr_code].Production_code.to_string(index=False)

print('Case ID : {} for Image ID: {}'.format(gcr_code,image_name))
print('Product Size:: '+ Product_size)
print('Production Code:: '+ Production_code)
print('Text:: '+ complaint_text)
