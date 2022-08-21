from django import forms

from .models import Profile


class ProfileUpdateForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = "__all__"
    exclude = ('owner',)


class GetFeedback(forms.Form):
  feedback = forms.CharField()