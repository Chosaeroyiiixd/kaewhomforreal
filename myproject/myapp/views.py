from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from myapp.forms import *
from django.contrib.auth import authenticate, login, logout
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView, View, CreateView,FormView,ListView
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect 
from myapp.models import *
from myapp import models
from django.core.mail import send_mail
from django.conf import settings

class EcomMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and request.user.customer:
                cart_obj.customer = request.user.customer
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)


class WatchDetailView(EcomMixin,DetailView):
    model = Watch
    template_name = 'watchdetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['watch_list'] = Watch.objects.all()
        context['allcategory'] = category.objects.all() 
        return context


class categoryView(EcomMixin,TemplateView):
    template_name='category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['watch_list'] = Watch.objects.all()
        context['allcategory'] = category.objects.all() 
        return context

class addtocartView(EcomMixin,TemplateView):
    template_name = 'addtocart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        watch_id = self.kwargs['Watch_id']
        watch_obj = Watch.objects.get(id=watch_id)
        cart_id = self.request.session.get('cart_id',None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_watch_in_cart = cart_obj.cartwatch_set.filter(
                watch=watch_obj)
            if this_watch_in_cart.exists():
                cartwatch = this_watch_in_cart.last()
                cartwatch.quantity += 1
                cartwatch.subtotal += watch_obj.price
                cartwatch.save()
                cart_obj.total += watch_obj.price
                cart_obj.save()
            else:
                cartwatch = Cartwatch.objects.create(
                    cart=cart_obj, watch=watch_obj, price=watch_obj.price, quantity=1, subtotal=watch_obj.price)
                cart_obj.total += watch_obj.price
                cart_obj.save()
        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartwatch = Cartwatch.objects.create(
                cart=cart_obj, watch=watch_obj, price=watch_obj.price, quantity=1, subtotal=watch_obj.price)
            cart_obj.total += watch_obj.price
            cart_obj.save()
        return context

class mycartView(EcomMixin,TemplateView):
    template_name='mycart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart =Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context

class managecartView(EcomMixin,View):
    def get(self, request, *args, **kwargs):
        w_id = self.kwargs['w_id']
        action = request.GET.get('action')
        w_obj = Cartwatch.objects.get(id=w_id)
        cart_obj = w_obj.cart

        if action == 'rmv':
            cart_obj.total -= w_obj.subtotal
            cart_obj.save()
            w_obj.delete()
        elif action == "inc":
            w_obj.quantity += 1
            w_obj.subtotal += w_obj.price
            w_obj.save()
            cart_obj.total += w_obj.price
            cart_obj.save()
        elif action == "dcr":
            w_obj.quantity -= 1
            w_obj.subtotal -= w_obj.price
            w_obj.save()
            cart_obj.total -= w_obj.price
            cart_obj.save()
            if w_obj.quantity == 0:
                w_obj.delete()

        else:
            pass
        return redirect('mycart')

class searchView(EcomMixin,TemplateView):
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search')
        result = Watch.objects.filter(model__contains=search)
        context['result'] = result
        return context


def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CreateUserForm()
    return render(request, 'register.html', {'form':form})


class checkoutView(EcomMixin,CreateView):
    template_name = 'checkout.html'
    form_class = checkoutform
    success_url = reverse_lazy('ordersuccess')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.customer:
            pass
        else:
            return redirect("/login/?next=/checkout/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get('cart_id')
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = 'Order_Received'
            del self.request.session['cart_id']
        else:
            return redirect('index')
        return super().form_valid(form)

class emptycartView(EcomMixin,View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.Cartwatch_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect('mycart')

def contact(request): 
    submitted = False
    if request.method == 'POST':
        form = contactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/contact?submitted=True')
    else:
        form = contactForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'contact.html',{'form':form, 'submitted':submitted})

class customerregistrationView(CreateView):
    template_name = 'register.html'
    form_class = customerregistrationForm
    success_url = reverse_lazy('index')



    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        user = User.objects.create_user(username,email,password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


class customerlogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('customerlogin')


class customerloginView(FormView):
    template_name = 'login.html'
    form_class = customerloginForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data["password"]
        usr = authenticate(username=username,password=password)
        if usr is not None and customer.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error":"Invalid credentials"})
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

class ordersuccessView(EcomMixin,TemplateView):
    template_name = 'ordersuccess.html'
    
class indexView(EcomMixin,TemplateView):
    template_name='index.html'

class customerprofileView(TemplateView):
    template_name = 'profile.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        context['customer'] = customer
        orders = order.objects.filter(cart__customer=customer).order_by('-id')
        context['orders'] = orders
        return context

class customerorderdetailView(DetailView):
    template_name = 'orderdetail.html'
    model = order
    context_object_name = 'ord_obj'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and customer.objects.filter(user=request.user).exists():
            Order_id = self.kwargs['pk']
            Order = order.objects.get(id=Order_id)
            if request.user.customer != Order.cart.customer:
                return redirect('profile')
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)


class AdminLoginView(FormView):
    template_name = "adminlogin.html"
    form_class = customerloginForm
    success_url= reverse_lazy('adminhome')

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
        return super().form_valid(form)

class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/adminlogin/")
        return super().dispatch(request, *args, **kwargs)

class AdminHomeView(AdminRequiredMixin,TemplateView):
    template_name = "adminhome.html"
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/adminlogin/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pendingorders"] = order.objects.filter(
            order_status="Order Received").order_by("-id")
        return context

class AdminOrderDetailView(AdminRequiredMixin, DetailView):
    template_name = "adminorderdetail.html"
    model = order
    context_object_name = "ord_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allstatus"] = ORDER_STATUS
        return context

class AdminOrderListView(AdminRequiredMixin, ListView):
    template_name = "adminorderlist.html"
    queryset = order.objects.all().order_by("-id")
    context_object_name = "allorders"

class AdminOrderStatuChangeView(AdminRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs["pk"]
        order_obj = order.objects.get(id=order_id)
        new_status = request.POST.get("status")
        order_obj.order_status = new_status
        order_obj.save()
        return redirect(reverse_lazy("adminorderdetail", kwargs={"pk": order_id}))

class AdminProductListView(AdminRequiredMixin, ListView):
    template_name = "adminproductlist.html"
    queryset = Watch.objects.all().order_by("-id")
    context_object_name = "allproducts"

class AdminProductCreateView(AdminRequiredMixin, CreateView):
    template_name = "adminproductcreate.html"
    form_class = ProductForm
    success_url = reverse_lazy("adminproductlist")

    def form_valid(self, form):
        p = form.save()
        images = self.request.FILES.getlist("more_images")
        for i in images:
            ProductImage.objects.create(product=p, image=i)
        return super().form_valid(form)


