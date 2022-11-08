from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView

from .models import News, Blog

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


class BlogView(ListView):
    template_name = "pages/blog.html"
    model = Blog
    context_object_name = "blog"
    paginate_by = 20
blog = BlogView.as_view()

class BlogDetailsView(DetailView):
    model = Blog
    template_name = 'pages/blog-details.html'
    def get_context_data(self, **kwargs):
        random_blogs = Blog.objects.all().order_by('?')[:3]
        data = super().get_context_data(**kwargs)
        data['random_blogs'] = random_blogs
        return data
blog_details = BlogDetailsView.as_view()


class NewsView(ListView):
    template_name = "pages/news.html"
    model = News
    context_object_name = "news"
    paginate_by = 20
news = NewsView.as_view()

class NewsDetailsView(DetailView):
    model = News
    template_name = 'pages/news-details.html'
news_details = NewsDetailsView.as_view()

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
