from django import forms
from .models import *

from django.contrib.admin import widgets


class UrlBaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UrlBaseForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget.attrs.update({'class': 'form-control'})
        self.fields['shortUrl'].widget.attrs.update({'class': 'form-control'})
        self.fields['longUrl'].widget.attrs.update({'class': 'form-control'})
        self.fields['longUrl'].required = True
        
    class Meta:
        model = UrlBase        
        fields = ['user','shortUrl','longUrl']
