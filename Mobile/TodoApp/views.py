from django.shortcuts import render,get_object_or_404
from .models import Product,Category
from cart.models import Cart
from django.core.paginator import Paginator,EmptyPage,InvalidPage
# Create your views here.
def Home(request,c_slug=None,stock=None):
    c_page=None
    product_list=None
    if c_slug!=None:
        c_page=get_object_or_404(Category,slug=c_slug)
        product_list=Product.objects.all().filter(category=c_page,available=True)

    else:
        product_list=Product.objects.all().filter(available=True)
    
    paginator=Paginator(product_list,10)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1
    try:
        products=paginator.page(page)
    except(EmptyPage,InvalidPage):
        products=paginator.page(paginator.num_pages)
   
    return render(request,'index.html',{'data':product_list,'products':products,'category':c_page})



def Details(req,id):
    data=Product.objects.get(id=id)
    return render(req,'details.html',{'data':data})

def buy(req):
    user=req.session['user']
    carts=Cart.objects.filter(user=user)
    for cart in carts:
        prod=Product.objects.get(id=cart.product.id)
        prod.stock-=cart.quantity
        prod.save()

    return redirect('phone:home')