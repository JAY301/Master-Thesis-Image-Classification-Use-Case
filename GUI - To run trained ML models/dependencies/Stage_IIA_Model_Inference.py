#!/usr/bin/env python
# coding: utf-8

# In[1]:
from subprocess import call
call(["python", "dependencies/P2_1_move_product_defect_to_test.py"])

import matplotlib.pyplot as plt
import os 
import numpy as np
import torch
import datetime
from torch import nn
from torch import optim
import torch.nn.functional as F
from torchvision import datasets, transforms, models
from torch.utils.data.sampler import SubsetRandomSampler
from mlxtend.evaluate import confusion_matrix
import matplotlib.pyplot as plt
import pandas as pd
from mlxtend.plotting import plot_confusion_matrix
from collections import OrderedDict 
import shutil
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from pathlib import Path
import sys


#debug mode
debug=True

#loaded_model_path=os.path.normpath(sys.argv[0])

loaded_model_path = os.getcwd()
load_model=os.path.join(loaded_model_path,'dependencies\ML_model_for_stage_2_images.pth')

csv_file_name="dependencies/Classified_Images_stage_IIA.csv"
data_dir=r'dependencies/dataset'

batch_size = 100
num_workers=0


# In[2]:



class ImageFolderWithPaths(datasets.ImageFolder):
    """Custom dataset that includes image file paths. Extends
    torchvision.datasets.ImageFolder
    """

    # override the __getitem__ method. this is the method dataloader calls
    def __getitem__(self, index):
        # this is what ImageFolder normally returns 
        original_tuple = super(ImageFolderWithPaths, self).__getitem__(index)
        # the image file path
        path = self.imgs[index][0]
        # make a new tuple that includes original and the path
        tuple_with_path = (original_tuple + (path,))
        return tuple_with_path


# In[3]:


train_on_gpu = torch.cuda.is_available()
if debug==True:
    if not train_on_gpu:
        print('CUDA is not available.  Training on CPU ...')
    else:
        print('CUDA is available!  Training on GPU ...')


# In[4]:


paths_of_files = []
test_folder_path=os.path.join(os.path.join(data_dir,'Sorted_Images_II'),'test')


if not os.path.exists(test_folder_path):
    os.makedirs(test_folder_path)
    
    #make a directory in test/test with images to be sent into...
    #get root, directory and files
    for root, direc, files in os.walk(data_dir):
        for file in files:
            paths_of_files.append(os.path.join(root, file))
    
    for i, f in enumerate(paths_of_files):
        old_image_path=paths_of_files[i]
        new_image_path =os.path.join(root, paths_of_files[i].split(os.sep)[-1])
        shutil.copy(old_image_path, new_image_path) 
    
    print (" {:d} images moved  --> ../Sorted_Images_II".format(len(paths_of_files)))
else:
    print('Already Exsists..')
	

test_dir = os.path.join(data_dir, 'Sorted_Images_II')
# classes are folders in each directory with these names
classes = ['Other', 'back ear tearing', 'front ear tearing', 'tape tearing']


# In[5]:


test_transforms = transforms.Compose([transforms.Resize(255),
                                          transforms.CenterCrop(224),
                                          transforms.ToTensor(),
                                          transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])


test_data = ImageFolderWithPaths(test_dir, transform=test_transforms)


# In[6]:


test_loader = torch.utils.data.DataLoader(test_data, batch_size=batch_size, 
                                          num_workers=num_workers, shuffle=True)


# In[7]:


def load_checkpoint(filepath):
    checkpoint = torch.load(filepath)
    model = checkpoint['model']
    model.load_state_dict(checkpoint['state_dict'])
    for parameter in model.parameters():
        parameter.requires_grad = False

    model.eval()
    return model

model = load_checkpoint(load_model)
print(model.parameters)


# In[8]:


if train_on_gpu:
    model.cuda()


# In[9]:


total_preds=np.array([])
total_labels=np.array([])

# track test loss 
# over 5  classes
test_loss = 0.0
df = pd.DataFrame(columns=['Predicted Class','Path'])


batch_number=0
Start_time=(datetime.datetime.now())
model.eval() # evaluation mode

# iterate over test data
for batch_number, (data, target, path) in enumerate(test_loader):
    print("Analyzing Batch {}".format(batch_number))
    #create a sub dataframe    
    sub_df = pd.DataFrame(columns=['Predicted Class','Path'])
    # move tensors to GPU if CUDA is available
    if train_on_gpu:
        data, target = data.cuda(), target.cuda()
    # forward pass: compute predicted outputs by passing inputs to the model
    output = model(data)
    #debug step --- print('The output:{}'.format(output.shape))
    # calculate the batch loss
    #loss = criterion(output, target)
    
    # update  test loss 
    # test_loss += loss.item()*data.size(0)
    # convert output probabilities to predicted class
    _, pred = torch.max(output, 1) 
   

   #%%     
    ########################################################
    ##############Write to a CSV File ######################
    ########################################################    
    
   
    for idx in np.arange(len(pred)): 

        #write to the CSV file
        sub_df.loc[idx,'Predicted Class'] = classes[pred[idx]]
        sub_df.loc[idx,'Path']= path[idx]
    
    #append sub_df to the main df
    df=df.append(sub_df, ignore_index=True)



End_time=(datetime.datetime.now())   

print('Time taken for Testing: {}'.format(End_time-Start_time))
print('-------------------------------')


# In[14]:


for i, class_name in enumerate(classes):
   #make 5 folders 
    new_path = os.path.join(test_dir, class_name)
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    
    print("{} of images were classified as {}".format(  len(df[df['Predicted Class']==class_name]) ,class_name))

print("Total classified images: {} ".format(len(df)))


# In[15]:


for i,row in df.iterrows():
    
    old_path=df.loc[i,'Path']    
    new_path=os.path.join(test_dir,df.loc[i,'Predicted Class'],df.loc[i,'Path'].split(os.sep)[-1])
    shutil.move(old_path, new_path)
    

#saves the processed data to data.csv file
df.to_csv(csv_file_name, sep='\t',index=False,  encoding='latin-1') 
print('***All images are sorted & "Classfied_Images.csv" was generated***')

#delete folder dataset\images\Sorted_Images_I\test
if not Path(test_folder_path).is_file():
    os.rmdir(test_folder_path)


# In[ ]:




