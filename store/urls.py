from django.urls import path
from . import views
from .views import *


urlpatterns = [
	#Leave as empty string for base url
	path('login/', views.loginPage, name="login"),
	path('register/', views.registerPage, name="register"),
	path('logout/', views.logoutUser, name="logout"),

	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),

#customer urls
	path('profileDetails/', views.profileDetails, name="profileDetails"),
	path('orderHistory/', views.orderHistory, name="orderHistory"),
	path('editProfile/', views.editProfile, name="editProfile"),


#test


#admin urls
	path('dashboard/', views.dashboard, name="dashboard"),
	path('adminCustomerlist/', views.adminCustomerlist, name="adminCustomerlist"),
	path('adminProductlist/', views.adminProductlist, name="adminProductlist"),
	path('adminOrderlist/', views.adminOrderlist, name="adminOrderlist"),
    path('editProduct/<str:pk>/', views.editProduct, name="editProduct"),

    path('customer/<str:pk_test>/', views.customer, name="customer"),
    path('product/<str:pk_test>/', views.product, name="product"),

    path('addProduct', views.addProduct, name="addProduct"),
    path('addCustomer', views.addCustomer, name="addCustomer"),
    path('editCustomer/<str:pk>', views.editCustomer, name="editCustomer"),
    path('deleteProduct/<str:pk>', views.deleteProduct, name="deleteProduct"),
    path('deleteCustomer/<str:pk>', views.deleteCustomer, name="deleteCustomer"),


]