from django import forms
from.models import *
class LoginTableform(forms.ModelForm):
    class Meta:
        model=LoginTable
        fields=['username','password','usertype']

class usertableform(forms.ModelForm):
    class Meta:
        model=usertable
        fields=['Name','phone_number','emailid','place','img']


class Filetableform(forms.ModelForm):
    class Meta:
        model=FileTable
        fields=['file']
