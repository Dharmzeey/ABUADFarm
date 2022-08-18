import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views import View
from django.shortcuts import get_object_or_404

from .models import Profile, Messages, Goods, Notification
from products.models import Product
from .forms import ProfileUpdateForm
from .serializer import GoodsSerializer


class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = "users/profile.html"
    model = Profile
    success_url = "profile_view"

    def get(self, request):
        owner = get_object_or_404(self.model, owner=request.user)
        form = ProfileUpdateForm(instance=owner)
        context = {"form": form}
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


class Dashboard(LoginRequiredMixin, View):
    template_name = "users/dashboard.html"

    def get(self, request):
        goods = Goods.objects.filter(owner=request.user)[:30]
        product = Product.objects.all()
        # THIS BELOW CHECKS THE GOODS A USER DO PURCHASE BY CHECKING THE REVERSE OF GOODS THROUGH THE PRODUCT MODEL. IT USES THE RELATED NAME ATTRIBUTE ON THE GOOD MODEL. 
        user_goods = [
            x.unit_item_good.filter(owner=request.user)[0]
            for x in product
            if x.unit_item_good.filter(owner=request.user)
        ]
        total = sum([x.price for x in goods])

        # THIS HANDLES THE FILTERING OF USER GOODS AND THEN ASSIGN IT TO THE GOOD DICT, AND IT GETS DISPLAYED ON THE TABLE ON HTML
        q = request.GET.get("q", "")
        try:
            if q:
                goods = Goods.objects.filter(owner=request.user, item__name=q)[:30]
                total = sum([x.price for x in goods])
        except:
            pass
        context = {"goods": goods, "total": total, "user_goods": user_goods, "q": q}
        if not goods.exists():
            return render(request, self.template_name, {"empty_dashboard": True}) 
        else:
            return render(request, self.template_name, context)


dashboard = Dashboard.as_view()

# THIS CLASS HANDLES THE MESSAGE STATUS OF A CUSTOMER
class UserMessage(LoginRequiredMixin, View):
    template_name = "users/messages.html"

    def get(self, request):
        user_messages = Messages.objects.filter(owner=request.user).order_by("date")[:10]
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
        user_notifications = Notification.objects.filter(owner=request.user).order_by("read")[:30]
        unread_notifications = Notification.objects.filter(owner=request.user, read=False)
        for notification in unread_notifications:
            notification.read = True
            notification.save()
        context = {
            "user_notifications": user_notifications
        }
        return render(request, self.template_name, context)
notifications = NotificationView.as_view()


# THIS IS PROCESSES WITH AJAX(GET) REQUEST. THE URL G3ETS HIT AND SEARILIZED DATA IS RETURNED BASED ON THE GOOD A USER CLICKS, IF NO GOOD IS CLICKED, ALL THE GOODS ARE RETURNED
class Chart(View):
    def get(self, request):
        good_name = request.GET["goodName"]
        if good_name == "":
            goods = Goods.objects.filter(owner=request.user)
            serialized = GoodsSerializer(goods, many=True)
            return JsonResponse({"data": serialized.data})
        else:
            goods = Goods.objects.filter(owner=request.user, item__name=good_name)
            serialized = GoodsSerializer(goods, many=True)
            # print(serialized.data)
            return JsonResponse({"data": serialized.data, "singleProduct": True})


chart = Chart.as_view()
