from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('user_login/',views.user_login,name='user_login'),
    path('user_signup/',views.user_signup,name='user_signup'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('user_signup_otp/',views.user_signup_otp,name='user_signup_otp'),
    path('user_login_otp/',views.user_login_otp,name='user_login_otp'),
    path('user_login_otp_verify/<str:phone_number>/',views.user_login_otp_verify,name='user_login_otp_verify'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('my_orders/',views.my_orders,name='my_orders'),
    path('order-details/<int:order_id>/',views.user_order_details, name='user_order_details'),
    path('edit-profile/',views.edit_profile,name='edit_profile'),
    path('my-address/',views.my_address,name='my_address'),
    path('get-address/<int:address_id>/',views.get_address,name="get_address"),
    path('delete-address/<int:address_id>/',views.del_addr,name='del_addr'),
    path('set-default-address/<int:address_id>/',views.set_default_addr, name='set_default_addr'),

    path('change-password/', views.change_password, name='change_password'),
    path('invoice/<int:order_item_id>/',views.invoice, name='invoice'),

    path('generateinvoice/<int:orderitem_id>/', views.generateInvoice.as_view(), name='generateinvoice'),
    path('forgotpassword/',views.forgotpassword, name='forgotpassword'),
    path('verify-otp-password/', views.verify_otp_password, name='verify_otp_password'),

    path('forgotpassword-reset/', views.reset_passw_forget, name='reset_passw_forget'),

    path('error/', views.error_404, name='error_404'),
    

    

]
