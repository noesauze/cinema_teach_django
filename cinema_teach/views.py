import time
import logging
import json
from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from django.shortcuts import render, redirect
from .forms import ImportForm
from .forms import FormulaireParametresPoint
from cinema_teach import img_traitment


def index(request):
    template = loader.get_template("cinema_teach/index.html")
    return HttpResponse(template.render({},request))

def modules(request):
    template = loader.get_template("cinema_teach/modules.html")
    return HttpResponse(template.render({},request))


def resultats_point(request):
    if request.method == 'POST':
        formulaire = FormulaireParametresPoint(request.POST)
        if formulaire.is_valid():
            debut = formulaire.cleaned_data['debut']
            fin = formulaire.cleaned_data['fin']
            taille_objet = formulaire.cleaned_data['taille_objet']
            nom_fichier = request.session['nom_fichier']
            paths = request.session['paths']
            tab_donnees = request.session['tab_donnees']

            print(len(tab_donnees))
            print(debut+fin)
            tab_donnees, paths = img_traitment.decoupe_temporelle(tab_donnees, paths, int(debut), int(fin))

            print(debut)
            print(paths)
            print(tab_donnees)
            

            # Faites quelque chose avec les données du formulaire
            # ...
            return render(request, 'cinema_teach/point-resultats.html', {'nom_fichier': nom_fichier, 'paths': paths})
        else:
            print("non valide")
            print(formulaire.errors)  # Afficher les erreurs de validation du formulaire

            # Le formulaire n'est pas valide, vous pouvez gérer les erreurs ici
            pass
        

    return render(request, 'cinema_teach/point-resultats.html', {'formulaire': formulaire})

def point(request):
    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid() & (request.FILES['fichier'] != None):
            fichier_upload = request.FILES['fichier']
            nom_fichier = str(time.time()).replace(".","-")+"."+fichier_upload.name.split(".")[1]
            destination = open('media/{}'.format(nom_fichier), 'wb+')
            for chunk in fichier_upload.chunks():
                destination.write(chunk)
            destination.close()
            print(nom_fichier)
            tab_donnees, paths = img_traitment.fichier_video_en_images(nom_fichier)
            request.session['tab_donnees'] = tab_donnees
            request.session['paths'] = paths
            request.session['nom_fichier'] = nom_fichier
            formulaire = FormulaireParametresPoint()

            return render(request, 'cinema_teach/point.html', {'nom_fichier': nom_fichier, 'paths': paths, 'formulaire': formulaire})
    else:
        form = ImportForm()

    return render(request, 'cinema_teach/point.html', {'form': form})