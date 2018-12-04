_auther_ = 'Harry'
_date_ = '12/2/2018 11:22 PM'

from django import forms

class ChangeForm(forms.Form):
    oldPsw = forms.CharField(required=True, label="Old Password")
    newPsw = forms.CharField(required=True, label="New Password")
    newPsw2 = forms.CharField(required=True, label="Confirmed Password")


