# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 09:45:40 2019

@author: jayatilake.s

karin's request:
	1. make another column/s as predicted failure mode,no of each FET;BET;TT;Other
		in obiee report as to what it the predicted failure mode?
	2. make a matrix as per in the email.
"""

import pandas as pd
import os
import sys
import numpy as np

map_df = pd.read_csv('dependencies/Map_GCR_with_ImageNames.csv')
map_GCR_text_df = pd.read_csv("dependencies/data.csv", sep='\t',  encoding='utf-8')	 
classified_images_df=pd.read_csv('dependencies/Classified_Images_stage_IIA.csv', sep='\t',	encoding='latin-1')

image_name=''
gcr_code=''
complaint_text=''
current_wd=os.getcwd()
phase_II_dir=r'dependencies\dataset\Sorted_Images_II'
image_id_and_tag_df=pd.DataFrame(columns=['Image_ID','Tag'])

#%%

inFile =os.path.normpath(sys.argv[1])# input()
#inFile=r"C:\Users\makerspace.im.EU\Documents\DO_NOT_DELETE_Shane_Tel_01637292488\GUI Tests\Automatic Complaint Classifier v3\Fastening_Aug_Sep_Heidi.xlsx"
obiee_df=pd.read_excel(inFile,header=27,)
obiee_df=obiee_df.fillna("unknown")
#merges each contact summary into one line
obiee_df["Contact Summary English1"]=[x.replace("\n"," ").replace("\t"," ") for x in obiee_df["Contact Summary English1"]]
obiee_df['Product_size']=obiee_df['Product Size']
obiee_df['Production_code']=obiee_df['Production Code']
#replace the prdicted failure mode column and all as na
'''
obiee_df['predicted_failure_mode'] = np.nan

obiee_df['front ear tearing'] = 0
obiee_df['back ear tearing'] = 0
obiee_df['tape tearing'] = 0
obiee_df['Other'] = 0
obiee_df=obiee_df.fillna('NA')
'''
# get product images and their tags
for root, directories, files in os.walk(phase_II_dir):
	directories[:] = [d for d in directories if d not in ['with bounding box']]
	for filename in files:
		
		filepath = os.path.join(root, filename)
		#create a df with image_id & tag
		image_name=os.path.split(filepath)[-1]
		tag=os.path.split(os.path.split(filepath)[0])[-1]
		image_id_and_tag_df = image_id_and_tag_df.append({'Image_ID':image_name, 'Tag':tag}, ignore_index=True)

#merge the two df to get GCR_CODE, image,tag
gcr_image_tag_df= pd.merge(map_df, image_id_and_tag_df, on=['Image_ID', 'Image_ID'])

#%% #Function to make new columns and put counts
   
#def get_columns(OBIEE_df,picture_df):
OBIEE_df =obiee_df
picture_df =gcr_image_tag_df
GCR_codes = list(OBIEE_df["Internal Case Id"].unique())
failure_elements = ["front ear tearing", "back ear tearing", "tape tearing", "Other"]
 
dict = {}

for code in GCR_codes:
	# create sub dataframe for each GCR code
	if not code in list(picture_df["Case_ID"].unique()):
		dict[code] = {"front ear tearing": 0,
					  "back ear tearing": 0,
					  "tape tearing": 0,
					  "Other": 0}
	else:	
		sub_df = picture_df.loc[picture_df["Case_ID"]==code].copy()
		sub_df.reset_index()
		sub_dict = sub_df["Tag"].value_counts().to_dict()
		for i in failure_elements:
			# put addtional elements into the sub_dict
			if not i in sub_dict.keys():
				sub_dict[i] = 0
		# put sub-dictionary as a value entry for the current GCR code
		dict[code] = sub_dict
 
# add empty columns to df
OBIEE_df["front ear tearing"] = ""
OBIEE_df["back ear tearing"] = ""
OBIEE_df["tape tearing"] = ""
OBIEE_df["Other"] = ""

# iterate through whole df
for i in range(len(OBIEE_df)):
	code = OBIEE_df.loc[i, "Internal Case Id"]
	# add the number of pictures per failure mode
	for key in dict[code].keys():
		OBIEE_df[key][i] = dict[code].get(key)

 

OBIEE_df['max_pic_n'] = OBIEE_df[["front ear tearing", "back ear tearing", "tape tearing", "Other"]].max(axis=1)
 # convert columns to numeric
OBIEE_df[["front ear tearing",
		  "back ear tearing",
		  "tape tearing",
		  "Other"]] = OBIEE_df[["front ear tearing",
								"back ear tearing",
								"tape tearing",
								"Other"]].apply(pd.to_numeric)
OBIEE_df["failing_parts"] = ""
OBIEE_df["failing_part"] = ""
failing_part = ""
for i  in range(len(OBIEE_df)):
	if (OBIEE_df["front ear tearing"][i] +
		OBIEE_df["back ear tearing"][i] +
		OBIEE_df["tape tearing"][i] + 
		OBIEE_df["Other"][i]) == 0:
		
		failing_parts = ["n/a (no product picture)"]
		failing_part = "n/a (no product picture)"
	else:
		failing_parts = []
		for j in ["front ear tearing", "back ear tearing", "tape tearing", "Other"]:
			if OBIEE_df[j][i] == OBIEE_df["max_pic_n"][i]:
				failing_parts.append(j)
				
	# converting to single failing_part
	if len(failing_parts) == 1:
		failing_part = failing_parts[0]
	
	if len(failing_parts) == 2:
		if "Other" in failing_parts:
			failing_part = failing_parts
			failing_part.remove("Other")
			failing_part = failing_part[0]
		else:
			failing_part = "multiple"
			
	if len(failing_parts) > 2:
		failing_part = "multiple"
		
	OBIEE_df["failing_parts"][i] = failing_parts
	OBIEE_df["failing_part"][i] = failing_part
	#OBIEE_df.loc[i, "failing_parts"] = failing_parts
	#OBIEE_df.loc[i, "failing_part"] = failing_part
 
di = {"front ear tearing": "# of front ear pics",
	  "back ear tearing": "# of back ear pics",
	  "tape tearing":"# of tape pics",
	  "Other": "# of other pics"}

OBIEE_df.rename(columns=di, inplace=True)

di2 = {"front ear tearing": "front ear",
	   "back ear tearing": "back ear",
	   "tape tearing":"tape",
	   "Other": "other"}

OBIEE_df = OBIEE_df.replace({"failing_part": di2})

# convert list to string
OBIEE_df["failing_parts"] = OBIEE_df["failing_parts"].apply(', '.join)
OBIEE_df["failing_parts"].value_counts()

OBIEE_df["failing_part"].value_counts()



OBIEE_df["L3_simple"] = OBIEE_df["L3 Comment Code/Comment Description"].str[0:3]

 
pd.crosstab(OBIEE_df["failing_part"], OBIEE_df["L3_simple"], dropna=False)
# remove un-necessary columns
OBIEE_df = OBIEE_df.drop(columns=['max_pic_n', 'failing_parts', "L3_simple"])
	
OBIEE_df.to_excel("OBIEE Report With Predictions.xlsx",index=False)

