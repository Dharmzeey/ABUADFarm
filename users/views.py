import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views import View
from django.shortcuts import get_object_or_404

from utils.export import view_pdf, download_pdf, download_excel, download_csv

from .models import LGA, Profile, Messages, Goods, Notification
from products.models import Product, UnitName
from .forms import ProfileUpdateForm, GetFeedback
from .serializer import GoodsSerializer


class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = "users/profile.html"
    model = Profile
    success_url = "profile_view"

    def get(self, request):
        profile = get_object_or_404(self.model, owner=request.user)
        form = ProfileUpdateForm(instance=profile)
        
        context = {
            "form": form,
            "profile": profile
        }
        return render(request, self.template_name, context)

    def post(self, request):
        owner = get_object_or_404(self.model, owner=request.user)
        form = ProfileUpdateForm(request.POST, request.FILES, instance=owner)
        if not form.is_valid():
            context = {"form": form}
            return render(request, self.template_name, context)
        form.save()
        messages.success(request, "Profile Updated Successfully")
        return redirect(self.success_url)
profile_update_view = ProfileUpdateView.as_view()

# THIS FUNCTION BELOW IS BEING ACCESSED BY AJAX
def load_data(request):
  state = request.GET.get('state', None)
  if state != None:
    lgas = LGA.objects.filter(state__id=state).order_by("name")
    return render(request, "users/data_list.html", {"lgas":lgas})  


class Dashboard(LoginRequiredMixin, View):
    template_name = "users/dashboard.html"

    def get(self, request):
        goods = Goods.objects.filter(owner=request.user)[:30]
        total = sum([x.price for x in goods])
        product = Product.objects.all()
        units = UnitName.objects.all()
        # THIS BELOW CHECKS THE GOODS A USER DO PURCHASE BY CHECKING THE REVERSE OF GOODS THROUGH THE PRODUCT MODEL. IT USES THE RELATED NAME ATTRIBUTE ON THE GOOD MODEL. 
        user_goods = [
            x.item_good.filter(owner=request.user)[0]
            for x in product
            if x.item_good.filter(owner=request.user)
        ]
        user_unit = [
            x.unit_good.filter(owner=request.user)[0]
            for x in units
            if x.unit_good.filter(owner=request.user)
        ]
        units = set()

        # THIS HANDLES THE FILTERING OF USER GOODS BASED ON ITEMS AND THEN ASSIGN IT TO THE GOOD DICT, AND IT GETS DISPLAYED ON THE TABLE ON HTML
        # S IS FOR USER UNIT
        s = request.GET.get("s", "")
        try:
            if s:
                goods = Goods.objects.filter(owner=request.user, unit__name=s)[:30]
                total = sum([x.price for x in goods])
        except:
            pass
        
        # Q IS FOR USER GOODS
        q = request.GET.get("q", "")
        try:
            if q:
                goods = Goods.objects.filter(owner=request.user, item__name=q)[:30]
                total = sum([x.price for x in goods])
        except:
            pass
        # THIS BELOW HANDLES DOWNLOADING THE FILES INTO ANY FORMAT SELECTED BY THE USER.
        export = request.GET.get("export", None)
        if export  == "view-pdf":
            user = request.user
            data = {'goods': goods, 'user': user, 'total': total}
            export_response = view_pdf(request, data, template_name='utils/pdf_template.html')
            return export_response
        elif export == "download-pdf":
            user = request.user
            data = {'goods': goods, 'user': user, 'total': total}
            export_response = download_pdf(request, data, template_name='utils/pdf_template.html')
            return export_response
        elif export == "excel":
            user = request.user
            data = {'goods': goods}
            export_response = download_excel(request, data)
            return export_response
        elif export == "csv":
            user = request.user
            data = {'goods': goods}
            export_response = download_csv(request, data)
            return export_response
            
        context = {"goods": goods, "total": total, "user_goods": user_goods, "q": q, "user_units": user_unit, "s":s}
        if not goods.exists():
            return render(request, self.template_name, {"empty_dashboard": True}) 
        else:
            return render(request, self.template_name, context)
dashboard = Dashboard.as_view()

# THIS IS PROCESSES WITH AJAX(GET) REQUEST. THE URL GETS HIT AND SEARILIZED DATA IS RETURNED BASED ON THE GOOD A USER CLICKS, IF NO GOOD IS CLICKED, ALL THE GOODS ARE RETURNED
class Chart(View):
    def get(self, request):
        good_name = request.GET["goodName"]
        good_unit = request.GET["goodUnit"]
        if good_unit != "":
            goods = Goods.objects.filter(owner=request.user, unit__name=good_unit).order_by('date_ordered')
            serialized = GoodsSerializer(goods, many=True)  
            return JsonResponse({"data": serialized.data})
        elif good_name != "":
            goods = Goods.objects.filter(owner=request.user, item__name=good_name).order_by('date_ordered')
            serialized = GoodsSerializer(goods, many=True)
            return JsonResponse({"data": serialized.data, "singleProduct": True})
        else:
            goods = Goods.objects.filter(owner=request.user).order_by('date_ordered')
            serialized = GoodsSerializer(goods, many=True)
            return JsonResponse({"data": serialized.data})
chart = Chart.as_view()

# THIS CLASS HANDLES THE MESSAGE STATUS OF A CUSTOMER
class UserMessage(LoginRequiredMixin, View):
    template_name = "users/messages.html"

    def get(self, request):
        user_messages = Messages.objects.filter(owner=request.user).order_by("-date")[:10]
        context = {"user_messages": user_messages}
        return render(request, self.template_name, context)
user_messages = UserMessage.as_view()


# THIS CLASS WILL BE EXECUTED BY A AJAX REQUEST
class ReadMessage(View):
    def get(self, request):
        pk = request.GET["pk"]
        message = Messages.objects.get(id=pk)
        message.read = True
        message.save()
        response_data = {"success": 1}
        return HttpResponse(json.dumps(response_data), content_type="application/json")
read_message = ReadMessage.as_view()

# THIS BELOW HANDLES THE NOTIFICATION USER GETS WHEN THE PRODUCT GETS ADDED, AND WHEN CLICKED THE NOTIFICATION INFO DISAPPEARS
class NotificationView(LoginRequiredMixin, View):
    template_name = 'users/notifications.html'
    def get(self, request):
        user_notifications = Notification.objects.filter(owner=request.user).order_by("-date")[:30]
        unread_notifications = Notification.objects.filter(owner=request.user, read=False)
        for notification in unread_notifications:
            notification.read = True
            notification.save()
        context = {
            "user_notifications": user_notifications
        }
        return render(request, self.template_name, context)
notifications = NotificationView.as_view()

# THIS BELOW HANDLES THE RENDERING AND DISPLAY OF PURCHASE DESCRIPTION
class PurchaseDescription(LoginRequiredMixin, View):
    template_name = "users/purchase_description.html"
    def get(self, request, slug):
        goods = Goods.objects.get(slug=slug)
        context = {
            "goods": goods,
        }  
        yes_or_no = request.GET.get("q", None)
        if yes_or_no == "no":
            goods.add_feedback = False
            goods.save()
        elif yes_or_no == "yes":
            form = GetFeedback()      
            context.update({"form": form})
        return render(request, self.template_name, context)    
    
    def post(self, request, slug):
        goods = Goods.objects.get(slug=slug)
        form = GetFeedback(request.POST)
        if form.is_valid():
            feedback = form.cleaned_data["feedback"]
            goods.feedback = feedback
            goods.add_feedback = False
            goods.save()
            messages.info(request, "Feedback Added Successfully")
        context = {
            "goods": goods,
        } 
        return render(request, self.template_name, context)  
            
purchase_description = PurchaseDescription.as_view() 