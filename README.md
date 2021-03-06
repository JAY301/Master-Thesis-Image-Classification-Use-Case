# Automatic Complaint Classifier (Image Classification using CNNs + GUI Application)

### Product Defect Identifier: 
An end-to-end ML solution to identify product defects from consumer complaint images. The created pipeline for customer feedback system saved 1200 Man-Hours annually.
### Automated Hyperparameter Optimization: 
A scalable solution for rapid development of image classifiers for multiple business use cases, further improving ML model accuracy by 4% after manual optimization.
### Distributed ML Training: 
Data-based distributed ML model (CNN) training on asynchronous multi-GPU environment, making the training process 10x faster.


```bash
└── Master-Thesis-Image-Classification-Use-Case
    ├── GUI - To run trained ML models
    │   ├── Classifier.bat
    │   └── dependencies
    │       ├── 1_process_data_v2.py
    │       ├── 2_getImages_and_create_map_GCR_Images.py
    │       ├── 3_metadata_removal__v2.py
    │       ├── Classified_Images_stage_I.csv
    │       ├── Classified_Images_stage_IIA.csv
    │       ├── Classified_Images_stage_IIB.csv
    │       ├── MainGUIScript.py
    │       ├── P2_1_move_product_defect_to_test.py
    │       ├── P2_6_getGCR_from_image.py
    │       ├── P2_7_Comparison_scirpt with Obiee original report.py
    │       ├── PySimpleGUI.py
    │       ├── Stage_IIA_Model_Inference.py
    │       ├── Stage_IIB_Model_Inference.py
    │       ├── Stage_I_Model_Inference.py
    │       ├── Testing-Stage_II_Done.ipynb
    │       ├── Testing-Stage_I_Done.ipynb
    ├── LICENSE
    ├── README.md
    ├── Stage I Classification + Optimization
    │   ├── Stage_I_Optimization_95_trials.ipynb
    │   ├── Stage_I_Optimization_First_10_trials.ipynb
    │   ├── Stage_I_Training_EfficientNet_19000_images.ipynb
    │   ├── Stage_I_Training_RESNET_19000_images.ipynb
    │   ├── Stage_I_Training_RESNET_25000_images.ipynb
    │   ├── Stage_I_Training_VGG_19000_images.ipynb
    │   ├── Stage_I_Training_VGG_25000_images.ipynb
    │   └── stage_I_optimization.db
    └── Stage II Classification + Optimization
        ├── Research for Stage 2 CNN Implementation
        │   ├── 4 classes
        │   │   ├── EfficientNet b0 For Stage II.ipynb
        │   │   ├── EfficientNet b1 For Stage II.ipynb
        │   │   ├── EfficientNet b3 For Stage II.ipynb
        │   │   ├── EfficientNet b4 For Stage II.ipynb
        │   │   └── RESNET For Stage II.ipynb
        │   └── 7 classes
        │       ├── EfficientNet b2 For Stage II with additional classes.ipynb
        │       └── RESNET For Stage II with additional classes.ipynb
        ├── Stage_II_EfficientNet_b2_Manual.ipynb
        ├── Stage_II_Optimization.ipynb
        ├── Stage_II_Optimization_107_trials.ipynb
        ├── Stage_II_Optimization_With_Additional_Classes.ipynb
        ├── Stage_II_Optimized_Training_With_Additional_Classes.ipynb
        ├── Stage_II_Training.ipynb
        ├── stage_II_optimization.db
        └── stage_II_optimization_additional_classes.db
```

### GUI to download consumer complaint images

![image](https://user-images.githubusercontent.com/45121451/111883813-dd539a00-89bd-11eb-84c6-a44d0a956643.png)

### GUI to classify consumer complaint images using trained ML models

![image](https://user-images.githubusercontent.com/45121451/111883799-d2006e80-89bd-11eb-928a-1eb104d02f51.png)
