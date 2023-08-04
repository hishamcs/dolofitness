from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payments/',views.payments,name='payments'),
    path('order_complete/',views.order_complete,name='order_complete'),

    path('order-details/',views.order_details,name='order_details'),
    path('order-act/', views.order_act, name='order_act'),
    path('order-return/', views.order_return, name='order_return'),
]
