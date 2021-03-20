# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 00:24:31 2019
author:jayatilake.s

move all Product defect images to test folder in tensorflow env.
this script ONLY works in makerspace computer...

"""
import shutil
import os

paths_of_files=[]

product_defect_dir=r'dependencies\dataset\Sorted_Images_I\Product Defect'
tensorflow_env_test_dir=r'dependencies\dataset\Sorted_Images_II\test'

if not os.path.exists(tensorflow_env_test_dir):
        os.makedirs(tensorflow_env_test_dir)

for root, directories, files in os.walk(product_defect_dir):
    for filename in files:
        filepath = os.path.join(root, filename)
        paths_of_files.append(filepath)
        
for file in paths_of_files:
    image_name=os.path.split(file)[-1]

    old_path=file
    new_path=os.path.join(tensorflow_env_test_dir,image_name)    
          
    shutil.copy(old_path,new_path)  

print("{} images copied...".format(len(paths_of_files)))
