from datetime import date, datetime, timezone
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.models import User

from products.models import Product
from users.models import Goods

from .models import StaffModel
from .forms import AddCustomerGoodForm, AddNewCustomerForm, SendCustomerMessageForm

# User = settings.AUTH_USER_MODEL
# def filter_function(day, *args, **kwargs):
#     if filter_day == "recently":
#         datetime_to_get = datetime(get_year, get_month, get_date, tzinfo=timezone.utc)
#         # date_to_get = date(get_year, get_month, get_date)  
#         if filter_product:
#             goods = Goods.objects.filter(item__name = filter_product)[:30]
#             total = sum([x.price for x in goods])
#         else:      
#             goods = Goods.objects.filter()[:30]
#             total = sum([x.price for x in goods])

# THIS CLASS HANDLES THE SUPERUSER(ADMIN) DASHBOARD
class AdminView(LoginRequiredMixin, View):
    login_url = "administrator:login"
    template_name = "administrator/home.html"

    def get(self, request):
        if request.user.is_superuser:
            products = Product.objects.all()
            today = date.today()
            str_today = str(today)
            list_today = str_today.split("-")
            get_year = int(list_today[0])
            get_month = int(list_today[1])
            get_date = int(list_today[2])
            
            # datetime_to_get = datetime(get_year, get_month, get_date, tzinfo=timezone.utc)
            # date_to_get = date(get_year, get_month, get_date)            
            goods = Goods.objects.all()[:30]
                        
            # THIS FUNCTIONALITY WILL HANDLE THE DAY FILTERING FOR DAY AND PRODUCT USINF CONDITIONAL STATEMENT
            filter_day = request.GET.get("day", "recently")
            filter_product = request.GET.get("product", None)
            if filter_day == "recently":
                if filter_product:
                    goods = Goods.objects.filter(item__name = filter_product)[:30]
                    total = sum([x.price for x in goods])
                else:      
                    goods = Goods.objects.filter()[:30]
                    total = sum([x.price for x in goods])
                    
            if filter_day == "today":
                datetime_to_get = datetime(get_year, get_month, get_date, tzinfo=timezone.utc)
                # date_to_get = date(get_year, get_month, get_date)  
                if filter_product:
                    goods = Goods.objects.filter(date_ordered__gte = datetime_to_get, item__name = filter_product)
                    total = sum([x.price for x in goods])
                else:      
                    goods = Goods.objects.filter(date_ordered__gte = datetime_to_get)
                    total = sum([x.price for x in goods])
                
            elif filter_day == "yesterday":
                datetime_to_get = datetime(get_year, get_month, get_date - 1, tzinfo=timezone.utc)
                # date_to_get = date(get_year, get_month, get_date)
                if filter_product:
                    goods = Goods.objects.filter(date_ordered__gte = datetime_to_get, item__name = filter_product)
                    total = sum([x.price for x in goods])
                else:      
                    goods = Goods.objects.filter(date_ordered__gte = datetime_to_get)        
                    total = sum([x.price for x in goods])

            elif filter_day == "last week":
                datetime_to_get = datetime(get_year, get_month, get_date - 7, tzinfo=timezone.utc)
                # date_to_get = date(get_year, get_month, get_date)        
                if filter_product:
                    goods = Goods.objects.filter(date_ordered__gte = datetime_to_get, item__name = filter_product)
                    total = sum([x.price for x in goods])
                else:      
                    goods = Goods.objects.filter(date_ordered__gte = datetime_to_get)
                    total = sum([x.price for x in goods])

            context = {
                "products": products,
                "goods": goods,
                "day": filter_day,
                "total": total
            }
            return render(request, self.template_name, context)
        elif request.user.is_staff:
            return redirect("administrator:staff_home")
        else:
            return redirect("home")
admin_view = AdminView.as_view()


class AdminLogin(View):
    template_name = "administrator/login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("administrator:home")
        else:
            form = AuthenticationForm()
            context = {"form": form}
            return render(request, self.template_name, context)

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("administrator:home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
            context = {"form": form}
        return render(request, self.template_name, context)


admin_login = AdminLogin.as_view()


def admin_logout(request):
    logout(request)
    return redirect("administrator:login")

# THIS BELOW IS FOR STAFFS

# THIS CLASS HABNDLES THE STAFF HOME PAGE 
class StaffHomeView(LoginRequiredMixin, View):
    login_url = "administrator:login"
    template_name = "staff/home.html"

    def get(self, request):
        # THIS ALLOWS ONLY STAFF TO VIEW AND NOT SUPERUSERS
        if request.user.is_staff and not request.user.is_superuser:
            return render(request, self.template_name)
        else:
            return redirect("home")
        
staff_home_view = StaffHomeView.as_view()

# THIS CLASS GETS ALL CUSTOMERS ASSOCIATED WITH A UNIT WHICH CAN THEN BE VIEWED AND WORKED ON BY THE HEAD
class UnitCustomers(LoginRequiredMixin, View):
    template_name = "staff/customers.html"    
    def get(self, request):
        if request.user.is_staff and not request.user.is_superuser:
            unit_name = StaffModel.objects.get(owner=request.user).unit
            unit_customers = Goods.objects.filter(item=unit_name).order_by("owner")
            customers = set([unit_customer.owner for unit_customer in unit_customers])
            context = {"customers": customers, "unit_name": unit_name}
            return render(request, self.template_name, context)
unit_customers = UnitCustomers.as_view()

# THIS CLASS BELOW IS WHAT HANDLES THE PROFILE AND PURCASES OF A CUSTOMER IN A PARTICULAR UNIT
class CustomerView(LoginRequiredMixin, View):
    template_name = "staff/customer_detail.html"
    def get(self, request, pk):
        unit_name = StaffModel.objects.get(owner=request.user).unit
        unit_customer = User.objects.get(id=pk)
        customer_unit_goods = Goods.objects.filter(owner=unit_customer , item=unit_name)[:30]
        total = sum([x.price for x in customer_unit_goods])
        context = {
            "customer_unit_goods" : customer_unit_goods,
            "unit_name" : unit_name,
            "unit_customer" : unit_customer,
            "total": total
        }
        return render(request, self.template_name, context)
customer_view = CustomerView.as_view()

# THIS CLASS WILL BE HANDLED BY THE UNIT HEAD, IT IS USED TO ADD GOODS
class AddCustomerGood(LoginRequiredMixin, CreateView):
    login_url = "administrator:login"
    form_class = AddCustomerGoodForm
    template_name =  "staff/add_customer_good.html"
    success_url = "administrator:customer_detail"
    
    # THIS METHOD ADDS THE CUSTOMER TO THE CONTEXT DICT FOR THE TEMPLATE
    def get_context_data(self, **kwargs):
        pk = self.request.GET.get("q", None)
        unit_customer = User.objects.get(id=pk)
        kwargs["customer"] = unit_customer
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        pk = self.request.GET.get("q", None)
        unit_name = StaffModel.objects.get(owner=self.request.user).unit
        unit_customer = User.objects.get(id=pk)
        form.instance.owner = unit_customer
        form.instance.item = unit_name
        messages.success(self.request, "Added Succssfully")
        return super(AddCustomerGood, self).form_valid(form)
    
    # THIS REEDIRECTS TO THE USER DASHBOARD ON STAFF PAGE
    def get_success_url(self):
        pk = self.request.GET.get("q", None)
        return reverse_lazy('administrator:customer_detail', kwargs={'pk': pk})
    
add_customer_good = AddCustomerGood.as_view()

# THIS CLASS HANDLES THE ADDING A NEW CUSTOMER TO A UNIT IF HE HAS NOT MADE ANY PURCHASE BEFORE
class AddNewCustomer(LoginRequiredMixin, View):
    login_url = "administrator:login"
    template_name = 'staff/add_new_customer.html'
    def get(self, request):
        form = AddNewCustomerForm()
        context = {"form" : form}
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = AddNewCustomerForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            quantity = form.cleaned_data["quantity"]
            price = form.cleaned_data["price"]
            add_note = form.cleaned_data["add_note"]
            note = form.cleaned_data["note"]
            unit_name = StaffModel.objects.get(owner=self.request.user).unit
            try:
                uname = User.objects.get(username=username)
            except:
                messages.info(request, "Username does not exist")
                return render(request, self.template_name, {"form":AddNewCustomerForm(request.POST)})
            user_id = uname.id
            Goods.objects.create(
                owner = uname,
                item = unit_name,
                quantity = quantity,    
                price = price,
                add_note = add_note,
                note = note,
            )
            messages.success(request, "Added Succssfully")
            return redirect('administrator:customer_detail', pk = user_id)
        return render(request, self.template_name, {"form":AddNewCustomerForm(request.POST)})
    
add_new_customer = AddNewCustomer.as_view()

# THIS CLASS WILL HANDLE STAFF SENDING MESSAGE TO CUSTOMERS IF NECESSARY
class SendcustomerMessage(LoginRequiredMixin, CreateView):
    login_url = "administrator:login"
    form_class = SendCustomerMessageForm
    template_name = "staff/send_customer_message.html"
    
    def get_context_data(self, **kwargs):
        pk = self.request.GET.get("q", None)
        unit_customer = User.objects.get(id=pk)
        kwargs["customer"] = unit_customer
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        pk = self.request.GET.get("q", None)
        unit_customer = User.objects.get(id=pk)
        form.instance.owner = unit_customer
        messages.success(self.request, "Message Sent Succssfully")
        return super(SendcustomerMessage, self).form_valid(form)
    
    # THIS REEDIRECTS TO THE USER DASHBOARD ON STAFF PAGE
    def get_success_url(self):
        pk = self.request.GET.get("q", None)
        return reverse_lazy('administrator:customer_detail', kwargs={'pk': pk})
    
send_customer_message = SendcustomerMessage.as_view()