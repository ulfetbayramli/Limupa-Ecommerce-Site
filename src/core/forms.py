from django import forms
from .models import Subscriber




class SubscriberForm(forms.ModelForm):
    class Meta:
        ModuleNotFoundError = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class':'input-text required-entry validate-email', 'type': 'text'})
        }