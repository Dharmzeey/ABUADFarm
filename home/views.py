from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


class Home(View):
    template_name = "home/index.html"

    def get(self, request):
        return render(request, self.template_name)


home = Home.as_view()


def agronomy(request):
    return render(request, "farm/agronomy.html")


def feedmill(request):
    return render(request, "farm/feedmill.html")


def fishries(request):
    return render(request, "farm/fishries.html")


def honey(request):
    return render(request, "farm/honey.html")


def mango_juice(request):
    return render(request, "farm/mango-juice.html")


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