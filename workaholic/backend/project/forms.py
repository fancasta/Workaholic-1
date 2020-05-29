from django import forms

from accounts.models import *

from .models import Todo

class AddMemberForm(forms.Form):
    project_member = forms.CharField(max_length=20)

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['todo']

class DeleteTodoForm(forms.Form):
    delete = forms.BooleanField()