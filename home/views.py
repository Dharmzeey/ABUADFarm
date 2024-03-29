from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView

from news.models import News
from blog.models import Blog

class Home(View):
    template_name = "home/index.html"
    def get(self, request):
        news = News.objects.all()[:3]
        blog = Blog.objects.all()[:3]
        context = {"news": news, "blog": blog}
        return render(request, self.template_name, context)
home = Home.as_view()

class Units(View):
    template_name = "pages/operations.html"
    def get(self, request):
        return render(request, self.template_name)
units = Units.as_view()

class AboutView(View):
    template_name = 'pages/about.html'
    def get(self, request):
        return render(request, self.template_name)
about = AboutView.as_view()


class ContactView(View):
    template_name = 'pages/contact.html'
    def get(self, request):
        return render(request, self.template_name)
contact = ContactView.as_view()


def agronomy(request):
    return render(request, "farm/agronomy.html")


def feedmill(request):
    return render(request, "farm/feedmill.html")


def fishries(request):
    return render(request, "farm/fishries.html")


def honey(request):
    return render(request, "farm/honey.html")


def mango(request):
    return render(request, "farm/mango.html")


def moringa(request):
    return render(request, "farm/moringa.html")


def piggery(request):
    return render(request, "farm/piggery.html")


def poultry(request):
    return render(request, "farm/poultry.html")


def plantain_chips(request):
    return render(request, "farm/plantain-chips.html")


def wood_factory(request):
    return render(request, "farm/wood-factory.html")
