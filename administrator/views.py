from datetime import date, datetime, timezone, timedelta
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views import View
from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.db.models import Q

from products.models import UnitName, Product
from users.models import Goods
from users.serializer import GoodsSerializer


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


class Home(LoginRequiredMixin, View):
    template_name = "administrator/home.html"
    # THIS GET REQUEST RENDERS THE DATA FOR LAST SEVEN DAYS ON THE HOME PAGE
    def get(self, request):
        end_date = date.today()
        start_date = date(int(end_date.year), int(end_date.month), int(end_date.day) - 7)
        goods = Goods.objects.filter(date_ordered__range=[start_date, end_date + timedelta(days=1)]) # I ADDED A DAY WITH TIMEDELTA BECAUSE OF RANGE BEHAVIOR WHICH EXCLUDE THE LAST DAY
        total = sum([x.price for x in goods])
        context = {"goods": goods, "total":total, "start_date": str(start_date), "end_date": str(end_date)}
        
        return render(request, self.template_name, context)
    
    def post(self, request):
        start_date = request.POST.get("start-date")
        end_date = request.POST.get("end-date")
        if start_date and end_date: 
            check_date = None
            split_end_date = end_date.split("-")
            goods = Goods.objects.filter(date_ordered__range=[start_date, datetime(int(split_end_date[0]), int(split_end_date[1]), int(split_end_date[2])) + timedelta(days=1)]) # HERE I USED DATETIME + TIMEDELTA IN PLACE OF END DATE BECAUSE OF PYTHON RANGE BEHAVIOR THAT EXCLUDE THE LAST ELEMENT
            total = sum([x.price for x in goods])
        elif start_date or end_date:
            if start_date:
                check_date = start_date
            else:
                check_date = end_date
            list_date = check_date.split("-")
            get_year = int(list_date[0])
            get_month = int(list_date[1])
            get_date = int(list_date[2])
            goods = Goods.objects.filter(date_ordered__year=get_year, date_ordered__month=get_month, date_ordered__day=get_date)
            total = sum([x.price for x in goods])
        else:
            return redirect("administrator:home")  
        context = {"goods": goods, "total":total, "start_date": start_date, "end_date": end_date, "check_date": check_date}
        return render(request, self.template_name, context)
home = Home.as_view()

# THIS VIEW WILL BE ACCESSED USING AJAX AND WILL BE RENDERD ON HOME
class HomeChart(View):
    def get(self, request):
        start_date = request.GET["startDate"]
        end_date = request.GET["endDate"]
        check_date = request.GET["checkDate"]
        if start_date and end_date:
            split_end_date = end_date.split("-")
            goods = Goods.objects.filter(date_ordered__range=[start_date, datetime(int(split_end_date[0]), int(split_end_date[1]), int(split_end_date[2])) + timedelta(days=1)]) # HERE I USED DATETIME + TIMEDELTA IN PLACE OF END DATE BECAUSE OF PYTHON RANGE BEHAVIOR THAT EXCLUDE THE LAST ELEMENT            
            serialized = GoodsSerializer(goods, many=True)
            return JsonResponse({"data": serialized.data})
        elif check_date:
            list_date = check_date.split("-")
            get_year = int(list_date[0])
            get_month = int(list_date[1])
            get_date = int(list_date[2])
            goods = Goods.objects.filter(date_ordered__year=get_year, date_ordered__month=get_month, date_ordered__day=get_date)
            serialized = GoodsSerializer(goods, many=True)
            return JsonResponse({"data": serialized.data})
home_chart = HomeChart.as_view()

# THIS CLASS HANDLES THE SUPERUSER(ADMIN) DASHBOARD
class Sales(LoginRequiredMixin, View):
    login_url = "administrator:login"
    template_name = "administrator/sales.html"

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
            # print(Goods.objects.dates('date_ordered', 'day'))
                        
            # THIS FUNCTIONALITY WILL HANDLE THE DAY FILTERING FOR DAY AND PRODUCT USINF CONDITIONAL STATEMENT
            filter_day = request.GET.get("day", None)
            filter_product = request.GET.get("product", None)
            filter_unit = request.GET.get("unit", None)
            start_date = request.GET.get("start-date", None)
            end_date = request.GET.get("end-date", None)
            check_date = None
            
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
                    
            elif filter_day == "today":
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
            
            # THIS IS FOR THE SELECT DATE RANGE                                  
            elif start_date and end_date:
                split_end_date = end_date.split("-")
                if filter_product:
                    goods = Goods.objects.filter(item__name = filter_product, date_ordered__range=[start_date, datetime(int(split_end_date[0]), int(split_end_date[1]), int(split_end_date[2])) + timedelta(days=1)]) # HERE I USED DATETIME + TIMEDELTA IN PLACE OF END DATE BECAUSE OF PYTHON RANGE BEHAVIOR THAT EXCLUDE THE LAST ELEMENT
                    total = sum([x.price for x in goods])
                elif filter_unit:
                    goods = Goods.objects.filter( unit__name = filter_unit, date_ordered__range=[start_date,  datetime(int(split_end_date[0]), int(split_end_date[1]), int(split_end_date[2])) + timedelta(days=1)]) # HERE I USED DATETIME + TIMEDELTA IN PLACE OF END DATE BECAUSE OF PYTHON RANGE BEHAVIOR THAT EXCLUDE THE LAST ELEMENT
                    total = sum([x.price for x in goods])
                else:      
                    goods = Goods.objects.filter(date_ordered__range=[start_date,  datetime(int(split_end_date[0]), int(split_end_date[1]), int(split_end_date[2])) + timedelta(days=1)]) # HERE I USED DATETIME + TIMEDELTA IN PLACE OF END DATE BECAUSE OF PYTHON RANGE BEHAVIOR THAT EXCLUDE THE LAST ELEMENT
                    total = sum([x.price for x in goods])
                    
            # THIS IS IF THE USER SELECTS ONE OF THE FROM OR TO, IT RETURNS THE EXACT DATE SELECTED
            elif start_date or end_date:
                if start_date:
                    check_date = start_date
                else:
                    check_date = end_date
                list_date = check_date.split("-")
                get_year = int(list_date[0])
                get_month = int(list_date[1])
                get_date = int(list_date[2])
                if filter_product:
                    goods = Goods.objects.filter(date_ordered__year=get_year, date_ordered__month=get_month, date_ordered__day=get_date, item__name = filter_product)
                    total = sum([x.price for x in goods])
                elif filter_unit:
                    goods = Goods.objects.filter(date_ordered__year=get_year, date_ordered__month=get_month, date_ordered__day=get_date, unit__name = filter_unit)
                    total = sum([x.price for x in goods])
                else:      
                    goods = Goods.objects.filter(date_ordered__year=get_year, date_ordered__month=get_month, date_ordered__day=get_date)
                    total = sum([x.price for x in goods])  
            # THE FINAL ELSE STATEMENT FOR WHEN NO FILTER IS APPLIED(wHEN JUST CLICKED)
            else:
                goods = Goods.objects.filter()[:30]
                total = sum([x.price for x in goods])
                filter_day = "Recently"

            context = {
                "filter_unit": filter_unit,
                "filter_product": filter_product,
                "units": units,
                "products": products,
                "goods": goods,
                "day": filter_day,
                "start_date": start_date,
                "end_date": end_date,
                "check_date": check_date,
                "total": total
            }
            return render(request, self.template_name, context)
        elif request.user.is_staff:
            return redirect("staff:home")
        else:
            return redirect("home")
sales = Sales.as_view()


class AllCustomers(LoginRequiredMixin, View):
    login_url = "administrator:login"
    template_name = 'administrator/all_customers.html'
    def get(self, request):
        units = UnitName.objects.all()
        products = Product.objects.all()
        customers = User.objects.all().order_by("username")
        context = {"units": units, "products":products}
        
        # CUSTOMER SEARCH IS FOR THE INPUT ELEMENT FOR SEARCHING FOR USERS AND IT RETURNS RENDER HTML PAGE
        customer_search = request.GET.get("customer", None)
        if customer_search is not None:
            search_result = User.objects.filter(
                Q(username__icontains=customer_search) |
            Q(first_name__icontains=customer_search) |
            Q(last_name__icontains=customer_search)
            )
            if not search_result:
                messages.info(request, "No Result Found")
            else:
                # THIS ELSE RENDERS THE HTML PAGE WHEN IT GETS A SEARCH QUERY
                messages.info(request, f'{search_result.count()} Results found')
                context.update({"customers": search_result, "customer_search": True})
                return render(request, self.template_name, context)
        
        # THIS IS FOR FILTERING THE UNIT CUSTOMERS
        q = request.GET.get("q", None)
        if q != None:
            unit_name = UnitName.objects.get(name=q)
            unit_customers = Goods.objects.filter(unit=unit_name)
            customers = set([x.owner for x in unit_customers if x.owner not in unit_customers ])
            context.update({"unit_name": unit_name,})
            if not customers:
                messages.info(request, f"No Customer Found for {unit_name} Unit")
            else:
                messages.info(request, f"{len(customers)} Customers found for {unit_name} Unit")
                context.update({"customers": customers})
                return render(request, self.template_name, context)
            
        # THIS IS FOR FILTERING ITEM CUSTOMERS
        q = request.GET.get("item", None)
        if q != None:
            item_name = Product.objects.get(name=q)
            unit_customers = Goods.objects.filter(item=item_name)
            customers = set([x.owner for x in unit_customers if x.owner not in unit_customers ])
            context.update({"item_name": item_name,})
            if not customers:
                messages.info(request, f"No Customer Found for {item_name} Product")
            else:
                messages.info(request, f"{len(customers)} Customers found for {item_name} Product")
                context.update({"customers": customers})
                return render(request, self.template_name, context)
        context.update({
            "customers": customers,
        })
        return render(request, self.template_name, context)
    
all_customers = AllCustomers.as_view()


# class CustomerDetails(LoginRequiredMixin, DetailView):
#     template_name = 'administrator/customer_detail.html'
#     model = User
    
#     def get(self, request, *args, **kwargs):
#         return
# customer_detail = CustomerDetails.as_view()

class CustomerDetails(LoginRequiredMixin, View):
    template_name = 'administrator/customer_detail.html'
   
    def get(self, request, pk):
        context = {}
        customer = User.objects.get(id=pk)
        customer_goods = customer.owner_goods.all().order_by('-date_ordered')
        customer_units = set([x.unit for x in customer_goods])
        customer_items = set([x.item for x in customer_goods])
        total = sum([x.price for x in customer_goods])
        
        search_unit = request.GET.get("unit", None)
        if search_unit:
            context.update({"search_unit": search_unit})
            customer_goods = Goods.objects.filter(owner=customer, unit__name=search_unit).order_by('-date_ordered')
            total = sum([x.price for x in customer_goods])
        search_item = request.GET.get("item", None)
        if search_item:
            context.update({"search_item": search_item})
            customer_goods = Goods.objects.filter(owner=customer, item__name=search_item).order_by('-date_ordered')
            total = sum([x.price for x in customer_goods])
            
                    
        context.update({
            "customer": customer,
            "pk": pk,
            "customer_goods": customer_goods,
            "customer_units": customer_units,
            "customer_items": customer_items,
            "total": total
        })
        return render(request, self.template_name, context)
customer_detail = CustomerDetails.as_view()

class CustomerChart(View):
    def get(self, request):
        pk = request.GET["pk"]
        search_unit = request.GET["searchUnit"]
        search_item = request.GET["searchItem"]
        customer = User.objects.get(id=pk)
        
        if search_unit:
            goods = Goods.objects.filter(owner=customer, unit__name=search_unit).order_by('-date_ordered')
            serialized = GoodsSerializer(goods, many=True)
            return JsonResponse({"data": serialized.data})
        elif search_item:
            goods = Goods.objects.filter(owner=customer, item__name=search_item).order_by('-date_ordered')
            serialized = GoodsSerializer(goods, many=True)
            return JsonResponse({"data": serialized.data})
        else:
            goods = Goods.objects.filter(owner=customer).order_by('-date_ordered')
            serialized = GoodsSerializer(goods, many=True)
            return JsonResponse({"data": serialized.data})

customer_chart = CustomerChart.as_view()

class PurchaseDescription(LoginRequiredMixin, DetailView):
    template_name = "administrator/purchase_description.html"
    model = Goods
purchase_description = PurchaseDescription.as_view()
