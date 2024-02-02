import time
import logging
from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from django.shortcuts import render, redirect
from .forms import ImportForm
from cinema_teach import img_traitment


def index(request):
    template = loader.get_template("cinema_teach/index.html")
    return HttpResponse(template.render({},request))

def modules(request):
    template = loader.get_template("cinema_teach/modules.html")
    return HttpResponse(template.render({},request))

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
            tab_images, paths = img_traitment.fichier_video_en_images(nom_fichier)
            print(paths)
            # Vous pouvez effectuer d'autres opérations ici si nécessaire
            return render(request, 'cinema_teach/point.html', {'nom_fichier': nom_fichier, 'paths': paths})
    else:
        form = ImportForm()

    return render(request, 'cinema_teach/point.html', {'form': form})

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
            tab_images, paths = img_traitment.fichier_video_en_images(nom_fichier)
            print(paths)
            # Vous pouvez effectuer d'autres opérations ici si nécessaire
            return render(request, 'cinema_teach/solide.html', {'nom_fichier': nom_fichier, 'paths': paths})
    else:
        form = ImportForm()

    return render(request, 'cinema_teach/solide.html', {'form': form})