from django import forms

from .models import Board

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['body']
    
    def __init__(self, *args, **kwargs):
        super(BoardForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'