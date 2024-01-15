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

class ActionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ActionForm, self).__init__(*args, **kwargs)
        self.fields['shortDescription'].widget.attrs.update({'class': 'form-control'})        
        self.fields['itsOn'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['dateStart'].widget.attrs.update({'class': 'form-control'})
        self.fields['dateEnd'].widget.attrs.update({'class': 'form-control'})
        self.fields['countPoint'].widget.attrs.update({'class': 'form-control'})
        self.fields['dateEndPoint'].widget.attrs.update({'class': 'form-control'})
        self.fields['limitCountOn'].widget.attrs.update({'class': 'form-control'})
        self.fields['emailZone'].widget.attrs.update({'class': 'form-control'})
        
    class Meta:
        model = Action        
        fields = ['shortDescription','itsOn','dateStart','dateEnd','countPoint','dateEndPoint','limitCountOn','emailZone']

class PromoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PromoForm, self).__init__(*args, **kwargs)
        self.fields['action'].queryset = Action.objects.filter(itsOn=True)
        self.fields['action'].widget.attrs.update({'class': 'form-control'})
        self.fields['stringPromo'].widget.attrs.update({'class': 'form-control'})
        self.fields['itsOn'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['dateEnd'].widget.attrs.update({'class': 'form-control'})
        self.fields['limitCountOn'].widget.attrs.update({'class': 'form-control'})
        
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        
    class Meta:
        model = Promo        
        fields = ['action','stringPromo','itsOn','dateEnd','limitCountOn','email']