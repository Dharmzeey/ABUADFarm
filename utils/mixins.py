from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

class AdminRequiredMixin(LoginRequiredMixin):
  
  """Verify that the current user is superuser."""
  def dispatch(self, request, *args, **kwargs):
    if not request.user.is_superuser:
      return redirect('home')
    return super().dispatch(request, *args, **kwargs)


class StaffRequiredMixin(LoginRequiredMixin):
  
  """Verify that the current user is staff."""
  def dispatch(self, request, *args, **kwargs):
    if not request.user.is_staff or request.user.is_superuser:
      return redirect('home')
    return super().dispatch(request, *args, **kwargs)