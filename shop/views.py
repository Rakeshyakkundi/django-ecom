from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from math import ceil
from django.contrib import messages
import json
from django.contrib.auth.models import User,auth
# Create your views here.


def index(request):
    allProds = []
    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslide = n//4 + ceil((n/4)-(n//4))
        allProds.append([prod,range(1,nslide),nslide])
    params = {'allProds':allProds}
    return render(request,'shop/index.html',params)
def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodthem = Product.objects.filter(category=cat)
        prod = [item for item in prodthem if searchMatch(query,item)]
        n = len(prod)
        nslide = n//4 + ceil((n/4)-(n//4))
        if len(prod) != 0:
            allProds.append([prod,range(1,nslide),nslide])
    params = {'allProds':allProds,'msg':''}
    if len(allProds)==0 or len(query)<4:
        params = {'msg':'Please make sure you search a revelent search key'}
    return render(request,'shop/search.html',params)
def searchMatch(query,item):
    if query in item.desc.lower() or query in item.product_name.lower()  or query in item.category.lower():
        return True
    else:
        return False
def about(request):
    return render(request,'shop/about.html')
def contact(request):
    if request.method=='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        contact = Contact(name=name,email=email,phone=phone,message=message)
        contact.save()
        messages.success(request,f"Hello {name} You will be reached in short")
    return render(request,'shop/contact.html')
def tracker(request):
    if request.method=='POST':
        orderid = request.POST.get('orderid')
        email = request.POST.get('email')
        try:
            order = Order.objects.filter(order_id=orderid,email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderid)
                updates = []
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response = json.dumps({'status':'success','updates':updates,'itemsJson':order[0].items_json},default=str)
                  
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"NoItem"}')
        except Exception as e:
            return HttpResponse("{'status':'Error'}")
    return render(request,'shop/tracker.html')
def prodView(request,pk):
    view = Product.objects.get(id=pk)
    comments = ProductComment.objects.filter(product=view)
    i=0
    for j in comments:
        i +=1
    return render(request,'shop/prodview.html',{'view':view,'comments':comments,'counts':i,'user':request.user})
def checkout(request):
    if request.method=='POST':
        items_json=request.POST.get('itemsJson')
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        order = Order(items_json=items_json,name=name,amount=amount,email=email,phone=phone,address1=address1,address2=address2,city=city,state=state,zip_code=zip_code)
        order.save()
        thank = True
        update = OrderUpdate(order_id=order.order_id,update_desc="the order has been placed")
        update.save()
        id = order.order_id
        return render(request,'shop/checkout.html',{'thank':thank,'id':id})
    return render(request,'shop/checkout.html')
def postCommet(request):
    if request.method=="POST":
        comment = request.POST.get('comment')
        user = request.user
        product_id = request.POST.get('id')
        product = Product.objects.get(id=product_id)
        if comment != "":
            comment = ProductComment(comment=comment,user=user,product=product)
            comment.save()

        
    return redirect(f'/shop/productview/{product.pk}')
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request,'Username or Password is wrong')
            return redirect('login')  
    else:
        return redirect('/')  

def logout(request):
    auth.logout(request)
    return redirect('/')
    
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username is Taken')
                return redirect('/')
            else:
                myuser = User.objects.create_user(username,email,password1)
                myuser.first_name = fname
                myuser.last_name = lname
                myuser.save()
                messages.success(request,f' account named {username}  has been created ')
                return redirect('/')
        else:
            messages.info(request,'Password not matched')
            return redirect('/')
    else:
        return HttpResponse('404 - Not found')