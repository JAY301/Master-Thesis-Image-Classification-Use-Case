# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 13:19:17 2019

@author: vaswani.m (version 1)
@Updated: jayatilake.s (version 2)
    Update Remarks:
        user interface to enter the name of the file
        appends path automatically
       
        

This script prepares the data.csv which is obtained from the OBIEE customer complaints DB
into a file type readable by Data Labelling Tool

"""
import sys
import pandas as pd
import os
import torch

debug=False
#prompt the user to enter the name of the file in the same directory
#debug option
#inFile=r"C:\Users\jayatilake.s\OneDrive - Procter and Gamble\MSc Thesis Schwalbach\GUI Builds\Automatic Complaint Classifier v2\dependencies\Sample_OBIEE_Report.xlsx"
#
if debug==False:
    inFile =os.path.normpath(sys.argv[1])# input()
if debug==True:
    inFile=r"C:\Users\jayatilake.s\OneDrive - Procter and Gamble\MSc Thesis Schwalbach\GUI Builds\Automatic Complaint Classifier v2\dependencies\Sample OBIEE Report.xlsx"
#reads the file
df=pd.read_excel(inFile,header=27,)

#puts "unkown" for empty values
df=df.fillna("unknown")

#merges each contact summary into one line
df["Contact Summary English1"]=[x.replace("\n"," ").replace("\t"," ") for x in df["Contact Summary English1"]]

#removes duplicates from the dataset
df=df.drop_duplicates(subset=['Internal Case Id'], keep='first')
df['CASE_ID']=df['Internal Case Id']
newDf=df[['CASE_ID','L2 Comment Code/Comment Category','L3 Comment Code/Comment Description','Contact Summary English1']]

newDf.rename(columns={'Contact Summary English1':'ContactSummaryEnglish1'}, inplace=True)
#saves the processed data to data.csv file
newDf.to_csv("dependencies\data.csv", sep='\t',index=False,  encoding='utf-8')    
print("UPDATE---data.csv file has been created !!!")
print("")

print("********* APROXIMATE TIMINGS *********")
print("GCR Codes found                             : {}".format(len(newDf.index)))
print("Approx. download time (minutes)       : {}  ".format(len(newDf.index)*50/60)) #assumption=each gcr code has 3 images and download time is 15s per gcr codes
print("Approx. sorting time(CPU) (minutes) : {}".format(len(newDf.index)*15/60)) #assumption= cpu takes 13s to sort one gcr code. 
print("**********************************************")

'''
Purpose:
    This will check whether a NVIDIA gpu is available or not.
    Haven't tried with AMD gpus.
 '''
# check if CUDA is available
train_on_gpu = torch.cuda.is_available()

if not train_on_gpu:
    print('*** GPU NOT available...A GPU is recommended for 100 images or more... ')
else:
    print('GPU Available... (Algorithm will run on GPU)')