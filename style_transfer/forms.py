from django import forms
from .models import Photo, Style


class PhotoForm(forms.ModelForm):


    class Meta:
        model = Photo
        fields = ('image',)
    
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class':'custom-file-input'}))
    
    

class StyleForm(forms.Form):
    
    name = forms.ChoiceField(label='変換スタイル', 
                             choices=lambda:[(item.name, item.name) for item in Style.objects.all().order_by('name')],
                             required=True,)
    
    
