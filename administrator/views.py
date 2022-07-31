from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.urls import reverse


class AdminView(LoginRequiredMixin, View):
    login_url = "administrator:login"
    template_name = "administrator/home.html"

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_name)
        else:
            return redirect("administrator:login")


admin_view = AdminView.as_view()


class AdminLogin(View):
    template_name = "administrator/login.html"

    def get(self, request):
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
