import tensorflow as tf
import numpy as np
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.models import Sequential
import pandas as pd
import os
import random

# Hyperparameters 
batch_size = 32
image_size = (224, 224)
epochs = 20 

# Dataset location 
data_dir = 'E:/archive'
csv_file = os.path.join(data_dir, 'Data_Entry_2017.csv')

# All disease labels
disease_list = ['Atelectasis', 'Consolidation', 'Infiltration', 'Pneumothorax', 
                'Edema', 'Emphysema', 'Fibrosis', 'Effusion', 'Pneumonia', 
                'Pleural_Thickening', 'Cardiomegaly', 'Nodule', 'Mass', 'Hernia', 'No Finding']

# Load & Map Labels from CSV
df = pd.read_csv(csv_file)
image_label_dict = df.set_index('Image Index')['Finding Labels'].to_dict()

# Label preprocessing function
def preprocess_labels(labels_string, disease_list):
    labels = labels_string.split("|")
    one_hot_labels = np.zeros(len(disease_list))  
    for label in labels:
        idx = disease_list.index(label)
        one_hot_labels[idx] = 1
    return one_hot_labels

# Modified Preprocessing and Generator
def custom_generator(data_dir, image_label_dict, image_size, batch_size, image_indices):
    images = []  
    labels = []  

    while True:
        for folder in os.listdir(data_dir):
            folder_path = os.path.join(data_dir, folder)
            if os.path.isdir(folder_path):  
                images_subdir = os.path.join(folder_path, 'images')  
                if os.path.isdir(images_subdir):  
                    for image_file in os.listdir(images_subdir):
                        image_path = os.path.join(images_subdir, image_file) 
                        image_index = os.path.basename(image_file) 
                        label = image_label_dict.get(image_index, 'No Finding')  

                        img = tf.io.read_file(image_path)
                        img = tf.image.decode_png(img, channels=3)  
                        img = tf.image.resize(img, image_size)
                        img = tf.keras.applications.vgg16.preprocess_input(img)  
                        images.append(img)  
                        labels.append(preprocess_labels(label, disease_list))  

                        if len(images) == batch_size:
                            yield tf.stack(images), tf.stack(labels)  
                            images, labels = [], []  

# Model (VGG16)
base_model = tf.keras.applications.VGG16(include_top=False, weights='imagenet', input_shape=image_size + (3,)) 

# Freeze pre-trained layers
for layer in base_model.layers:
    layer.trainable = False 

# Head for our classification 
x = Flatten()(base_model.output)
x = Dense(1024, activation='relu')(x) 
predictions = Dense(15, activation='sigmoid')(x)  

model = tf.keras.Model(inputs=base_model.input, outputs=predictions)

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Data Splitting 
all_image_indices = list(image_label_dict.keys())  
random.shuffle(all_image_indices)  

split_index = int(0.8 * len(all_image_indices))  
train_indices = all_image_indices[:split_index]
validation_indices = all_image_indices[split_index:]

# Train with the custom generator!
train_data = custom_generator(data_dir, image_label_dict, image_size, batch_size, train_indices)
validation_data = custom_generator(data_dir, image_label_dict, image_size, batch_size, validation_indices) 

model.fit(train_data, epochs=epochs, validation_data=validation_data)

# Save the model
model.save('chest_xray_model_vgg16.h5')