import cv2
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO
import csv
#Calcul du masque d'un objet par soustraction 
def calcul_masque (image, gray_fond, seuil):
    gray_frame=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    (longueur, largeur) = np.shape(gray_fond)
    masque = np.zeros((longueur, largeur))
    for x in range (longueur):
        for y in range (largeur):
            if (abs(int(gray_frame[x][y])-int(gray_fond[x][y])))>seuil:
                masque[x][y]=255
    kernel=np.ones((5, 5), np.uint8)
    masque=cv2.erode(masque, kernel, iterations=3)
    return masque

#Calcul du centre de l'objet grâce à son masque
def calcul_centre (masque):
    moy_x=0
    moy_y=0
    nb=0
    (longueur, largeur) = np.shape(masque)
    for x in range (longueur):
        for y in range(largeur):
            if masque[x][y]!=0:
                nb+=1
                moy_x=((moy_x*(nb-1))+x)/nb
                moy_y=((moy_y*(nb-1))+y)/nb
    return (np.floor(moy_x),np.floor(moy_y))

#Converti une vidéo en tableau d'image au format png
def video_en_image(video, nom_fichier):
    # Vérifier si la vidéo est ouverte
    if not video.isOpened():
        print("Erreur: Impossible d'ouvrir la vidéo.")
    total_frame=int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    paths = []
    for frame in range (total_frame):
        video.set(cv2.CAP_PROP_POS_FRAMES,frame)
        success,image=video.read()
        if success:
            path = "/static/cinema_teach/cache/"+nom_fichier + "_"+ str(frame)+ ".png"
            cv2.imwrite(f'cinema_teach/static/cinema_teach/cache/{nom_fichier + "_"+ str(frame)}.png',image)
            paths.append(path)
    return total_frame, paths

#Fonction principal qui prend en paramètre une vidéo et la transforme en un tableau avec l'ensemble des centres de l'objet
def video_en_donne(total_frame, nom_fichier, video):
    tab_donne=[]
    fond=cv2.imread("cinema_teach/static/cinema_teach/cache/"+nom_fichier + "_0.png")
    gray_fond = cv2.cvtColor(fond, cv2.COLOR_BGR2GRAY)
    for i in range (total_frame):
        nom = "cinema_teach/static/cinema_teach/cache/"+ nom_fichier + "_"+ str(i)+".png"
        image=cv2.imread(f"{nom}")
        masque=calcul_masque(image=image,gray_fond=gray_fond,seuil=10)
        tab_donne.append((calcul_centre(masque=masque),i/(video.get(cv2.CAP_PROP_FPS))))
    return tab_donne

def fichier_video_en_images(nom_fichier):
    video=cv2.VideoCapture("media/"+nom_fichier)
    total_frame, paths=video_en_image(video=video, nom_fichier=nom_fichier)
    tab_donne = video_en_donne(total_frame=total_frame, nom_fichier=nom_fichier, video=video)
    return tab_donne, paths

def decoupe_temporelle(tab_donne, debut, fin,paths=[]):
    return tab_donne[debut:fin+1]

def fichier_video_avec_points(nom_fichier,debut,fin,tab_donne):
    paths=[]
    for frame in range (debut,fin+1):
        print(type(tab_donne[frame][0][0]))
        image=cv2.imread(f'cinema_teach/static/cinema_teach/cache/{nom_fichier + "_"+ str(frame)}.png')
        image=cv2.circle(image,(int(tab_donne[frame][0][1]),int(tab_donne[frame][0][0])),2,(0,255,0),-1)
        path="/static/cinema_teach/cache/"+nom_fichier + "_traite_"+ str(frame)+".png"
        cv2.imwrite(f'cinema_teach/static/cinema_teach/cache/{nom_fichier + "_traite_"+ str(frame)}.png',image)
        paths.append(path)
    print(paths)
    return paths