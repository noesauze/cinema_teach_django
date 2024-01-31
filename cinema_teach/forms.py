# forms.py

from django import forms

class ImportForm(forms.Form):
    fichier = forms.FileField()
