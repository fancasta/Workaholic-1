from django import forms

from accounts.models import *

class AddMemberForm(forms.Form):
    project_member = forms.CharField(max_length=20)

    def __init__(self, *args, **kwargs):
        super(AddMemberForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

class SetAdminForm(forms.Form):
    set_admin = forms.BooleanField()
    def __init__(self, *args, **kwargs):
        super(SetAdminForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'