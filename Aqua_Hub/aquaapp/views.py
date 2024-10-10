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
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.views.decorators.cache import never_cache   




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
                request.session['master']=username
                return redirect('approve')
            else:
                request.session['user']=username
                return redirect('product_list')
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
            user = userreg.objects.create_user(
                username=username,
                email=email,
                password=password,
                phone_number=number,
                address=address
            )
            # user.profile.phone_number = number
            # user.profile.address = address
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

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import Seller  # Import your Seller model
from django.core.files.storage import FileSystemStorage  # To handle file uploads

def seller_reg(request):
    if request.method == 'POST':
        shop_name = request.POST.get('shop_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        location = request.POST.get('location')
        contact_num = request.POST.get('contact_num')
        product_type = request.POST.get('product_type')

        # Handle file upload for the licensing document
        if request.FILES.get('licensing_document'):
            licensing_document = request.FILES['licensing_document']
            fs = FileSystemStorage()
            filename = fs.save(licensing_document.name, licensing_document)
            licensing_document_url = fs.url(filename)  # Get the file's URL (optional)

            # Create the Seller object with the uploaded file
            Seller.objects.create(
                username=username,
                shop_name=shop_name,
                email=email,
                password=make_password(password),
                location=location,
                contact_num=contact_num,
                product_type=product_type,
                licensing_document=filename  # Save the file name to the licensing_document field
            )
        
        return redirect('slogin')  # Replace with your success URL

    return render(request, 'sellereg.html')


 
 
def user_home(request):
    return render(request, 'products.html')


def about_view(request):
    return render(request, 'about.html')




from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Seller

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

        # Check if seller is approved
        if not seller.approved:
            messages.error(request, 'Your account is not approved yet. Please wait for admin approval.')
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
    request.session.flush()
    logout(request)
    return redirect('index')
    



def seller_dash(request):
    return render(request, 'sellerdash.html')


@never_cache
def admin_approv(request):
    if 'master' in request.session:
    # Fetch all sellers whose 'approved' field is False (i.e., pending approval)
        pending_sellers = Seller.objects.filter(approved=False)

        # Render the 'adminapprov.html' template with the pending sellers data
        return render(request, 'adminapprov.html', {'pending_sellers': pending_sellers})
    else:
        return redirect('login')

def approve_seller(request, id):
    
    seller = get_object_or_404(Seller,pk=id)
    seller.approved=True    
    seller.save()
    return redirect('approve')


@never_cache
def approved_seller(request):
    if 'master' in request.session:
        # Fetch all sellers who are approved
        approved_sellers = Seller.objects.filter(approved=True)
        
        return render(request, 'approvedsellers.html', {'approved_sellers': approved_sellers})
    else:
        return redirect('login')
    
def remove_seller(request, seller_id):
    # Fetch the seller by id
    seller = get_object_or_404(Seller, id=seller_id)
    
    if request.method == 'POST':
        # Remove the seller or change the approved status to False
         # This will remove the seller completely
        # Alternatively, you can mark the seller as unapproved:
         seller.approved = False
         seller.save()

        # Redirect back to the list of approved sellers
    return redirect('sellerappr')

    return render(request, 'approvedsellers.html')






def add_product(request):
    seller_id = request.session.get('seller_id')
    sellers = get_object_or_404(Seller,pk=seller_id)
    print(sellers.product_type)
    if request.method == 'POST':
        # Fetch the currently logged-in seller by their username
        

        if not seller_id:
            messages.error(request, "No Seller matches the given query.")
            return redirect('sellerdash')  # or another appropriate page

        # Get product details from the form (example: name, price, stock, etc.)
        # seller = Seller.objects.get(id=seller_id)
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        description = request.POST.get('description')  # Get description from form
        image = request.FILES.get('image')
        water_quality = request.POST['water_quality']
        tank_size = request.POST['tank_size']
        feeding = request.POST['feeding']
        behavior = request.POST['behavior']
        health_issues = request.POST['health_issues']

        # Create a new product and associate it with the seller
        product = Product.objects.create(
            seller=sellers, 
            product_name=product_name, 
            price=price,
            stock=stock,
            description=description,
            image=image,
            water_quality=water_quality,
            tank_size=tank_size,
            feeding=feeding,
            behavior=behavior,
            health_issues=health_issues,
        )
        product.save()
        messages.success(request, "Product added successfully!")
        return redirect('sellerproduct')

    return render(request, 'add_product.html',{'sellers':sellers})






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
            return render(request, 'userlogin.html', {"message": "Password reset link is sent"})
        except User.DoesNotExist:
            return render(request, 'forgotpassword.html', {'error': 'No user found with that email.'})
    return render(request, 'forgotpassword.html')


def reset_password(request, uidb64, token):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            return render(request, 'resetpassword.html', {'error': 'Passwords do not match'})
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                # Update the user's password
                user.set_password(password)
                user.save()
                logout(request)
                return render(request, 'userlogin.html', {"message": "Reset complete, Login now"})
        except User.DoesNotExist:
            return render(request, 'resetpassword.html', {'error': 'Invalid link'})
    return render(request, 'resetpassword.html')



def edit_view(request, product_id):
    # Get the product by ID or return a 404 if not found
    product = get_object_or_404(Product, id=product_id)
    
    # Check if the form is submitted via POST request
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        description = request.POST.get('description')
        water_quality = request.POST.get('water_quality')
        tank_size = request.POST.get('tank_size')
        feeding = request.POST.get('feeding')
        behavior = request.POST.get('behavior')
        health_issues = request.POST.get('health_issues')
        
        # Validate inputs
        if not product_name or not description:
            messages.error(request, 'Product name and description cannot be empty.')
        elif float(price) < 0:
            messages.error(request, 'Price should be a positive number.')
        elif not stock.isdigit() or int(stock) < 0:
            messages.error(request, 'Stock should be a non-negative integer.')
        else:
            # Update the product details
            product.product_name = product_name
            product.price = float(price)
            product.stock = int(stock)
            product.description = description
            product.water_quality = water_quality
            product.tank_size = tank_size
            product.feeding = feeding
            product.behavior = behavior
            product.health_issues = health_issues
            
            # Handle image upload
            if 'image' in request.FILES:
                product.image = request.FILES['image']
            
            product.save()  # Save the updated product details
            
            messages.success(request, 'Product updated successfully!')
            return redirect('sellerproduct')  # Redirect to seller dashboard or product listing
    
    context = {
        'product': product
    }
    
    return render(request, 'editproduct.html', context)


def disable_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if 'seller_id' in request.session:
        product.is_active = False
        product.save()
        messages.success(request, f"{product.product_name} has been disabled.")
    else:
        messages.error(request, "You are not authorized to disable this product.")
    
    return redirect('sellerproduct') 


def enable_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if 'seller_id' in request.session:
        product.is_active = True
        product.save()
        messages.success(request, f"{product.product_name} has been enabled.")
    else:
        messages.error(request, "You are not authorized to disable this product.")
    
    return redirect('sellerproduct') 




@never_cache
def product_list_view(request):
    
        # Fetch all approved products from the database
        products = Product.objects.filter(is_active=True)

        # Set up pagination (e.g., 9 products per page)
        paginator =Paginator(products, 9)  # Show 9 products per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Pass paginated products to the template
        context = {
            'products': page_obj
        }

        return render(request, 'products.html', context)
    
        

def product_detail(request, product_id):
    # Get the product by its ID, or return a 404 error if not found
    product = get_object_or_404(Product, id=product_id)
    
    # Render the product detail template with product data
    context = {
        'product': product,
    }
    return render(request, 'product_detail.html', context)


@never_cache
@login_required(login_url='login')
def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to add items to your cart.')
        return redirect('login')

    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity',1)) # Get quantity from the form

    # Check if the user already has a cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += quantity  # Update quantity if it already exists
    cart_item.save()

    messages.success(request, f'{product.product_name} has been added to your cart.')
    return redirect('view_cart')  # Redirect to view cart page


@login_required(login_url='login')
def view_cart(request):
    if 'user' in request.session:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
        total_price = sum(item.get_total_price() for item in cart_items)
        context = {
            'cart_items': cart_items,
            'total_price': total_price,
        }
        return render(request, 'cart.html', context)

    else:
        return redirect('login')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('view_cart')


@login_required(login_url='login')
def book_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to book this product.')
        return redirect('login')
    

@never_cache
@login_required(login_url='login')
def profile_view(request):
    if 'user' in request.session:
        user = request.user.userreg
        # Fetch the related usereg record
        
        if request.method == 'POST':
            # Get user details from the form
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            
            
            # Update user fields
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.phone_number =phone_number
            
            # Update the phone number in usereg table
            

            user.save()  # Save the updated user details
        
            messages.success(request, 'Profile updated successfully!')
            return redirect('product_list')  # Redirect to profile page after saving

        context = {
            'user': user,
            
        }

        return render(request, 'profile_edit.html', context)
    else:
        return redirect('login')





def edit_seller_profile(request):
    # Check if seller is logged in by checking session
    if 'seller_id' not in request.session:
        messages.error(request, 'You need to log in to access this page.')
        return redirect('slogin')  # Redirect to login page if not authenticated

    # Get the seller ID from session
    seller_id = request.session['seller_id']

    # Fetch the seller instance based on the seller ID stored in the session
    seller = Seller.objects.get(id=seller_id)

    if request.method == 'POST':
        # Update the seller's information
        seller.email = request.POST.get('email')
        seller.contact_num = request.POST.get('contact_num')
        seller.location = request.POST.get('location')

        # Validate the input data as needed
        if not seller.email or not seller.contact_num or not seller.location:
            messages.error(request, 'All fields are required.')
        else:
            # Save the updated seller information
            seller.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('sellerproduct')  # Redirect to the profile page after saving

    # Render the profile editing template with current seller data
    context = {
        'seller': seller
    }
    return render(request, 'seller_profile.html', context)
