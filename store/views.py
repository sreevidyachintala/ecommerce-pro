from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from store.forms import Usreg
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password,check_password

from .models import *
# Create your views here.

def store(request):
	products = Product.objects.all()
	context = {'products':products}
	return render(request, 'store/store.html', context)

def cart(request):
	context = {}
	return render(request, 'store/cart.html', context)

def checkout(request):
	context = {}
	return render(request, 'store/checkout.html', context)
def validateCustomer(customer):
	error_message=None
	if (not customer.fname):
		error_message="firstname required"
	elif len(customer.fname)<4:
		error_message="firstname name must be 4 chrs"
	elif not customer.lname:
		error_message="lname name required"
	elif len(customer.lname)<4:
		error_message="lastname name must be 4 chrs"
	elif not customer.phone:
		error_message="Phone number required"
	elif len(customer.phone)<10:
		error_message="phone number must be 10 char long"
	elif len(customer.password)<6:
		error_message="password must be 6 char long"
	elif len(customer.email)<5:
		error_message="email must be 5 char long"
	elif customer.isExist():
		error_message="email address already exist"
	return error_message

def registerUser(request):
	PostData=request.POST
	fname=PostData.get('fname')
	lname=PostData.get('lname')
	phone=PostData.get('phone')
	email=PostData.get('email')
	password=PostData.get('password')
	value={'fname':fname,'lname':lname,'phone':phone,'email':email}
	error_message=None
	customer=Customer(fname=fname,lname=lname,phone=phone,email=email,password=password)
	error_message=validateCustomer(customer)
	if not error_message:
		customer.password=make_password(customer.password)
		customer.register()
		return render(request,'store/store.html')
	else:
		data={
			'error':error_message,
			'values':value
			}
		return render(request,"store/signup.html",data)
	#return HttpResponse("success")


def signup(request):
	if request.method == "POST":
		form = Usreg(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponse("Done")
	form = Usreg()
	return render(request,"store/signup.html",{'form':form})


def login(request):
	if request.method == 'GET':
		return render(request,"store/login.html")

	else:
		email=request.POST.get('email')
		password=request.POST.get('password')
		customer=Customer.get_customer_by_email(email)
		error_message=None
		if customer:
			flag=check_password(password,customer.password)
			if flag:
				return redirect('/store')
			else:
				error_message="email or password invalid"
		else:
			error_message='email or password invalid'
		return render(request,'store/login.html',{'error':error_message})

def view1(request):
	p = Product.objects.filter()
	context = {'p':p}
	return render(request,'store/v28.html',context)

@login_required
def dashboard(request):
	return render(request,'store/dashboard.html')

def profile(request):
	return render(request,'store/profile.html')
	