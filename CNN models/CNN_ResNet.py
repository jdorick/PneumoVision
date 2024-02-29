import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.models import Sequential
from sklearn.model_selection import train_test_split
import pandas as pd
import os
import random

# Hyperparameters 
batch_size = 32
image_size = (224, 224)
epochs = 10

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
def custom_generator(data_dir, image_label_dict, image_size, batch_size, image_indices, total_batches_per_epoch):
    images = []  
    labels = [] 
    batches_generated = 0 

    while True:
        for folder in os.listdir(data_dir):
            folder_path = os.path.join(data_dir, folder)
            if os.path.isdir(folder_path):  
                images_subdir = os.path.join(folder_path, 'images')  
                if os.path.isdir(images_subdir):  
                    for image_file in os.listdir(images_subdir):
                        image_path = os.path.join(images_subdir, image_file) 
                        image_index = os.path.basename(image_file) 

                        if image_index in image_indices:  # Check if image is in the intended set
                            label = image_label_dict.get(image_index, 'No Finding')  

                            img = tf.io.read_file(image_path)
                            img = tf.image.decode_png(img, channels=3)  
                            img = tf.image.resize(img, image_size)
                            img = tf.keras.applications.resnet.preprocess_input(img)  
                            images.append(img)  
                            labels.append(preprocess_labels(label, disease_list))  

                            if len(images) == batch_size:
                                yield tf.stack(images), tf.stack(labels)  
                                images, labels = [], [] 
                                batches_generated += 1

                                if batches_generated == total_batches_per_epoch:
                                    batches_generated = 0 
                                    break  

# Read train_val_list.txt and test_list.txt
with open(os.path.join(data_dir, 'train_val_list.txt')) as f:
    train_val_image_indices = f.read().splitlines()

with open(os.path.join(data_dir, 'test_list.txt')) as f:
    test_image_indices = f.read().splitlines()

# Data Splitting
train_val_indices, test_indices = train_test_split(train_val_image_indices, test_size=0.2, random_state=42)
train_indices, validation_indices = train_test_split(train_val_indices, test_size=0.2, random_state=42)

# Calculate batches per epoch
total_training_samples = len(train_indices)
total_validation_samples = len(validation_indices)
total_batches_per_epoch_train = total_training_samples // batch_size
total_batches_per_epoch_val = total_validation_samples // batch_size

# Model (ResNet50)
base_model = ResNet50(include_top=False, weights='imagenet', input_shape=image_size + (3,))

for layer in base_model.layers:
    layer.trainable = False

model = Sequential([
    base_model,
    Flatten(),
    Dense(1024, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(l2=0.05), bias_regularizer='l1'),
    BatchNormalization(),
    Dropout(0.4),
    Dense(15, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train with the custom generator
train_data = custom_generator(data_dir, image_label_dict, image_size, batch_size, train_indices, total_batches_per_epoch_train)
validation_data = custom_generator(data_dir, image_label_dict, image_size, batch_size, validation_indices, total_batches_per_epoch_val)

early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True 
)

print("Total Training Samples:", total_training_samples)
print("Batch Size:", batch_size)
print("Total Batches per Epoch (Train):", total_batches_per_epoch_train)

# Train the model
model.fit(
    train_data,
    epochs=epochs,
    validation_data=validation_data,
    steps_per_epoch=total_batches_per_epoch_train,
    validation_steps=total_batches_per_epoch_val,
    callbacks=[early_stopping]
)

# Save the model
model.save(r"C:\Users\jdori\Downloads\chest_xray_model_resnet.h5")