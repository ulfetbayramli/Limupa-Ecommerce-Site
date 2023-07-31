from django import forms
from .models import Subscriber, Contact




class SubscriberForm(forms.ModelForm):
    class Meta:
        ModuleNotFoundError = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class':'input-text required-entry validate-email', 'type': 'text'})
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        
