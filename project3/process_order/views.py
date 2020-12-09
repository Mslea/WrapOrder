from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate,login, logout
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib.auth.decorators import login_required
import json

def home(request):
    product_list = Product.objects.all()[:8]

    return render(request, 'home.html',{'product_list':product_list})
# Create your views here.
@login_required
def order_detail(request,ordercode):
    order_detail_list = Order_detail.objects.filter(order__order_code = ordercode)
    context = {'order_detail_list': order_detail_list}
    return render(request,'cart.html',context)
    
@login_required
def order_list(request):
    orders = Order.objects.all()
    context = {'order_list':orders}
    return render(request,'order.html',context)
def user_login(request):
    return render(request,'login.html')

def user_logout(request):
# Since we know the user is logged in, we can now just log them out.
    logout(request)
# Take the user back to the homepage.
    return redirect('home')

def validate_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username,password= password)
        if user:
            if user.is_active:
                login(request,user)
                return JsonResponse({'status':'ok'})
            else:
                return JsonResponse({'status':'ok'})
                
        else:
            return JsonResponse({'status':'fail'})
