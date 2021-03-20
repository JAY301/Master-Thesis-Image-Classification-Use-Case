# -*- coding: utf-8 -*-
"""
Created on 01_05_2019

@author: jayatilake.s (version 1) 

purpose: automatically remove meta data from any sorted image before
being uploaded to aws or azure or feeding to the network.

** run this inside the images or sorted_images directory
"""
import os
import os.path
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import pandas as pd

#if needed to skip an image 
#skip_number=int(sys.argv[1])
skip_number=0

#get current working folder 
#root_folder = os.getcwd()

#prompt the user to enter the name of the file in the same directory
#print("This script is used to remove meta data of images inside image folder and sorted_images folder. The path should be with the correct folder..")
#print("Please enter root folder path as root..\(locate inside images or sorted images folder) ")
#root_folder = os.path.join("dataset", "images")
root_folder =r'dependencies/dataset/images'

#build the paths of each file within the subfolders
paths_of_files = []
map_grc_pictureID=pd.DataFrame(columns=['Case_ID','Image_ID'])
#get root, directory and files 




#first generate csv of all gcr codes and image IDs
#this was moved to this script because the server gave bad gateway error if there is no script
for root, direc, files in os.walk("dependencies\\dataset\\images"):
   
	for file in files:
		if not file.startswith("PII_data"):
			if '.jpg' in file: #only search for JPEGs
			#paths_of_files.append(os.path.join(root, file)) 
			case_id=os.path.split(root)[-1]
			map_grc_pictureID=map_grc_pictureID.append({'Case_ID': case_id,'Image_ID':file} ,ignore_index=True)



		   
map_grc_pictureID.to_csv("dependencies/Map_GCR_with_ImageNames.csv",index=False)
print('Created map of GCR and image names & End of Script')

for root, direc, files in os.walk(root_folder):
   
	for file in files:
		if not file.startswith("PII_data"):
		#if '.jpg' in file:# --- sometimes all the images would not be jpg
			paths_of_files.append(os.path.join(root, file))
		


print ("Metadata to be removed in --> {:d} images".format(len(paths_of_files)))
#remove metadata for each file in the paths_of_files array	   
if skip_number > 0:
	del paths_of_files[0 : skip_number] 


for i, f in enumerate(paths_of_files):
	#open image
	image = Image.open(f)
	image_removed = image.convert('RGB') #convert RGBA(PNG) to jpeg images only with RGB
	
	
	# deletes exif data or meta data 
	data = list(image_removed.getdata())
	image_without_exif = Image.new(image_removed.mode, image_removed.size)
	image_without_exif.putdata(data)
	
	#resave the jpg in another folder under meta data removed	 
	image_without_exif.save(f,"JPEG")	 
	#move to a done folder 
	new_file_path =os.path.join(root, file)
	
	#print ("Removing metadata --> {:d}th image".format(i+skip_number))
	
	

print ("All Metadata are removed in --> {:d} images".format(len(paths_of_files)))
