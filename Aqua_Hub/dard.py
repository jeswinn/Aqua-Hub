from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Define ImageDataGenerator with augmentation
datagen = ImageDataGenerator(
    rescale=1./255,  # Normalize images to 0-1
    rotation_range=40,  # Random rotation
    width_shift_range=0.2,  # Horizontal shift
    height_shift_range=0.2,  # Vertical shift
    shear_range=0.2,  # Shear angle
    zoom_range=0.2,  # Zooming
    horizontal_flip=True,  # Horizontal flip
    fill_mode='nearest'  # Filling missing pixels after transformations
)

# Set the directory where your images are stored
dataset_dir = 'AquariumFishImages'

# Load images from the dataset directory, apply augmentation, and split into train and validation sets
train_generator = datagen.flow_from_directory(
    dataset_dir,
    target_size=(224, 224),  # Resize all images to 224x224
    batch_size=8,  # Batch size
    class_mode='categorical'  # Since you have multiple categories
)
