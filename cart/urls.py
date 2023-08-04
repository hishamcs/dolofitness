from django.urls import path
from . import views

urlpatterns = [
    path('',views.cart,name='cart'),
    path('add_cart/<int:product_id>/',views.add_cart,name='add_cart'),
    path('remove_cart/<int:product_variation_id>/<int:cart_item_id>/',views.remove_cart,name='remove_cart'),
    path('remove_cart_item/<int:product_variation_id>/<int:cart_item_id>/',views.remove_cart_item,name='remove_cart_item'),
    path('checkout/',views.checkout,name='checkout'),
    path('checkout/<int:coupon_id>/',views.checkout,name='checkout'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('del-wishlist-item/', views.del_wishlist_item, name='del_wishlist_item'),

    path('increment-quantity/<int:cart_item_id>', views.increment_qty, name='increment_qty'),
    path('decrement-quantity/<int:cart_item_id>', views.decrement_qty, name='decrement_qty'),
    path('remove-cartitem/<int:cart_item_id>', views.removeCartItem, name='removeCartItem'),

]
