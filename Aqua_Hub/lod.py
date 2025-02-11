from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Data Augmentation and Normalization (without resizing)
datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_data = datagen.flow_from_directory(
    "fishset/test", 
    batch_size=32, 
    class_mode='categorical', 
    subset="training"
)

val_data = datagen.flow_from_directory(
    "fishset/test", 
    batch_size=32, 
    class_mode='categorical', 
    subset="validation"
)
