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
    #for x in range (longueur):
    #    for y in range (largeur):
    #        if (abs(int(gray_frame[x][y])-int(gray_fond[x][y])))>seuil:
    #            masque[x][y]=255
    #-------------'''
    #SOLUION 2 
    gray_fond=gray_fond.astype(int)
    gray_frame=gray_frame.astype(int)
    masque_bool = abs(gray_fond - gray_frame)>seuil
    masque = masque_bool*np.ones((longueur, largeur), np.uint8)*255
    #------------
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
    for i in range(1, nb_labels):
        for j in range(1,nb_labels):
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
        
        for i in range (0,len(nb_points_ensembles)):
            if nb_points_ensembles[i][1]>deuxieme_min:
                list_transit.append(nb_points_ensembles[i])
        nb_points_ensembles=list_transit
    nb_points_ensembles_final=nb_points_ensembles
    
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
    
    for i in range(0,nb_paquets_impose):
        
        val_ieme_premier=nb_points_ensembles_final[i][0]-1
        
        for k in range(len(sommets_connexes)):
            if sommets_connexes[k][0]==val_ieme_premier+1:
                index=k #indice de l'emplacement dans sommets_connexes de la valeur label qui regroupe les blocs 
        list_centroids.append([[centroids[val_ieme_premier+1][0],centroids[val_ieme_premier+1][1]],stats[val_ieme_premier+1][4]])
        for j in range(1,len(sommets_connexes[index])):
            list_centroids[i][0][0]=(list_centroids[i][0][0]*list_centroids[i][1] + centroids[sommets_connexes[index][j]][0]*stats[sommets_connexes[index][j]][4])/(list_centroids[i][1]+stats[sommets_connexes[index][j]][4])
            list_centroids[i][0][1]=(list_centroids[i][0][1]*list_centroids[i][1] + centroids[sommets_connexes[index][j]][1]*stats[sommets_connexes[index][j]][4])/(list_centroids[i][1]+stats[sommets_connexes[index][j]][4])
            list_centroids[i][1]=list_centroids[i][1]+stats[sommets_connexes[index][j]][4]

    return list_centroids #[[(x,y),nb points],...]










'''''
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
        plt.scatter(x, y, color='red', marker='o', s=10) '''

#Il faudra préciser que le nombre de paquets ne doit pas dépasser 5 (ou sinon faire une modification du code)
def new_image_paquet(image,nb_labels,labels):
      # Définir un ensemble de couleurs prédéfinies
    couleurs_predefinies = [ (255,0, 0),(0, 255, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

    # Initialiser un dictionnaire pour stocker les correspondances label-couleur
    correspondances_couleurs = {}

    # Assigner une couleur à chaque label
    for label in range(1, nb_labels):  # Commencer à 1 car le label 0 représente le fond
        # Utiliser un ensemble cyclique de couleurs prédéfinies
        couleur = couleurs_predefinies[(label - 1) % len(couleurs_predefinies)]
        correspondances_couleurs[label] = couleur

    # Appliquer les couleurs à l'image en fonction des labels
    for label, couleur in correspondances_couleurs.items():
        image[labels == label] = couleur

    return image


    


def fichier_video_avec_points(nom_fichier,debut,fin,nb_paquets_impose,distance_paquets,seuil):
    paths=[]
    paths_centre=[]
    tab_donne=[]
    k=0
    video=cv.VideoCapture("media/"+nom_fichier)
    fond=cv.imread("cinema_teach/static/cinema_teach/cache/"+nom_fichier + "_0.png")
    gray_fond = cv.cvtColor(fond, cv.COLOR_BGR2GRAY)
    for frame in range (debut,fin+1):
        nom = "cinema_teach/static/cinema_teach/cache/"+ nom_fichier + "_"+ str(frame)+".png"
        image=cv.imread(f"{nom}")
        image_centre=cv.imread(f"{nom}")
        nb_labels,labels,stats,centroids=calcul_masque_solide(image=image,gray_fond=gray_fond,seuil=seuil)

        if nb_labels>=nb_paquets_impose:
            sommets_connexes=mat_adj_paquets(nb_labels,centroids, distance_paquets)
            labels=agglomerer_paquets(labels=labels,sommets_connexes=sommets_connexes)
            nb_points_ensembles_final=selec_paquets(sommets_connexes=sommets_connexes,stats=stats,nb_paquets_impose=nb_paquets_impose)
            labels=reduc_nb_paquets(labels, nb_points_ensembles_final)
            tab_donne.append((calc_centre_paquets(centroids,sommets_connexes,nb_points_ensembles_final,stats,nb_paquets_impose),frame/(video.get(cv.CAP_PROP_FPS))))
           
            for j in range(nb_paquets_impose):
                
                image_centre=cv.circle(image_centre,(int(tab_donne[frame-debut-k][0][j][0][0]),int(tab_donne[frame-debut-k][0][j][0][1])),5,(0,0,255),-1)
            
            path_centre="/static/cinema_teach/cache/"+nom_fichier + "_centre_"+ str(frame)+".png"
            cv.imwrite(f'cinema_teach/static/cinema_teach/cache/{nom_fichier + "_centre_"+ str(frame)}.png',image_centre)
            paths_centre.append(path_centre)

            image=new_image_paquet(image,nb_labels,labels)
        
            #[[[(x,y),nb points],...],time]
            
        else :
            k=k+1
            print('k=')
            
        path="/static/cinema_teach/cache/"+nom_fichier + "_traite_"+ str(frame)+".png"
        cv.imwrite(f'cinema_teach/static/cinema_teach/cache/{nom_fichier + "_traite_"+ str(frame)}.png',image)
        paths.append(path)
        
    return paths,tab_donne,paths_centre #comporte que les données où il y a quelque chose à voir





    
# Fonction de conversion pour gérer la sérialisation des tableaux NumPy et autres objets non sérialisables en JSON
def convert_to_json_serializable(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()  # Convertir les tableaux NumPy en listes Python
    elif isinstance(obj, np.float64):
        return float(obj)  # Convertir les numpy.float64 en float Python
    elif isinstance(obj, np.intc):
        return int(obj)  # Convertir les numpy.intc en int Python
    elif isinstance(obj, tuple):
        return [convert_to_json_serializable(item) for item in obj]
    elif isinstance(obj, list):
        return [convert_to_json_serializable(item) for item in obj]
    else:
        return obj




