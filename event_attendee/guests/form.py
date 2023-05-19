# Use to render form that get the user input
from django import forms
from django.forms import ValidationError
# from django import forms
import re
from .models import *

class EntryForm(forms.ModelForm):
    # number_vallidate
            # raise ValidationError('Field should not contain character!')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone_number"].widget.attrs.update({'type': 'number'})

    def clean_message(self):
        phone_number = self.cleaned_data['phone_number']
        return phone_number.replace(' ', '') # remove all space from input
    
    class Meta: 
        model = UpcomingInput
        fields = ['phone_number']
        

class AdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["file_name"].widget.attrs.update({"type": "file", 'accept': '.csv'})

    class Meta: 
        model = Csv
        fields = ('file_name',)