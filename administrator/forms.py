from django import forms
from users.models import Goods

class AddCustomerGoodForm(forms.ModelForm):
  class Meta:
    model = Goods
    fields = ("quantity", "price", "add_note", "note")
    widgets = {
      "note" : forms.Textarea(attrs={'rows': '4', "cols": "22"}),
    }
    

class AddNewCustomerForm(forms.Form):
  username = forms.CharField(label="Username", max_length=50)
  quantity = forms.FloatField()
  price = forms.FloatField()
  add_note = forms.BooleanField()
  note = forms.CharField(widget=forms.Textarea(attrs={'rows': '4', "cols": "22"}))
