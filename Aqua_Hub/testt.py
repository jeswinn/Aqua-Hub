import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

# Load the trained model
model = tf.keras.models.load_model('ml_models/fish_breed_identifier.h5')

# Path to the image you want to predict
img_path = r"C:\Users\jeswi\Desktop\tet.jpg"  # Change this to the path of your image

# Load and preprocess the image
img = image.load_img(img_path, target_size=(224, 224))  # Resize image to match model input size
img_array = image.img_to_array(img)  # Convert image to array
img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
img_array /= 255.0  # Normalize image to 0-1 range

# Predict the class probabilities
prediction = model.predict(img_array)

# Get the index of the class with the highest probability
predicted_class_index = np.argmax(prediction)

# Print the predicted class index
print(f"Predicted class index: {predicted_class_index}")

# Optional: if you want to map the index to class names, use this:
class_names = ['Guppy', 'Molly', 'Neon Tetra', 'zebra']  # Replace with your actual class names
predicted_class_name = class_names[predicted_class_index]
print(f"Predicted class: {predicted_class_name}")
