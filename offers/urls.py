from django.urls import path
from . import views


urlpatterns = [
    path('coupon-verify/', views.coupon_verify, name='coupon_verify'),
]