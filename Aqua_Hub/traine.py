from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.optimizers import Adam

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
dataset_dir = 'AquariumFishImages'  # Replace with your actual dataset path

# Load images from the dataset directory, apply augmentation, and split into train and validation sets
train_generator = datagen.flow_from_directory(
    dataset_dir,
    target_size=(224, 224),  # Resize all images to 224x224
    batch_size=8,  # Batch size
    class_mode='categorical'  # Since you have multiple categories
)

# Define your model architecture
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(4, activation='softmax')  # 4 categories (fish species)
])

# Compile the model
model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(
    train_generator,  # The image data generator
    epochs=10,  # Number of epochs to train
    steps_per_epoch=train_generator.samples // train_generator.batch_size,  # Number of steps per epoch
    verbose=1  # Output progress during training
)

# Save the trained model
model.save('ml_models/fish_breed_identifier.h5')
