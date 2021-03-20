# -*- coding: utf-8 -*-
"""
Created on 11.08.2020

@author: Jay Parmar

Functions:
1. Build .csv file from OBIEE report
2. Download images
3. Remove Metadata
4. Run stage 1 ML model
5. Move images for Stage 2 classification
6. Run stage 2A or 2B ML model

"""

import subprocess  
import PySimpleGUI as sg  
import base64
import pandas as pd

###############Sub Programs	  
sg.ChangeLookAndFeel('Kayak')
input_csv_path=""


#commandline subprocess definition
def ExecuteCommandSubprocess(command, *args):	   
	try:	  
		sp = subprocess.Popen([command, *args], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)		 
		out, err = sp.communicate()		 
		if out:		 
			print(out.decode("utf-8"))		
		if err:		 
			print(err.decode("utf-8"))		
	except:		 
		pass  


#Layout 
def main():
	
	Preprocessing = [
			   
				[sg.Text('Choose Path', size=(70, 1))],
				[sg.Text('Original xlsx file ', size=(15, 1), auto_size_text=False, justification='right'),
				sg.InputText('choose correct xlsx file...',do_not_clear=True), sg.FileBrowse()],
				[sg.Button('Build data.csv')],
				
				[],
				[sg.Text('Enter P&G Credentials To Download All Images', size=(70, 1))],
				[sg.Text('Username ', size=(15, 1), auto_size_text=False, justification='right'),
				sg.InputText('')],
				[sg.Text('Password', size=(15, 1), auto_size_text=False, justification='right'),
				sg.InputText('', password_char="*")],
				[sg.Text('Download Images & Remove Meta data					   ::', size=(32, 1)),sg.Button('Run',size=(10,1)) ],
				
				
				
				[],
				
				]  
				
	#phase II tab layout..
	Image_Classification=[
							
				[],
				
				[sg.Text('Stage I - Image Type Classification', size=(70, 1))],
				[sg.Text('5 classes (product defect / package / lot code / receipt / other)', size=(70, 1))],
				[sg.Button('Run Model I')],
				[],
				[sg.Text('Stage II - Fastening Defect Classification', size=(70, 1))],
				[sg.Text('A – 4 classes (back ear tearing / front ear tearing / tape tearing / Other)', size=(70, 1))],
				[sg.Text('B – 7 classes ( A - 4 classes / hook creep / hook missing / exposed elastic)', size=(70, 1))],
				[sg.Button('Run Model II A'), sg.Button('Run Model II B')],
				[],	    
				[sg.Text('Predict main failure mode per GCR code and add it to OBIEE report', size=(70, 1))],
				[sg.Button('Press Here',size=(20,1))]
			]
	
	layout = [[sg.TabGroup([[sg.Tab('Preprocessing', Preprocessing), 
							 sg.Tab('Image Classification', Image_Classification)]])],
				 [sg.Button('Exit')],[sg.Button('Clear Log')],[sg.Text("Program Log :: ")],
				  [sg.Text('    Check Relevant GCR ', size=(15, 1), auto_size_text=False, justification='right'),
				sg.InputText('',size=(22, 1)),sg.Button('Check',size=(10,1))], 
									
				 [sg.Output(size=(70, 10))]] 
	
	#windows	
	window = sg.Window('Automatic Complaint Classifier v4.0', layout)  
	################################ Event Loop	 ##########################
	while True:	 
		event, values = window.Read()#timeout=0)  
			   
		if event is None or event == 'Exit':  
			break  

		if event == 'Build data.csv':	
			input_csv_path=values["Browse"]
			ExecuteCommandSubprocess('python', "dependencies/1_process_data_v2.py", input_csv_path) 
			
		if event == 'Run':	  
			username=values[1]
			encoded_password = base64.b64encode(bytes(values[2], 'utf-8'))
			if username== '' and values[2]=='':
				sg.Popup('Please Enter A Valid Username & Password',title = "*** ERROR ***") #shows error button
			else:
				print("Username: ",username)
				print("Password: ",encoded_password.decode())
				ExecuteCommandSubprocess('python', 'dependencies/2_getImages_and_create_map_GCR_Images.py', username,encoded_password.decode()) 
				
	
		#if event == 'Delete ExIF': 
			#ExecuteCommandSubprocess('python', "dependencies/3_metadata_removal__v2.py") 
			
		if event == 'Run Model I': 
			ExecuteCommandSubprocess('python', "dependencies/Stage_I_Model_Inference.py")

		##For phase II
		#move product defects to stage II test folder			
			
		#if event == 'Press Here': 
			#ExecuteCommandSubprocess('python', "dependencies/P2_1_move_product_defect_to_test.py")
			
		if event == 'Run Model II A': 
			ExecuteCommandSubprocess('python', "dependencies/Stage_IIA_Model_Inference.py")	   
			
		if event == 'Run Model II B': 
			ExecuteCommandSubprocess('python', "dependencies/Stage_IIB_Model_Inference.py")

			
		if event == 'Check': 
			input_csv_path=values["Browse"]
			image_name=values[5]+'.jpg'
			ExecuteCommandSubprocess('python', "dependencies/P2_6_getGCR_from_image.py", image_name,input_csv_path)
			
		if event == 'Press Here': 
			input_csv_path=values["Browse"]
			ExecuteCommandSubprocess('python',
									 "dependencies/P2_7_Comparison_scirpt with Obiee original report.py", input_csv_path)
			   
						
		if event == 'Clear Log': 
			import os
			os.system('cls')  
	   # if event == 'TEST':
			
	ExecuteCommandSubprocess('exit')  
	window.Close()
		

if __name__ == '__main__':
	main()