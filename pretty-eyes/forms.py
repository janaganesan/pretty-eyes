from django import forms
from django.core.exceptions import ValidationError

class LogFileNameForm(forms.Form):
    file_name = forms.CharField(label='Log file name', max_length=1024)

    def clean_file_name(self):
        file_name = self.cleaned_data['file_name']
        try:
            with open(file_name, 'r') as f:
                f.readline()
        except:
            raise ValidationError("Unable to read file name: " + file_name)