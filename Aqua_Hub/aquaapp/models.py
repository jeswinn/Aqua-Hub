from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class userreg(User):
    phone_number = models.CharField(max_length=15, unique=True)
    address= models.CharField(max_length=50)




class Seller(models.Model):
    shop_name = models.CharField(max_length=100)
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    contact_num = models.CharField(max_length=15)
    licensing_document = models.FileField(upload_to='licensing_docs/', blank=True, null=True)  # New field for PDF upload
    product_type = models.CharField(max_length=50, choices=[
        ('fish', 'Fish'),
        ('aquariums', 'Aquariums'),
        ('fish-food', 'Fish Food'),
    ])
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.shop_name


class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)  # Link to Seller table
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    stock = models.PositiveIntegerField(default=0)  # assuming you need stock field
    is_active = models.BooleanField(default=True)  # New field to track active/inactive products
 # New field for fish care details

    water_quality = models.CharField(max_length=255,null=True)
    tank_size = models.CharField(max_length=255,null=True)
    feeding = models.CharField(max_length=255,null=True)
    behavior = models.CharField(max_length=255,null=True)
    health_issues = models.CharField(max_length=255,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product_name



class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='blogs/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.product_name} (x{self.quantity})"
    
    def get_total_price(self):
        return self.quantity * self.product.price
