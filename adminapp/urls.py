from django.urls import path
from . import views

urlpatterns = [
    path('' ,views.admin_login, name='admin_login'),
    path('ad-logout/', views.ad_logout, name='ad_logout'),
    path('ad-home/', views.admin_home, name='admin_home'),
    path('ad_categories/', views.ad_categories, name='ad_categories'),
    path('ad-products/', views.ad_products, name='ad_products'),
    path('ad-product-variations/', views.ad_products_variations, name='ad_products_variations'),
    path('ad-product-variations/<int:product_id>/', views.ad_products_variations, name='ad_products_variations'),
    path('ad-brand/', views.ad_brand, name='ad_brand'),
    path('ad-users/', views.ad_users, name='ad_users'),
    path('ad-coupons/', views.ad_coupons, name='ad_coupons'),
    path('ad-orders/', views.ad_orders, name='ad_orders'),
    path('ad-order-details/<int:order_num>/', views.order_details, name='order_details'),
    path('ad-edit-category/', views.ad_edit_category, name='ad_edit_category'),
    path('ad-edit-category/<int:category_id>/', views.ad_edit_category, name='ad_edit_category'),
    path('del-category/',views.del_category, name='del_category'),
    
    path('ad-edit-product/', views.ad_edit_product, name='ad_edit_product'),
    path('ad-edit-product/<int:product_id>/', views.ad_edit_product, name='ad_edit_product'),
    path('del-product/',views.del_product, name='del_product'),
    path('deact-product/', views.deact_product, name='deact_product'),


    path('ad-edit-product-variations/', views.ad_edit_product_variations, name='ad_add_product_variations'),
    path('ad-edit-product-variations/<int:product_var_id>/', views.ad_edit_product_variations, name='ad_edit_product_variations'),
    path('ad-del-product-variations/', views.ad_del_product_variations, name='ad_del_product_variations'),
    path('ad-deact-product-variations/', views.ad_deact_product_variations, name='ad_deact_product_variations'),

    path('ad-add-brand/', views.ad_add_brand, name='ad_add_brand'),
    path('ad-edit-brand/<int:brand_id>/', views.ad_add_brand, name='ad_edit_brand'),
    path('ad-del-brand/', views.ad_del_brand, name='ad_del_brand'),

    path('ad-add-coupon/', views.ad_add_coupon, name='ad_add_coupon'),
    path('ad-add-coupon/<int:coupon_id>/', views.ad_add_coupon, name='ad_edit_coupon'),
    path('ad-status-update/',views.status_update, name='status_update'),
    path('orderitems-active/', views.orderitems_active, name='orderitems_active'),
    path('orderitems-history/', views.orderitems_history, name='orderitems_history'),
    path('salesreport/', views.sales_report, name='sales_report'),
    path('yearly-sales/', views.yearly_sales, name='yearly_sales'),
    path('monthly-sales/', views.monthly_sales, name='monthly_sales'),

    path('ad-del-coupon/', views.del_coupon, name='del_coupon'),
    path('deact-coupon/', views.deact_coupon, name='deact_coupon'),
    path('deact-user/', views.deact_user, name='deact_user'),

]
