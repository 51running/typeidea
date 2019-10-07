#encoding:utf-8
from django import forms


class PostAdminForms(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)