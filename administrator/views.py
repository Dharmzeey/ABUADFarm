from datetime import date, datetime, timezone
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.models import User

from products.models import UnitName, Product
from users.models import Goods


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


# THIS CLASS HANDLES THE SUPERUSER(ADMIN) DASHBOARD
class AdminView(LoginRequiredMixin, View):
    login_url = "administrator:login"
    template_name = "administrator/home.html"

    def get(self, request):
        if request.user.is_superuser:
            units = UnitName.objects.all()
            products = Product.objects.all().order_by("name")
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
            filter_unit = request.GET.get("unit", None)
            start_date = request.GET.get("start-date", None)
            end_date = request.GET.get("end-date", None)
            
            if filter_day == "recently":
                if filter_product:
                    goods = Goods.objects.filter(item__name = filter_product)[:30]
                    total = sum([x.price for x in goods])
                elif filter_unit:
                    goods = goods = Goods.objects.filter(unit__name = filter_unit)[:30]
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
                elif filter_unit:
                    goods = Goods.objects.filter(date_ordered__gte = datetime_to_get, unit__name = filter_unit)
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
                elif filter_unit:
                    goods = Goods.objects.filter(date_ordered__gte = datetime_to_get, unit__name = filter_unit)
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
                elif filter_unit:
                    goods = Goods.objects.filter(date_ordered__gte = datetime_to_get, unit__name = filter_unit)
                    total = sum([x.price for x in goods])
                else:      
                    goods = Goods.objects.filter(date_ordered__gte = datetime_to_get)
                    total = sum([x.price for x in goods])
            
            elif start_date and end_date != None:
                datetime_to_get = datetime(get_year, get_month, get_date - 7, tzinfo=timezone.utc)

            context = {
                "filter_unit": filter_unit,
                "filter_product": filter_product,
                "units": units,
                "products": products,
                "goods": goods,
                "day": filter_day,
                "total": total
            }
            return render(request, self.template_name, context)
        elif request.user.is_staff:
            return redirect("staff:home")
        else:
            return redirect("home")
admin_view = AdminView.as_view()

class AllCustomers(LoginRequiredMixin, View):
    login_url = "administrator:login"
    template_name = 'administrator/all_customers.html'
    def get(self, request):
        customers = User.objects.all().order_by("username")
        context = {
            "customers": customers
        }
        return render(request, self.template_name, context)
    
all_customers = AllCustomers.as_view()
