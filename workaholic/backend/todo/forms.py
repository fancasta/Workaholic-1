from django import forms

from accounts.models import *

from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['todo']

class EditTodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['todo']

class DeleteForm(forms.Form):
    delete = forms.BooleanField()