from django import forms
from .models import Program, Module

class ModuleForm(forms.ModelForm):
    module_code = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    module_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    module_leader = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Module
        fields = ['module_code', 'module_name', 'module_leader']


class ProgramForm(forms.ModelForm):
    program_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    program_leader = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Program
        fields = ['program_name', 'program_leader']
        

class UploadFileForm(forms.Form):
    file = forms.FileField()