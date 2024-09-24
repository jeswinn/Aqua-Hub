from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class userreg(User):
    phone_number = models.CharField(max_length=15, unique=True)
    address= models.CharField(max_length=50)




class Seller(models.Model):
    shop_name = models.CharField(max_length=100)
    username=models.CharField(unique=True,max_length=100)
    email = models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    contact_num = models.CharField(max_length=15)
    product_type = models.CharField(max_length=50, choices=[
        ('fish', 'Fish'),
        ('aquariums', 'Aquariums'),
        ('fish-food', 'Fish Food'),
    ])
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.shop_name

