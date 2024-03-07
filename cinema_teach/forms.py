# forms.py

from django import forms

class ImportForm(forms.Form):
    fichier = forms.FileField()

class FormulaireParametresPoint(forms.Form):
    debut = forms.FloatField(label='Début du mouvement', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insérer un nombre'}))
    fin = forms.FloatField(label='Fin du mouvement', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insérer un nombre'}))
    taille_objet = forms.FloatField(label='Taille de l\'objet en cm', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insérer un nombre'}))
    taille_pixels = forms.FloatField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mesurer une distance sur une image', 'id': 'pixels'}))

class FormulaireParametresSolide(forms.Form):
    debut = forms.FloatField(label='Début du mouvement', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insérer un nombre'}))
    fin = forms.FloatField(label='Fin du mouvement', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insérer un nombre'}))
    taille_objet = forms.FloatField(label='Taille de l\'objet en cm', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insérer un nombre'}))
    taille_pixels = forms.FloatField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mesurer une distance sur une image', 'id': 'pixels'}))
    nb_paquets_impose = forms.FloatField(label='Nombre de points sur le solide', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insérer un nombre'}))
    distance = forms.FloatField(label='Distance d agglomeration des paquets', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insérer un nombre'})) #Valeur à faire varier pour avoir une agglomération des paquets correcte