from django import forms
from .models import *

class AdvertisementForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    class Meta:
        model = Advertisement
        fields = ['adName','addId','adDescription', 'image']
        labels  = {
        'addId':'',
        'adName': '',
        'adDescription' : '',
        'image':'Click here to upload advertisement', 
        }
        widgets = {
            'addId' : forms.TextInput(attrs={'placeholder':'Your unique advertisement ID here'}),
            'adName' : forms.TextInput(attrs={'placeholder':'Your advertisement name here'}),
            'adDescription' : forms.TextInput(attrs={'placeholder':'Your advertisement description here'}),
        }