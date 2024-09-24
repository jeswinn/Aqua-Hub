from urllib import request
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from aquaapp.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, get_object_or_404
from .models import Seller
import re 
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404




# Create your views here.
def index_view(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('approve')
            return redirect('userhome')
        else:
            return render(request,'userlogin.html',{
                'message':"Invalid Username Or Password"
            })
            
    return render(request, 'userlogin.html')

def seller_view(request):
    return render(request, 'sellerlogin.html')

def user_reg(request):
       if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        number = request.POST.get('contact_number')
        address = request.POST.get('address')

        # Check if any required field is empty
        if not username or not password or not confirm_password or not email or not number or not address:
            return render(request, 'usereg.html', {
                "messages": "All fields are required."
            })

        # Password validation: check if passwords match
        if password != confirm_password:
            return render(request, 'usereg.html', {
                "messages": "Passwords do not match."
            })

        # Password strength validation: Minimum 8 characters, at least one uppercase letter, one lowercase letter, and one digit
        if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'\d', password):
            return render(request, 'usereg.html', {
                "messages": "Password must be at least 8 characters long, contain one uppercase letter, one lowercase letter, and one digit."
            })

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'usereg.html', {
                "messages": "Enter a valid email address."
            })

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'usereg.html', {
                "messages": "Username already exists."
            })

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return render(request, 'usereg.html', {
                "messages": "Email already exists."
            })

        # Validate phone number format: Ensure it contains only digits and is of valid length (e.g., 10 digits)
        if not re.match(r'^\d{10}$', number):
            return render(request, 'usereg.html', {
                "messages": "Enter a valid 10-digit phone number."
            })

        # Create user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.profile.phone_number = number
            user.profile.address = address
            user.save()

            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
        except Exception as e:
            # Handle exceptions (e.g., database errors)
            return render(request, 'usereg.html', {
                "messages": "An error occurred during registration. Please try again."
            })

       return render(request, 'usereg.html')

def admin_view(request):
    return render(request, 'admin.html')

# def seller_reg(request):
#  from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# from .models import Seller

def seller_reg(request):
    if request.method == 'POST':
        shop_name = request.POST.get('shop_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        location = request.POST.get('location')
        contact_num = request.POST.get('contact_num')
        product_type = request.POST.get('product_type')

       # user = User.objects.create(
        #username=username,
        #email=email,
        #password=make_password(password)
         

        Seller.objects.create(
           
            username=username,
            shop_name=shop_name,
            email=email,
            password=make_password(password),
            location=location,
            contact_num=contact_num,
            product_type=product_type,
        )
        
        return redirect('slogin')  # Replace with your success URL

    return render(request, 'sellereg.html')

 
 
def user_home(request):
    return render(request, 'userhome.html')


def about_view(request):
    return render(request, 'about.html')




def seller_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        shop_name = request.POST['shop_name']
        password = request.POST['password']

        # Try to find the seller by both username and shop_name
        try:
            seller = Seller.objects.get(username=username, shop_name=shop_name)
        except Seller.DoesNotExist:
            messages.error(request, 'Invalid username, shop name, or password')
            return redirect('slogin')

        # Check the password
        if check_password(password, seller.password):  # Assuming password is hashed
            # Set the seller session if authenticated
            request.session['seller_id'] = seller.id
            request.session['seller_username'] = seller.username
            request.session['seller_shop_name'] = seller.shop_name

            return redirect('sellerproduct')
        else:
            messages.error(request, 'Invalid username, shop name, or password')
            return redirect('slogin')
    
    return render(request, 'sellerlogin.html')

def logout_view(request):
    logout(request)
    return redirect('index')
    



def seller_dash(request):
    return render(request, 'sellerdash.html')



def admin_approv(request):
    # Fetch all sellers whose 'approved' field is False (i.e., pending approval)
    pending_sellers = Seller.objects.filter(approved=False)

    # Render the 'adminapprov.html' template with the pending sellers data
    return render(request, 'adminapprov.html', {'pending_sellers': pending_sellers})

def approve_seller(request, id):
    seller = get_object_or_404(Seller,pk=id)
    seller.approved=True    
    seller.save()
    return redirect('approve')



def approved_seller(request):
    # Fetch all sellers who are approved
    approved_sellers = Seller.objects.filter(approved=True)
    
    return render(request, 'approvedsellers.html', {'approved_sellers': approved_sellers})

def remove_seller(request, seller_id):
    # Fetch the seller by id
    seller = get_object_or_404(Seller, id=seller_id)
    
    if request.method == 'POST':
        # Remove the seller or change the approved status to False
        seller.delete()  # This will remove the seller completely
        # Alternatively, you can mark the seller as unapproved:
        # seller.approved = False
        # seller.save()

        # Redirect back to the list of approved sellers
        return redirect('sellerappr')

    return render(request, 'approvedsellers.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Generate password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            # Send the reset email
            reset_url = request.build_absolute_uri(f'/reset_password/{uid}/{token}/')
            subject = 'Reset Your Password'
            message = render_to_string('password_reset_email.html', {
                'user': user,
                'reset_url': reset_url,
            })
            send_mail(subject, message, 'aquahub837@gmail.com', [user.email], html_message=message)
            return render(request, 'login.html', {"message": "Password reset link is sent"})
        except User.DoesNotExist:
            return render(request, 'forgotpassword.html', {'error': 'No user found with that email.'})
    return render(request, 'forgotpassword.html')



def add_product(request):
    if request.method == 'POST':
        # Fetch the currently logged-in seller by their username
        seller_id = request.session.get('seller_id')

        if not seller_id:
            messages.error(request, "No Seller matches the given query.")
            return redirect('sellerdash')  # or another appropriate page

        # Get product details from the form (example: name, price, stock, etc.)
        seller = Seller.objects.get(id=seller_id)
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        description = request.POST.get('description')  # Get description from form
        image = request.FILES.get('image')

        # Create a new product and associate it with the seller
        product = Product.objects.create(
            seller=seller, 
            product_name=product_name, 
            price=price,
            stock=stock,
            description=description,
            image=image
        )
        product.save()
        messages.success(request, "Product added successfully!")
        return redirect('sellerproduct')

    return render(request, 'add_product.html')






def seller_product(request):
    # Fetch the currently logged-in seller's ID from session
    seller_id = request.session.get('seller_id')

    if not seller_id:
        messages.error(request, "You must be logged in as a seller.")
        return redirect('sellerdash')  # Redirect to seller login

    # Get the seller's details
    seller = Seller.objects.get(id=seller_id)

    # Fetch all products added by the seller
    products = Product.objects.filter(seller=seller)

    return render(request, 'sellerproduct.html', {'products': products})


