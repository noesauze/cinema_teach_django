# forms.py

from django import forms

class ImportForm(forms.Form):
    fichier = forms.FileField()

class ImportFormSolide(forms.Form):
    fichier = forms.FileField()
    """nb_paquets_impose = forms.IntegerField(label='Nombre de points sur le solide', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insérer un nombre'}))
    distance_paquets = forms.FloatField(label='Distance d agglomeration des paquets', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insérer un nombre'})) #Valeur à faire varier pour avoir une agglomération des paquets correcte
"""

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
    nb_paquets_impose = forms.IntegerField(label='Nombre de points sur le solide', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insérer un nombre','value':2}))
    distance_paquets = forms.FloatField(label='Distance d agglomeration des paquets', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insérer un nombre','value':50})) #Valeur à faire varier pour avoir une agglomération des paquets correcte
    seuil = forms.FloatField(label='Seuil de différence entre le fond et la frame', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insérer un nombre','value':70}))
class FormulaireEtalonnageSolide(forms.Form):
    nb_paquets_impose = forms.IntegerField(label='Nombre de points sur le solide', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insérer un nombre'}))
    distance_paquets = forms.FloatField(label='Distance d agglomeration des paquets', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insérer un nombre'})) #Valeur à faire varier pour avoir une agglomération des paquets correcte
    seuil = forms.FloatField(label='Seuil de différence entre le fond et la frame', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insérer un nombre'}))