from django import forms
from models import *


class DataForm(forms.ModelForm):
    numbers_of_error = forms.IntegerField()
    interval = forms.IntegerField()
