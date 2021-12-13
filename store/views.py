from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import *
from django.http import JsonResponse
import json
import datetime	

from django.views.generic import View, TemplateView
from .forms import CreateUserForm, ProductForm, CustomerForm, editProductForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.mixins import LoginRequiredMixin

ORDER_LIST = []

@unauthenticated_user
def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='customer')
			user.groups.add(group)
			#Added username after video because of error returning customer name if not added
			Customer.objects.create(
				user=user,
				name=user.username,
				)

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')

	context = {'form':form}
	return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
	if request.user.is_authenticated:
		return redirect('store')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('login')
			else:
				messages.info(request, 'Username or Password is Incorrect')

		context = {}
		return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def store(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
		# ORDER_LIST.append(order)
		# for i in ORDER_LIST:
		# 	print(i)
		# ORDER_LIST.remove()
	else:
		items = []
		order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
		cartItems = order['get_cart_items']

	products = Product.objects.all()
	context = {'products':products,'cartItems':cartItems}
	return render(request, 'store/store.html', context)

@login_required(login_url='login')
def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
		orders = Order.objects.filter(customer=customer, complete=False)
		for o in orders:
			print(o)
	else:
		items = []
		order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
		cartItems = order['get_cart_items']

	context = {'items':items,'order':order,'cartItems':cartItems }
	return render(request, 'store/cart.html', context)

class CheckOutView(LoginRequiredMixin):
	pass

@login_required(login_url='login')
def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
		orders = Order.objects.filter(customer=customer, complete=False)
		for o in orders:
			print(o)
		# ORDER_LIST.append(order)
		# for i in ORDER_LIST:
		# 	print(i)
		# ORDER_LIST.remove()
	else:
		items = []
		order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
		cartItems = order['get_cart_items']

	context = {'items':items,'order':order,'cartItems':cartItems }
	return render(request, 'store/checkout.html', context)

@login_required(login_url='login')
def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order,created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
	
	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove' :
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

@login_required(login_url='login')
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order,created = Order.objects.get_or_create(customer=customer, complete=False)
		total = float(data['form']['total'])
		order.transaction_id = transaction_id

		if total == float(order.get_cart_total):
			order.complete = True
		order.save()

		if order.shipping == True:
			ShippingAddress.objects.create(
				customer=customer,
				order=order,
				address=data['shipping']['address'],
				city=data['shipping']['city'],
				state=data['shipping']['state'],
				zipcode=data['shipping']['zipcode'],

			)

	else:
		print('User is not loging in..')
	return JsonResponse('Order Complete!', safe=False)

#admin view
@login_required(login_url='login')
@admin_only
def dashboard(request):
	context = {}
	return render(request, 'admin/dashboard.html', context)

@login_required(login_url='login')
@admin_only
def adminCustomerlist(request):
	customers = Customer.objects.all()
	customer = request.user.customer

	context = {'customers':customers}
	return render(request, 'admin/adminCustomerlist.html', context)

@login_required(login_url='login')
@admin_only
def customer(request, pk_test):
	orders = Order.objects.all()
	total_orders = orders.count()

	customer = Customer.objects.get(id=pk_test)

	context = {'customer':customer,'total_orders':total_orders}
	return render(request, 'admin/adminCustomerdetails.html',context)


@login_required(login_url='login')
@admin_only
def adminProductlist(request):
	products = Product.objects.all()

	context = {'products':products}
	return render(request, 'admin/adminProductlist.html', context)

@login_required(login_url='login')
def product(request, pk_test):
	product = Product.objects.get(id=pk_test)

	context = {'product':product}
	return render(request, 'admin/adminProductdetails.html',context)

@login_required(login_url='login')
@admin_only
def addProduct(request):
	products = Product.objects.all()

	form =ProductForm()
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = ProductForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('adminProductlist')

	context = {'form':form,'products':products}
	return render(request, 'admin/adminProductadd.html', context)

	
@login_required(login_url='login')
@admin_only
def addCustomer(request):
	customer = Customer.objects.all()
	form =CreateUserForm()
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='customer')
			user.groups.add(group)
			#Added username after video because of error returning customer name if not added
			Customer.objects.create(
				user=user,
				name=user.username,
				)

			messages.success(request, 'Account was created for ' + username)
			return redirect('adminCustomerlist')

	context = {'form':form,'customer':customer}
	return render(request, 'admin/adminCustomeradd.html', context)

@login_required(login_url='login')
@admin_only
def adminOrderlist(request):
	orders = OrderItem.objects.all()

	context = {'orders':orders}
	return render(request, 'admin/adminOrderlist.html', context)

@login_required(login_url='login')
@admin_only
def editProduct(request, pk):
	product = Product.objects.get(id=pk)
	form = editProductForm(instance=product)

	if request.method == 'POST':
		form = editProductForm(request.POST, instance=product)
		if form.is_valid():
			form.save()
			return redirect('adminProductlist')

	context = {'form':form,'product':product}
	return render(request, 'admin/adminProductedit.html', context)

@login_required(login_url='login')
@admin_only
def deleteProduct(request, pk):
	product = Product.objects.get(id=pk)
	if request.method == 'POST':
		product.delete()
		return redirect('adminProductlist')

	context = {'product':product}
	return render(request, 'admin/adminProductdelete.html', context)

@login_required(login_url='login')
@admin_only
def editCustomer(request, pk):
	customers = Customer.objects.get(id=pk)
	form = CustomerForm(instance=customers)

	if request.method == 'POST':
		form = CustomerForm(request.POST, instance=customers)
		if form.is_valid():
			form.save()
			return redirect('adminCustomerlist')

	context = {'form':form,'customers':customers}
	return render(request, 'admin/adminCustomeredit.html', context)

@login_required(login_url='login')
@admin_only
def deleteCustomer(request, pk):
	customer = Customer.objects.get(id=pk)
	if request.method == 'POST':
		customer.delete()
		return redirect('adminCustomerlist')

	context = {'customer':customer}
	return render(request, 'admin/adminCustomerdelete.html', context)

#customer view
@login_required(login_url='login')
def profileDetails(request):
	orders = Order.objects.all()


	if request.user.is_authenticated:
		customer = request.user.customer

		total_orders = orders.count()
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
		cartItems = order['get_cart_items']

	context = {'customer':customer,'cartItems':cartItems,'total_orders':total_orders}
	return render(request, 'customer/profile.html', context)

@login_required(login_url='login')
def orderHistory(request):

	if request.user.is_authenticated:
		#customer = request.user.customer
		orders =Order.objects.filter(customer=request.user.customer).values('product')
		for o in orders:
			print(o)
		#product =Products.objects.filter(product=product)

	context = {'orders':orders,'customer':customer}
	return render(request, 'customer/orderHistory.html', context)

	
@login_required(login_url='login')
def editProfile(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()

			messages.success(request, 'Account was Updated.')

			return redirect('profileDetails')

	context = {'form':form,'customer':customer}
	return render(request, 'customer/editProfile.html', context)



