from django import forms
from django.forms.widgets import NumberInput, HiddenInput
from django.db.models import fields
from auctions.models import Bids, Comments
from django.forms import ModelForm
from django.db import models




CATEGORIES = (
   ('gr', 'groceries'),
   ('cl', 'clothing'),
   ('bk', 'books'),
   ('fn', 'furniture'),
   ('ft', 'fitness'),
   ('gm', 'games'),
   ('gd', 'gadjets'),
   ('no', 'None'),
)

#create form for listing
class Create_form(forms.Form):
    title = forms.CharField(label="Title", max_length=64, widget=forms.Textarea(attrs={'rows':1, 'class':'form-control'}))
    image = forms.URLField(label="Image URL", max_length=200, error_messages={
        'task': {'max_length': ("Error: max length is set at 255 characters")}}, widget=forms.URLInput(attrs={'rows':3, 'class': 'form-control'}))
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={'rows':3, 'class':'form-control'}), max_length=500)
    price = forms.IntegerField(label="Price", widget=forms.NumberInput (attrs={'rows':1,'class':'form-control'}))
    date_created = forms.DateField(widget=NumberInput(attrs={'type': 'date', 'class':'form-control'}))
    categories = forms.ChoiceField(choices=CATEGORIES, widget=forms.RadioSelect)

#craete comment form
class Comment_form(forms.Form):
    name = forms.CharField(label="Name", max_length=64, widget=forms.Textarea(attrs={'rows' :1, 'class': 'form-control'}))
    email = forms.CharField(label="Email", widget=forms.EmailInput(attrs={'rows' :1, 'class': 'form-control'}))
    content = forms.CharField(label="Description", widget=forms.Textarea(attrs={'rows' :3, 'class': 'form-control'}), max_length=500)

#create bidding form
class Bid_form(forms.Form):
    bid = forms.IntegerField(label="Bid", widget=forms.NumberInput (attrs={'rows':1,'class':'form-control'}))