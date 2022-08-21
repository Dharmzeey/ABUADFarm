from ckeditor.widgets import CKEditorWidget
from django import forms
from users.models import Goods, Messages
from .models import StaffModel
from products.models import Product

class AddCustomerGoodForm(forms.ModelForm):
  class Meta:
    model = Goods
    fields = ("item", "quantity", "price", "add_description", "description")
    widgets = {
      # "description" : forms.Textarea(attrs={'rows': '4', "cols": "22"}),
      "add_description": forms.CheckboxInput()
    }
    
  def __init__(self, *args, **kwargs):
      self.request = kwargs.pop('request', None)
      user = self.request.user
      unit_name = StaffModel.objects.get(owner=user).unit
      super(AddCustomerGoodForm, self).__init__(*args, **kwargs)
      if user != None:
        self.fields['item']=forms.ModelChoiceField(queryset=Product.objects.filter(unit=unit_name))
    

class AddNewCustomerForm(forms.Form):
  username = forms.CharField(label="Username", max_length=50)
  item = forms.ModelChoiceField(queryset=None)
  quantity = forms.FloatField()
  price = forms.FloatField()
  add_description = forms.BooleanField(required=False)
  description = forms.CharField(required=False, widget=CKEditorWidget())
  
  def __init__(self, *args, **kwargs):
    self.request = kwargs.pop('request', None)
    user = self.request.user
    unit_name = StaffModel.objects.get(owner=user).unit
    super(AddNewCustomerForm, self).__init__(*args, **kwargs)
    if user != None:
        self.fields['item']=forms.ModelChoiceField(queryset=Product.objects.filter(unit=unit_name))


class SendCustomerMessageForm(forms.ModelForm):
  class Meta:
    model = Messages
    fields = ("title", "body")
    widgets = {
      "body" : forms.Textarea(attrs={'rows': '4', "cols": "22"}),
    }