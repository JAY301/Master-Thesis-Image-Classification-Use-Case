#***************************************************************************
#****************************SORTING ALGORITHM******************************
#***************************************************************************
	
def final_sorting_algorithm(sub_df,classes):
	##common local vairable decleration*********************
	classified_class=''
	size=sub_df['DetectedClass'].unique().size
	unique_classes=sub_df['DetectedClass'].unique()
	back=classes[1]
	front=classes[0]
	tape=classes[2]
	other=classes[3]
	random_forest='random_forest'
		
	#whether it contains 1 classification
	if (size==1):
		if(unique_classes[0]=='human'):
				classified_class=other	
		if(unique_classes[0]=='back ear'):
				classified_class=back 
		if(unique_classes[0]=='front ear'):
				classified_class=	front
		if(unique_classes[0]=='tape'):
				classified_class= tape
		if(unique_classes[0]=='diaper'):
				classified_class=other
			 
			 #if two classifications are there..			

	elif (size==2):
        
		if (any(p == 'human' for p in unique_classes) and any(p == 'front ear' for p in unique_classes)):
			classified_class=front
		if (any(p == 'human' for p in unique_classes) and any(p == 'back ear' for p in unique_classes)):
			classified_class=back
		if (any(p == 'human' for p in unique_classes) and any(p == 'tape' for p in unique_classes)):
			classified_class=tape
		if (any(p == 'human' for p in unique_classes) and any(p == 'diaper' for p in unique_classes)):
			classified_class=other
		if (any(p == 'back ear' for p in unique_classes) and any(p == 'diaper' for p in unique_classes)):
			classified_class=back
		if (any(p == 'back ear' for p in unique_classes) and any(p == 'tape' for p in unique_classes)):
			classified_class=random_forest
		if (any(p == 'tape' for p in unique_classes) and any(p == 'diaper' for p in unique_classes)):
			classified_class=tape
		if (any(p == 'front ear' for p in unique_classes) and any(p == 'diaper' for p in unique_classes)):
			classified_class=front
		if (any(p == 'front ear' for p in unique_classes) and any(p == 'back ear' for p in unique_classes)):
			classified_class=random_forest
		if (any(p == 'front ear' for p in unique_classes) and any(p == 'tape' for p in unique_classes)):
			classified_class=random_forest
			
	elif (size==3):
		if (any(p == 'human' for p in unique_classes) and any(p == 'diaper' for p in unique_classes)):
			if (any(p == 'front ear' for p in unique_classes)):
				classified_class=front
			if (any(p == 'back ear' for p in unique_classes)):
				classified_class=back
			if (any(p == 'tape' for p in unique_classes)):
				classified_class=tape
			else:
				classified_class=random_forest
		else:
				classified_class=random_forest
	
	
	
	else:
		classified_class=random_forest

	return classified_class 
		
		


