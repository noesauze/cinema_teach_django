# forms.py

from django import forms

class ImportForm(forms.Form):
    fichier = forms.FileField()

class FormulaireParametresPoint(forms.Form):
    debut = forms.FloatField(label='Début du mouvement', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insérer un nombre'}))
    fin = forms.FloatField(label='Fin du mouvement', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insérer un nombre'}))
    taille_objet = forms.FloatField(label='Taille de l\'objet en cm', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insérer un nombre'}))