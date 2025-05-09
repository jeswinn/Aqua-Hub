"""
URL configuration for Aqua_Hub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . views import *
from aquaapp.views import delivery_login  # Import the view function


urlpatterns = [
    path('',index_view, name='index'),
     path('login',login_view, name='login'),
      path('slogin',seller_login, name='slogin'),
      path('userreg',user_reg, name='userreg'),
      path('admin' ,admin_view, name='admin'),
      path('sellereg',seller_reg, name='sellereg'),
      path('userhome',user_home, name='userhome'),
      path('sellerdash',seller_dash, name='sellerdash'),
      path('logout',logout_view, name='logout'),
      path('approve',admin_approv,name='approve'),
      path('adminappr/<int:id>/', approve_seller, name='approve_seller'),
      path('sellerappr',approved_seller,name='sellerappr'),
      path('forgotpassword',forgot_password,name='forgotpassword'),
      path('reset_password/<uidb64>/<token>/', reset_password, name='reset_password'),
      path('removeseller/<int:seller_id>',remove_seller,name='removeseller'),
      path('add_product/',add_product, name='add_product'),
      path('about',about_view, name='about'),
      path('sellerproduct/',seller_product, name='sellerproduct'),
      path('oauth/', include('social_django.urls', namespace='social')),
      path('edit_product/<int:product_id>',edit_view,name='edit_product'),
      path('prouct_list/',product_list_view,name='product_list'),
      path('product/<int:product_id>/',product_detail, name='product_detail'),
      path('add_to_cart/<int:product_id>/',add_to_cart, name='add_to_cart'),
      path('book_now/<int:product_id>/',book_now, name='book_now'),
      path('cart/', view_cart, name='view_cart'),
      path('remove_from_cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
      path('disable_product/<int:product_id>/',disable_product, name='disable_product'),
      path('enable_product/<int:product_id>/',enable_product, name='enable_product'),
      path('profile/', profile_view, name='Profile'),
      path('sprofile/',edit_seller_profile, name='sprofile'),
      path('virtual-tank/', view_virtual_tank, name='virtual_tank_view'),
      path('create-tank/', create_virtual_tank, name='create_virtual_tank'),
      path('blogs/', blog_list, name='blog_list'),
      path('blogs/<int:pk>/', blog_detail, name='blog_detail'),
      path('blogs/create/', create_blog, name='create_blog'),
      path('blog/<int:blog_id>/comment/', add_comment, name='add_comment'),
      path('myblogs/', my_blogs, name='my_blogs'),
      path('blogs/<int:blog_id>/edit/', edit_blog, name='edit_blog'),
      path('reject_seller/<int:seller_id>/', reject_seller, name='reject_seller'),
      path('manage-users/', manage_users, name='manage_users'),
      path('complaints/register/', register_complaint, name='register_complaint'),
      path('view-complaints/', view_complaints, name='view_complaints'),
      path('product/<int:product_id>/book-now/<int:quantity>', book_now, name='book_now'),
      path('product/<int:product_id>/enter-address/', add_new_address, name='add_new_address'),
      path('product/<int:product_id>/book-now/', create_order, name='order_now'),
      path('payment-handler/', payment_handler, name='payment_handler'),
      path('completed-orders/', completed_orders, name='completed_orders'),
      path('seller/orders/', seller_orders, name='seller_orders'),
      path('admin_orders/', admin_all_orders, name='admin_all_orders'),
      path('product/<int:product_id>/select-address/', select_address, name='select_address'),
      path('reply-complaint/<int:complaint_id>/', reply_complaint, name='reply_complaint'),
      path('fish-food/',food_list, name='food_list'),
      path('plant/',plants_list, name='plants_list'),
      path('review/<int:product_id>',submit_review, name='submit_review'),
      path('product/<int:product_id>/reviews/', product_reviews, name='product_reviews'),
      path('disease/',disease_detector,name='disease_detector'),
      path('wishlist/',wishlist_view,name='wishlist'),
      path('add_to_wishlist/<int:product_id>/',add_to_wishlist,name='add_to_wishlist'),
      path('remove_from_wishlist/<int:product_id>/',remove_from_wishlist,name='remove_from_wishlist'),
    #   path("analyze_water/", analyze_water, name="analyze_water"),
      path('water-quality-analyzer/', water_quality_analyzer, name='water_quality_analyzer'),
      path("fish-compatibility/", check_compatibility, name="fish_compatibility"),
        path("plant-compatibility/", get_fish_details, name="get_fish"),
        path('find_fish/', fish_search_page, name='find_fish'),
         path('create/', create_care_guide, name='create_care_guide'),
       path('list/', care_guide_list, name='care_guide_list'),
    path('generate-pdf/<int:guide_id>/', generate_pdf, name='generate_pdf'),
     path('register/', register_delivery_person, name='register_delivery_person'),
    # path('logout/', delivery_person_logout, name='delivery_person_logout'),
    # path('assign/<int:order_id>/', assign_delivery_person, name='assign_delivery_person'),
    # path('update-status/<int:order_id>/', update_delivery_status, name='update_delivery_status'),
    # path('track/<int:order_id>/', track_order, name='track_order'),
    path('manage-delivery/', manage_delivery_persons, name='manage_delivery'),
    path('approve-delivery/<int:delivery_id>/', approve_delivery_person, name='approve_delivery'),
    path('reject-delivery/<int:delivery_id>/', reject_delivery_person, name='reject_delivery'),
     path('dashboard/', delivery_dashboard, name='delivery_dashboard'),
     path("delivery-login/", delivery_login, name="delivery_login"),
     path("update-order-status/", update_order_status, name="update_order_status"),
     path("comission/",commission_dashboard, name="commission_dashboard"),
     path("detect_disease/", disease_detection, name="detect_disease"),
     path("predict_disease/", predict_disease, name="predict_disease"),
     
   
   
]
     



      
      
     
    
    


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)