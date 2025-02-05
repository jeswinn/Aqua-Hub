import os
import django
import csv

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project_name.settings")
django.setup()

# Import the model
from aquaapp.models import FishWaterPreference

# File path to your CSV file
file_path = 'aquaapp/fish_dataset.csv'  # Adjust path if necessary

if os.path.exists(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            FishWaterPreference.objects.create(
                fish_name=row['Fish Name'],
                min_ph=row['Min pH'],
                max_ph=row['Max pH'],
                min_temp=row['Min Temp (°C)'],
                max_temp=row['Max Temp (°C)'],
                hardness=row['Hardness'],
                description=row['Description']
            )
    print("Fish data populated successfully.")
else:
    print(f"Error: The file {file_path} was not found.")
