import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import time
from keras import layers
from keras.applications.mobilenet_v2 import preprocess_input

import socket
from message_pb2 import Messaggio  # Import your protocol buffer message definition


import os
import random

def forecast(model):
    dataset_folder = '../../Dataset'
    random_directory = random.choice(os.listdir(dataset_folder))

    directory_path = os.path.join(dataset_folder, random_directory)
    image_files = os.listdir(directory_path)

    # Choose a random fire image from the folder
    random_image = random.choice(image_files)
    image_path = os.path.join(directory_path, random_image)
    print(image_path)
    img = cv2.imread(image_path)

    resize_rescale = preprocess_model()
    img = np.expand_dims(img, axis=0)
    new_img = resize_rescale(img)

    pred = model.predict(new_img)
    dato = pred.astype(float)  
    return dato

def preprocess_model():
    input = layers.Input([None, None, 3])
    x = preprocess_input(input)
    output = layers.Resizing(224, 224)(x)
    model = tf.keras.Model(inputs=input, outputs=output)
    return model


def send_message(host, port, message):
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the receiver
        sock.connect((host, port))

        # Serialize the message
        serialized_message = message.SerializeToString()

        # Send the message
        sock.sendall(serialized_message)

        # Print a success message
        print("Message sent successfully.")
    finally:
        # Close the socket
        sock.close()


# Specify the receiver's host and port
host = 'localhost'
port = 1234

while True:
    # Send the message
    model = tf.keras.saving.load_model("../firemodel.keras")
    dato = forecast(model)

    message = Messaggio()
    message.id = 2
    message.data = dato[0][0]
    
    send_message(host, port, message)
    # Create a new instance of the protocol buffer message

    # Delay for 1 second before sending the next message
    time.sleep(1)