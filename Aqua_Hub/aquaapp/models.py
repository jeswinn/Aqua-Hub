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
    category = models.CharField(max_length=255, null=True, blank=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)  # Link to Seller table
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    stock = models.PositiveIntegerField(default=0)  # assuming you need stock field
    is_active = models.BooleanField(default=True)  # New field to track active/inactive products
    suitable = models.CharField(max_length=255,null=True)
    weight = models.CharField(max_length=255,null=True)

   
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



class VirtualTank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    height = models.IntegerField()
    width = models.IntegerField()
    depth = models.IntegerField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tank ({self.height}x{self.width}x{self.depth})"


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user who created the post
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    allow_comments = models.BooleanField(default=True)  # To enable/disable comments
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)  # Image field

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.blog.title}"
    

class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who registered the complaint
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)  # Seller the complaint is against
    subject = models.CharField(max_length=255)
    description = models.TextField()
    payment_id = models.CharField(max_length=255, blank=True, null=True)  # Added payment ID field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint by {self.user.username} against {self.seller.shop_name}"
    
class DeliveryPerson(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Will be hashed
    contact_number = models.CharField(max_length=10)
    vehicle_details = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)  # Active/Inactive
    address = models.TextField()  # Address field added
    pin_code = models.CharField(max_length=6)  # Mandatory Pin Code
    is_active = models.BooleanField(default=False)
    delivery_status = models.ForeignKey(
        'Order', on_delete=models.SET_NULL, null=True, blank=True, related_name="delivery_person_status"
    )
    

    def __str__(self):
        return self.username



class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')  # Link to the user
    full_name = models.CharField(max_length=255)
    contact1 = models.CharField(max_length=10)  # Primary contact number
    contact2 = models.CharField(max_length=10, blank=True, null=True)  # Alternative contact number
    locality = models.CharField(max_length=255)
    address = models.TextField()  # Full address
    landmark = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    saved = models.BooleanField(default=False)  # To mark whether the address is saved

    def __str__(self):
        return f"{self.full_name} - {self.city}, {self.state}"
    


class Order(models.Model):
    STATUS_CHOICES = (
        ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
     
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User placing the order
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Product being ordered
    quantity = models.PositiveIntegerField()  # Quantity of the product
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Total price of the order
    address = models.ForeignKey(UserAddress, on_delete=models.SET_NULL, null=True)  # Shipping address
    payment_id = models.CharField(max_length=100, blank=True, null=True)  # Razorpay Payment ID
    payment_status = models.CharField(max_length=50, default='Pending')  # Payment status (Pending, Completed, Failed)
    order_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Confirmed')
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of the order creation
    delivery_person = models.ForeignKey(DeliveryPerson, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_status = models.CharField(
        max_length=50,
        choices=[('Pending', 'Pending'), ('Out for Delivery', 'Out for Delivery'), ('Delivered', 'Delivered')],
        default='Pending')

    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {self.payment_status}"


class RatingAndReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # 1 to 5 stars
    review_text = models.TextField(blank=True, null=True)
    images = models.ImageField(upload_to='review_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)  # Ensure it's linked to a purchase

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlist_items')
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

    class Meta:
        unique_together = ('user', 'product')  # Prevent duplicate wishlist entries for the same user and product


class FishWaterPreferences(models.Model):
    fish_name = models.CharField(max_length=100, unique=True)
    min_ph = models.FloatField()
    max_ph = models.FloatField()
    min_temp = models.FloatField()
    max_temp = models.FloatField()
    hardness = models.CharField(
    max_length=50,
    choices=[
        ('soft', 'Soft'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
        ('soft_to_medium', 'Soft to Medium'),
        ('medium_to_hard', 'Medium to Hard'),
    ]
)
    description = models.TextField()

    def __str__(self):
        return self.fish_name
    

    from django.db import models

class FishCare(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Fish species name
    scientific_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()  # General information
    tank_requirements = models.TextField()  # Water quality, pH levels, temperature, etc.
    diet = models.TextField()  # Feeding habits
    compatibility = models.TextField()  # Can it live with other species?
    common_diseases = models.TextField()  # Health concerns
    image = models.ImageField(upload_to='fish_care_images/', blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class FishCareGuide(models.Model):
    fish_name = models.CharField(max_length=100)
    description = models.TextField()
    feeding_habits = models.TextField()
    water_quality = models.TextField()
    fish_image = models.ImageField(upload_to='fish_images/')
    additional_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fish_name



class FishDiseaseResult(models.Model):
    image = models.ImageField(upload_to="disease_images/")
    detected_disease = models.CharField(max_length=255)
    confidence = models.FloatField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.detected_disease} ({self.confidence}%)"