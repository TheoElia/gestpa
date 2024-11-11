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


class JobCreationForm(ModelForm):
    overview=forms.CharField(widget=FroalaEditor)
    description=forms.CharField(widget=FroalaEditor)
    responsibilities=forms.CharField(widget=FroalaEditor)
    requirements=forms.CharField(widget=FroalaEditor)
    benefits=forms.CharField(widget=FroalaEditor)
    # content = forms.CharField(widget=TinyMCE())
    class Meta:
        model = Job
        fields = ('title','cover_image','overview','description','responsibilities',
                  'requirements','benefits','salary','experience_level',
                  'company','job_type','location','application_deadline',
                )