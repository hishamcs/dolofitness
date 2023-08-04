from django.urls import path
from . import views

urlpatterns = [
    path('',views.shop,name='shop'),
    path('get-weight/',views.get_weight,name='get_weight'),
    path('get-product-details/',views.get_product_details,name='get_product_details'),
    path('category/<slug:category_slug>/',views.shop,name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/',views.product_detail,name='product_deatill'),
    path('search/', views.search, name='search'),

    path('filter-product/', views.filter_product, name='filter_product' ),
    
]
