from django import forms
from .models import ProcessedImage


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ProcessedImage
        fields = ['original_image', 'filter_used', 'image_name']
