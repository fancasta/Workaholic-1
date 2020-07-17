from django import forms
from django.forms import ModelForm

from accounts.models import *
from .models import Post, Thread

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['content'] 
    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

class ThreadForm(ModelForm):
    class Meta:
        model = Thread
        fields = ['title'] 
    
    def __init__(self, *args, **kwargs):
        super(ThreadForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

class DeleteForm(forms.Form):
    delete = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        super(DeleteForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'