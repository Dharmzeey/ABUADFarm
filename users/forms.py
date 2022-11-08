from django import forms

from .models import Profile, LGA


class ProfileUpdateForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = "__all__"
    exclude = ('owner',)
    
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['local_government'].queryset = LGA.objects.none()
    
    if 'state' in self.data and 'local_government' in self.data:
      try:
        state_id = int(self.data.get('state'))
        
        self.fields['local_government'].queryset = LGA.objects.filter(state__id=state_id).order_by('name')
      except:
        pass
    elif self.instance.pk:
      self.fields['local_government'].queryset = self.instance.state.lga_set.order_by('name')

class GetFeedback(forms.Form):
  feedback = forms.CharField()