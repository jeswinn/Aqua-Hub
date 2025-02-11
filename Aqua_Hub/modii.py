import tensorflow as tf
import numpy as np
import cv2
import os

# Load the trained model
model = tf.keras.models.load_model("fish_disease_mode.keras")  # Ensure correct path

# Define image size (same as used in training)
img_size = (224, 224)

# Class labels (Update these to match your dataset)
class_labels = ["Healthy", "Disease1", "Disease2", "Disease3","disease4","disease5"]  # Modify as per your classes

def preprocess_image(image_path):
    """Loads and preprocesses an image for prediction."""
    img = cv2.imread(image_path)  # Read the image
    if img is None:
        print(f"Error: Could not read {image_path}")
        return None
    img = cv2.resize(img, img_size)  # Resize to model input size
    img = img / 255.0  # Normalize pixel values
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

def predict_fish_disease(image_path):
    """Predicts the disease in a fish image."""
    processed_img = preprocess_image(image_path)
    if processed_img is None:
        return  # Stop if image loading failed
    
    predictions = model.predict(processed_img)
    predicted_class = np.argmax(predictions)  # Get class index with highest probability
    confidence = np.max(predictions)  # Get confidence score

    print(f"Predicted Class: {class_labels[predicted_class]}")
    print(f"Confidence: {confidence:.4f}")

# Define the test image path
test_image = r"C:\Users\jeswi\Desktop\dis.jpg"  # Replace with an actual image path

# Check if the file exists before prediction
if os.path.exists(test_image):
    predict_fish_disease(test_image)
else:
    print(f"Error: {test_image} not found!")
