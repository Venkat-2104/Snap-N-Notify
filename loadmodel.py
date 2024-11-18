# import numpy as np
# import tensorflow as tf
# from tensorflow.keras.models import load_model
# from tensorflow.keras.utils import load_img, img_to_array

# # Load the model
# model = load_model('trained_model.h5')  # Replace '/path/to/your/model.h5' with the actual path to your model file

# # path = 'vk.jpg'
# def get_prediction_string(path):
#     img = load_img(path, target_size=(224, 224))

#     x = img_to_array(img)
#     x /= 255
#     x = np.expand_dims(x, axis=0)
#     images = np.vstack([x])

#     classes = model.predict(x, batch_size=10)

#     print(classes[0])

#     if classes[0] > 3e-32:
#         print(" pothole")
#         return "Pothole"
#     else:
#         print(" normal road")
#         return "Normal road"
# prompt: write a code test an image

from tensorflow import keras
import cv2
import numpy as np

# Load the saved model
model = keras.models.load_model('trained_model.h5')

# Path to the image you want to test
# image_path = 'path/to/your/test/image.jpg'

# Preprocess the image
def get_prediction_string(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (128, 128))
    img = np.array(img)
    img = img / 255.0  # Normalize the image (if you normalized during training)
    img = np.expand_dims(img, axis=0)  # Add a batch dimension

    # Make a prediction
    prediction = model.predict(img)

    # Get the predicted class (0 or 1, based on your model's output)
    predicted_class = np.argmax(prediction)

    # Interpret the prediction
    if predicted_class == 0:
        print('The image is predicted to be NORMAL')
        return "NORMAL"
    else:
        print('The image is predicted to be POTHOLES')
        return "POTHOLE"
