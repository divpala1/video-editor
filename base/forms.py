from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    
    class Meta:
        model = Video
        fields = "__all__"
        exclude = ['caption_file']
