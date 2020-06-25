from django import forms
from django.forms import ModelForm, DateInput, Select, widgets
from .models import Event

LABEL_TYPES = (('Meeting','Meeting'), ('Submission','Submission'), ('Others','Others'), (None, None))

class EventForm(ModelForm):
    class Meta:
        model = Event
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'label': Select(choices=LABEL_TYPES)
        }
        fields = ['title','description','start_time','end_time', 'label']

    
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'
            
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['start_time'].required = False
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].required = False
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    



#attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'