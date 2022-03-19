from django import forms
from django.core.exceptions import ValidationError

from .models import Upload


class UploadForm(forms.ModelForm):
    def fileValidator(file):
        if file.size > 1024 * 1000 * 100:
            raise ValidationError("Max size of file is 100 MB")
        
    file = forms.FileField(validators=[fileValidator])
    max_downloads = forms.ChoiceField(
        choices=[
            (1, "1 download"),
            (2, "2 downloads"),
            (3, "3 downloads"),
            (4, "4 downloads"),
            (5, "5 downloads"),
            (20, "20 downloads"),
            (50, "50 downloads"),
            (100, "100 downloads"),
        ]
    )
    expire_duration = forms.ChoiceField(
        choices=[
            (5 * 60, "5 minutes"),
            (60 * 60, "1 hour"),
            (24 * 60 * 60, "1 day"),
            (7 * 24 * 60 * 60, "7 days"),
        ]
    )
    password = forms.CharField(widget= forms.PasswordInput(), required=False)

    class Meta:
        model = Upload
        fields = ["file", "max_downloads", "expire_duration", "password"]


class DownloadForm(forms.ModelForm):
    password = forms.CharField(widget= forms.PasswordInput(), required=False)
    
    class Meta:
        model = Upload
        fields = ["password"]
