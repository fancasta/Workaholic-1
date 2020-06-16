from django import forms

from accounts.models import *

class AddMemberForm(forms.Form):
    project_member = forms.CharField(max_length=20)

class SetAdminForm(forms.Form):
    set_admin = forms.BooleanField()