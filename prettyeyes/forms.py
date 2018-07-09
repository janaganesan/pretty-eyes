import glob
from django import forms
from django.core.exceptions import ValidationError

from .config import write_config


def log_file_choices():
    choices = [(str(1), "None")]
    for f in glob.glob("/var/log/debesys/OC_*"):
        choices.append((str((len(choices) + 1)), f))
    return choices


class LogFileNameForm(forms.Form):
    file_name = forms.ChoiceField(label='Log file name', widget=forms.Select(), choices=log_file_choices())

    def clean_file_name(self):
        file_name = dict(self.fields['file_name'].choices)[self.cleaned_data['file_name']]
        if file_name is "None":
            raise ValidationError("Please select a valid log file")
        try:
            with open(file_name, 'r') as f:
                f.readline()
        except:
            raise ValidationError("Unable to read file name: " + file_name)
        write_config({'logfile': file_name})
