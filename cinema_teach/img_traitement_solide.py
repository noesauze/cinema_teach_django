import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO
import csv
import os
from .img_traitment import video_en_image


#Au propre : 1- Masque 2-Déterminer les différents blocs du masque et les différencier 3- Assembler les blocs proches 4- Supprimer les petits pour qu'il n'en reste que 2 5-les afficher sur l'image
#Il faudra que l'utilisateur rentre le nombre de points sur l'objet (nb_paquets_impose) et il pourra modifier la "distance" dans le cas où le regroupement de paquets proches est à retoucher
#1
def calcul_masque_solide (image, gray_fond, seuil):
    gray_frame=cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    (longueur, largeur) = np.shape(gray_fond)
    masque = np.zeros((longueur, largeur),np.uint8)
    #SOLUTION 1
    for x in range (longueur):
        for y in range (largeur):
            if (abs(int(gray_frame[x][y])-int(gray_fond[x][y])))>seuil:
                masque[x][y]=255
    #-------------'''
    #SOLUION 2 
    ''''
    masque_bool = abs(gray_fond - gray_frame)>seuil
    print("masque_bool")
    print(masque_bool)
    masque = masque_bool*np.ones((longueur, largeur), np.uint8)*255
    #------------'''
    kernel=np.ones((5, 5), np.uint8)
    masque=cv.erode(masque, kernel, iterations=3)
    
    nb_labels, labels, stats, centroids = cv.connectedComponentsWithStats(masque)
    return nb_labels,labels,stats,centroids

def dfs(matrice_adjacence, sommet, sommets_visites, sommets_connexes):
    sommets_visites[sommet] = True
    sommets_connexes.append(sommet)
    for voisin in range(len(matrice_adjacence[sommet])):
        if matrice_adjacence[sommet][voisin] == 1 and not sommets_visites[voisin]:
            dfs(matrice_adjacence, voisin, sommets_visites, sommets_connexes)

def trouver_sommets_connexes(matrice_adjacence):
    nb_sommets = len(matrice_adjacence)
    sommets_visites = [False] * nb_sommets
    ensembles_sommets_connexes = []
    for sommet in range(nb_sommets):
        if not sommets_visites[sommet]:
            sommets_connexes = []
            dfs(matrice_adjacence, sommet, sommets_visites, sommets_connexes)
            ensembles_sommets_connexes.append(sommets_connexes)
    return ensembles_sommets_connexes


#3.1 calcul matrice d'adjacence  
def mat_adj_paquets(nb_labels,centroids, distance_paquets):
    
    proximite=np.zeros((nb_labels-1,nb_labels-1))
    for i in range(1, nb_labels-1):
        for j in range(1,nb_labels-1):
            if np.sqrt((centroids[i][0] - centroids[j][0])**2 + (centroids[i][1] - centroids[j][1])**2)<distance_paquets:
                proximite[i-1,j-1]=1
    sommets_connexes=trouver_sommets_connexes(proximite)
    sommets_connexes = [[x + 1 for x in sous_liste] for sous_liste in sommets_connexes]
    return sommets_connexes

#3.2 Transformer label pour rassembler les points proches sous la meme valeur 

def agglomerer_paquets(labels,sommets_connexes):
    (longueur, largeur) = np.shape(labels)
    for k in range(longueur):
        for l in range(largeur):
            if labels[k,l]!=0 :
                for liste in sommets_connexes:
                    if labels[k,l] in liste and len(liste)!=1:
                        labels[k,l]=liste[0]
    return labels



#3.3 Garder seulement 2 ensembles
def selec_paquets(sommets_connexes,stats,nb_paquets_impose):
    #Determiner les paquets assemblés et le nombre de points dans chacun  
    nb_points_ensembles=[]
    for i in range (0,len(sommets_connexes)):
        nb_points=0
        for j in range(0,len(sommets_connexes[i])):
            nb_points= nb_points+stats[sommets_connexes[i][j]][4]
        #On obtient une liste de liste où le premier terme est la valeur d'un des sommets des paquets assemblés et le second terme est la somme des points des paquets assemblés
        nb_points_ensembles.append([sommets_connexes[i][0],nb_points])

    #Choisir les paquets à enlever : dont le nombre de points est faible
    while len(nb_points_ensembles)>nb_paquets_impose:
        list_transit=[] 
        deuxieme_min = min(liste[1] for liste in nb_points_ensembles)
        print(deuxieme_min)
        for i in range (0,len(nb_points_ensembles)):
            if nb_points_ensembles[i][1]>deuxieme_min:
                list_transit.append(nb_points_ensembles[i])
        nb_points_ensembles=list_transit
    nb_points_ensembles_final=nb_points_ensembles
    print(nb_points_ensembles_final)
    return nb_points_ensembles_final


def reduc_nb_paquets(labels, nb_points_ensembles_final):
    #Enlever de label les points qui ne sont pas dans les paquets selectionnées
    for k in range(0,len(labels)):
        for l in range(0,len(labels[k])):
        
            if all(labels[k,l] != liste[0] for liste in nb_points_ensembles_final):
                labels[k,l]=0
    return labels

                


def calc_centre_paquets(centroids,sommets_connexes,nb_points_ensembles_final,stats,nb_paquets_impose):

    #Calcul effectif des centroides avec leur poids une fois les paquets proches rassemblés
    list_centroids=[]
    if (len(nb_paquets_impose)<=len(nb_points_ensembles_final)):
        for i in range(0,nb_paquets_impose):
        
            val_ieme_premier=nb_points_ensembles_final[i][0]-1
            print(nb_points_ensembles_final[i][0])
            for k in range(len(sommets_connexes)):
                if sommets_connexes[k][0]==val_ieme_premier+1:
                    index=k #indice de l'emplacement dans sommets_connexes de la valeur label qui regroupe les blocs 
            list_centroids.append([[centroids[val_ieme_premier+1][0],centroids[val_ieme_premier+1][1]],stats[val_ieme_premier+1][4]])
    
            for j in range(1,len(sommets_connexes[index])):
                list_centroids[i][0][0]=(list_centroids[i][0][0]*list_centroids[i][1] + centroids[sommets_connexes[index][j]][0]*stats[sommets_connexes[index][j]][4])/(list_centroids[i][1]+stats[sommets_connexes[index][j]][4])
                list_centroids[i][0][1]=(list_centroids[i][0][1]*list_centroids[i][1] + centroids[sommets_connexes[index][j]][1]*stats[sommets_connexes[index][j]][4])/(list_centroids[i][1]+stats[sommets_connexes[index][j]][4])
                list_centroids[i][1]=list_centroids[i][1]+stats[sommets_connexes[index][j]][4]
    
    return list_centroids











def plt_fig(image,labels,nb_labels,list_centroids):
    image_couleur = image.copy()

    # Assigner une couleur aléatoire à chaque bloc
    for label in range(1, nb_labels):  # Commencer à 1 car le label 0 représente le fond
    
        couleur = np.random.randint(0, 256, 3)  # Générer une couleur aléatoire (RVB)
        image_couleur[labels == label] = couleur

    # Afficher l'image résultante avec Matplotlib
    plt.imshow(cv.cvtColor(image_couleur, cv.COLOR_BGR2RGB))
    plt.axis('off')  # Désactiver les axes

    #Affichage des centroids
    for ligne in list_centroids:
    # Extraire les coordonnées du premier point de la ligne
        premier_point = ligne[0]
    
    # Extraire les coordonnées x et y du premier point
        x, y = premier_point
    
    # Tracer le point sur le graphique
        plt.scatter(x, y, color='red', marker='o', s=10) 


def new_image_paquet(image,nb_labels,labels):
    for label in range(1, nb_labels):  # Commencer à 1 car le label 0 représente le fond
    
        couleur = np.random.randint(0, 256, 3)  # Générer une couleur aléatoire (RVB)
        image[labels == label] = couleur
    return image

def video_en_donne_solide(total_frame, nom_fichier, video,distance_paquets,nb_paquets_impose):
    tab_donne=[]
    
    for i in range (total_frame):
        nom = "cinema_teach/static/cinema_teach/cache/"+ nom_fichier + "_"+ str(i)+".png"
        image=cv.imread(f"{nom}")
        nb_labels,labels,stats,centroids=calcul_masque_solide(image=image,gray_fond=gray_fond,seuil=65)
        sommets_connexes=mat_adj_paquets(nb_labels,centroids, distance_paquets)
        labels=agglomerer_paquets(labels=labels,sommets_connexes=sommets_connexes)
        nb_points_ensembles_final=selec_paquets(sommets_connexes=sommets_connexes,stats=stats,nb_paquets_impose=nb_paquets_impose)
        labels=reduc_nb_paquets(labels, nb_points_ensembles_final)
        
        #tab_donne.append((calc_centre_paquets(centroids=centroids,sommets_connexes=sommets_connexes,nb_points_ensembles_final=nb_points_ensembles_final,stats=stats,nb_paquets_impose=nb_paquets_impose),i/(video.get(cv.CAP_PROP_FPS))))
    return tab_donne
    


def fichier_video_avec_points(nom_fichier,debut,fin,nb_paquets_impose,distance_paquets,seuil):
    paths=[]
    tab_donne=[]
    fond=cv.imread("cinema_teach/static/cinema_teach/cache/"+nom_fichier + "_0.png")
    gray_fond = cv.cvtColor(fond, cv.COLOR_BGR2GRAY)
    for frame in range (debut,fin+1):
        nom = "cinema_teach/static/cinema_teach/cache/"+ nom_fichier + "_"+ str(frame)+".png"
        image=cv.imread(f"{nom}")
        nb_labels,labels,stats,centroids=calcul_masque_solide(image=image,gray_fond=gray_fond,seuil=seuil)
        sommets_connexes=mat_adj_paquets(nb_labels,centroids, distance_paquets)
        labels=agglomerer_paquets(labels=labels,sommets_connexes=sommets_connexes)
        nb_points_ensembles_final=selec_paquets(sommets_connexes=sommets_connexes,stats=stats,nb_paquets_impose=nb_paquets_impose)
        labels=reduc_nb_paquets(labels, nb_points_ensembles_final)
        image=new_image_paquet(image,nb_labels,labels)
        ##
        #print(type(tab_donne[frame][0][0]))
        
        #tab_donne.append((calc_centre_paquets(centroids,sommets_connexes,nb_points_ensembles_final,stats,nb_paquets_impose)))
        #image=cv.circle(image,(int(tab_donne[frame][0][1]),int(tab_donne[frame][0][0])),2,(0,255,0),-1)
        path="/static/cinema_teach/cache/"+nom_fichier + "_traite_"+ str(frame)+".png"
        cv.imwrite(f'cinema_teach/static/cinema_teach/cache/{nom_fichier + "_traite_"+ str(frame)}.png',image)
        paths.append(path)
    print(paths)
    return paths





    






