from django import forms
from django.core.exceptions import ValidationError
import os

class UploadFileForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Check file extension
            if not file.name.lower().endswith('.csv'):
                raise ValidationError('Only CSV files are allowed.')

            # Check file size (10MB limit)
            if file.size > 10 * 1024 * 1024:
                raise ValidationError('File size must be under 10MB.')

        return file
