import tensorflow as tf
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.models import Sequential
import pandas as pd
import os

# Hyperparameters 
batch_size = 32
image_size = (224, 224)
epochs = 20 

# Dataset location 
data_dir = 'E:/archive'  
csv_file = 'E:/archive/Data_Entry_2017.csv'

# Load & Map Labels from CSV
df = pd.read_csv(csv_file)
image_label_dict = df.set_index('Image Index')['Finding Labels'].to_dict()

# Modified Preprocessing and Generator
def custom_generator(data_dir, image_label_dict, image_size, batch_size):
    while True:
        for folder in os.listdir(data_dir):
            folder_path = os.path.join(data_dir, folder)
            for image_file in os.listdir(folder_path):
                image_path = os.path.join(folder_path, image_file)
                image_index = os.path.basename(image_file) 
                labels = image_label_dict.get(image_index, 'No Finding')  

                # Load, Preprocess, and Yield (Image, Labels)
                img = tf.io.read_file(image_path)
                img = tf.image.decode_png(img, channels=3)  # Assumes PNG images
                img = tf.image.resize(img, image_size)
                img = tf.keras.applications.vgg16.preprocess_input(img)  # VGG16 specific   
                yield img, labels

# Model (Let's use VGG16 as an example)
base_model = tf.keras.applications.VGG16(include_top=False, weights='imagenet', input_shape=image_size + (3,)) 

# Freeze pre-trained layers (optional)
for layer in base_model.layers:
    layer.trainable = False 

# Head for our classification 
x = Flatten()(base_model.output)
x = Dense(1024, activation='relu')(x) 
predictions = Dense(14, activation='sigmoid')(x)  # 14 disease classes

model = tf.keras.Model(inputs=base_model.input, outputs=predictions)

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train with the custom generator!
train_data = custom_generator(data_dir, image_label_dict, image_size, batch_size)
validation_data = custom_generator(data_dir, image_label_dict, image_size, batch_size) 

model.fit(train_data, epochs=epochs, validation_data=validation_data) 