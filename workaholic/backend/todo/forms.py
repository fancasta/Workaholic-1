from django import forms
from django.forms import DateInput
from accounts.models import *

from .models import Todo

from accounts.models import *


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        widgets = {
            'deadline': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),            
        }
        fields = ['title', 'description','assigned_to', 'deadline']

    def __init__(self, pk,*args, **kwargs):
        super(TodoForm, self).__init__(*args, **kwargs)
        project = Project.objects.get(id=pk)
        self.fields['deadline'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['assigned_to'].queryset = project.project_members.all()

class DeleteForm(forms.Form):
    delete = forms.BooleanField()