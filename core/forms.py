from django import forms
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
# from django.forms import DateInput, TimeInput
# from django.utils import timezone
from .models import *
from froala_editor.widgets import FroalaEditor
# from ckeditor.widgets import CKEditorWidget



class ChapterCreationForm(ModelForm):
    content=forms.CharField(widget=FroalaEditor)
    # content = forms.CharField(widget=TinyMCE())
    class Meta:
        model = Chapter
        fields = ('title','cover_image','content','position','course')

class ChapterChangeForm(ModelForm):
    content=forms.CharField(widget=FroalaEditor)
    # content = forms.CharField(widget=TinyMCE())
    class Meta:
        model = Chapter
        fields = ('title','cover_image','content','position','course')
