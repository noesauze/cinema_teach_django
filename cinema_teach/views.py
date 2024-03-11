import math
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
from .forms import ImportForm, ImportFormSolide
from .forms import FormulaireParametresPoint
from .forms import FormulaireParametresSolide
from .forms import FormulaireEtalonnageSolide
from cinema_teach import img_traitment
from cinema_teach import img_traitement_solide
from django.http import HttpResponse
from .meca_point import plot_fig

import tkinter as tk
from PIL import Image, ImageTk

from django.http import JsonResponse



def index(request):
    template = loader.get_template("cinema_teach/index.html")
    return HttpResponse(template.render({},request))

def modules(request):
    template = loader.get_template("cinema_teach/modules.html")
    return HttpResponse(template.render({},request))

def about(request):
    template = loader.get_template("cinema_teach/about.html")
    return HttpResponse(template.render({},request))


def resultats_point(request):
    if request.method == 'POST':
        formulaire = FormulaireParametresPoint(request.POST)
        if formulaire.is_valid():
            debut = formulaire.cleaned_data['debut']
            fin = formulaire.cleaned_data['fin']
            taille_objet = formulaire.cleaned_data['taille_objet']
            nom_fichier = request.session['nom_fichier']
            tab_donnees = request.session['tab_donnees']
            paths_traites=img_traitment.fichier_video_avec_points(nom_fichier,int(debut),int(fin),tab_donnees)
            tab_donnees = json.loads(str(img_traitment.decoupe_temporelle(tab_donnees, int(debut), int(fin))))

            request.session['path_traites'] = paths_traites
            


            image_data = plot_fig(tab_donnees, int(taille_objet))


            return render(request, 'cinema_teach/point-resultats.html', {'nom_fichier': nom_fichier, 'paths': paths_traites, 'image_data':image_data})
        else:
            print("non valide")
            print(formulaire.errors)  # Afficher les erreurs de validation du formulaire

            # Le formulaire n'est pas valide, vous pouvez gérer les erreurs ici
            pass
        

    return render(request, 'cinema_teach/point-resultats.html', {})

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
            # Récupérer les coordonnées du point cliqué depuis la requête POST
            x = request.POST.get('x')
            y = request.POST.get('y')
            
            # Renvoyer les coordonnées du point enregistré
            return JsonResponse({'x': point.x, 'y': point.y})
    else:
        form = ImportForm()
        request.session['pointsEchelle'] = []

    return render(request, 'cinema_teach/point.html', {'form': form, 'formulaire':FormulaireParametresPoint()})

def post_point(request):
    print("dans la vue")
    if request.method == 'POST':
        print("dans le if")
        x = request.POST.get('x')
        y = request.POST.get('y')
        print(x, y)
        if len(request.session['pointsEchelle']) != 0:
            request.session['pointsEchelle'].append([float(x), float(y)])
            print(request.session['pointsEchelle'][0], request.session['pointsEchelle'][1])
            request.session['distancePixels'] = math.dist([float(request.session['pointsEchelle'][0][0]), float(request.session['pointsEchelle'][0][1])], request.session['pointsEchelle'][1])
            print(request.session['distancePixels'])
            request.session['pointsEchelle']=request.session['pointsEchelle'][1:]
        else:
            request.session['pointsEchelle'].append([float(x), float(y)])
            request.session['distancePixels']=0
            
        # Renvoyer les coordonnées du point enregistré
        reponse = JsonResponse({'x': x, 'y': y, 'distance':round(request.session["distancePixels"], 1)})

        return reponse


def solide(request):
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
            
            
            formulaire = FormulaireParametresSolide()

            print(paths)
            # Vous pouvez effectuer d'autres opérations ici si nécessaire
            return render(request, 'cinema_teach/solide.html', {'nom_fichier': nom_fichier, 'paths': paths,'formulaire': formulaire})
    else:
        form = ImportForm()

    return render(request, 'cinema_teach/solide.html', {'form': form,'formulaire': FormulaireParametresSolide})

def vider(request):

    for path in request.session['paths']:
        img_traitment.supprimer_fichier(path)
    for path in request.session['paths_traites']:
        img_traitment.supprimer_fichier(path)

    img_traitment.supprimer_fichier("media/"+request.session['nom_fichier'])
    response = JsonResponse({'message': 'Cache vidé avec succès.'})
    # Ajouter des en-têtes pour indiquer au navigateur de vider le cache
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    return response


def etalonnage_solide(request):
    
    
    
    if request.method == 'POST':
        debut = request.session['debut']
        fin = request.session['fin']
        formulaire = FormulaireEtalonnageSolide(request.POST, initial={'debut': debut, 'fin': fin})
        
        if formulaire.is_valid():

            nb_paquets_impose = formulaire.cleaned_data['nb_paquets_impose']
            distance_paquets = formulaire.cleaned_data['distance_paquets']
            seuil = formulaire.cleaned_data['seuil']
            nom_fichier = request.session['nom_fichier']
            tab_donnees = request.session['tab_donnees']
            
           
            paths_traites=img_traitement_solide.fichier_video_avec_points(nom_fichier,int(debut),int(fin),nb_paquets_impose,distance_paquets,seuil)
            tab_donnees = json.loads(str(img_traitment.decoupe_temporelle(tab_donnees, int(debut), int(fin))))
            
            
            request.session['path_traites'] = paths_traites
            request.session['seuil']=seuil
            request.session['nb_paquets_impose']=nb_paquets_impose
            request.session['distance_paquets']=distance_paquets
          
            return render(request, 'cinema_teach/solide-etalonnage.html', {'nom_fichier': nom_fichier, 'paths': paths_traites,  'formulaire':formulaire})
        else:
            print("non valide")
            print(formulaire.errors)  # Afficher les erreurs de validation du formulaire
  
            # Le formulaire n'est pas valide, vous pouvez gérer les erreurs ici
            pass
    
    
    return render(request, 'cinema_teach/solide-etalonnage.html', {})

def resultats_solide(request):
    if request.method == 'POST':
        formulaire = FormulaireParametresSolide(request.POST)
        if formulaire.is_valid():
            debut = formulaire.cleaned_data['debut']
            fin = formulaire.cleaned_data['fin']
            nb_paquets_impose = formulaire.cleaned_data['nb_paquets_impose']
            distance_paquets = formulaire.cleaned_data['distance_paquets']
            seuil = formulaire.cleaned_data['seuil']
            taille_objet = formulaire.cleaned_data['taille_objet']
            nom_fichier = request.session['nom_fichier']
            tab_donnees = request.session['tab_donnees']
            paths_traites=img_traitement_solide.fichier_video_avec_points(nom_fichier,int(debut),int(fin),tab_donnees)
            tab_donnees = json.loads(str(img_traitment.decoupe_temporelle(tab_donnees, int(debut), int(fin))))

            request.session['path_traites'] = paths_traites
            


            image_data = plot_fig(tab_donnees, int(taille_objet))


            return render(request, 'cinema_teach/solide-resultats.html', {'nom_fichier': nom_fichier, 'paths': paths_traites, 'image_data':image_data})
        else:
            print("non valide")
            print(formulaire.errors)  # Afficher les erreurs de validation du formulaire

            # Le formulaire n'est pas valide, vous pouvez gérer les erreurs ici
            pass
        

    return render(request, 'cinema_teach/solide-resultats.html', {})


def post_solide(request):
    print("dans la vue")
    if request.method == 'POST':
        print("dans le if")
        x = request.POST.get('x')
        y = request.POST.get('y')
        print(x, y)
        if len(request.session['pointsEchelle']) != 0:
            request.session['pointsEchelle'].append([float(x), float(y)])
            print(request.session['pointsEchelle'][0], request.session['pointsEchelle'][1])
            request.session['distancePixels'] = math.dist([float(request.session['pointsEchelle'][0][0]), float(request.session['pointsEchelle'][0][1])], request.session['pointsEchelle'][1])
            print(request.session['distancePixels'])
            request.session['pointsEchelle']=request.session['pointsEchelle'][1:]
        else:
            request.session['pointsEchelle'].append([float(x), float(y)])
            request.session['distancePixels']=0
            
        # Renvoyer les coordonnées du point enregistré
        reponse = JsonResponse({'x': x, 'y': y, 'distance':round(request.session["distancePixels"], 1)})

        return reponse


