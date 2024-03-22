import numpy as np

import matplotlib as plt
import cv2 as cv
from scipy.optimize import minimize


#Cette fonction associe le paquet  de l'image 1 au bon paquet de l'image 2. Il le fait pour tous les paquets d'une image. Il retourne une liste avec la position dans tab_donnes 
def assign_paquets(frame,tab_donnes):
    
    distance_min=[]
    
    for i in range(len(tab_donnes[frame][0])):
        
        distance_glob=[]
        for j in range(len(tab_donnes[frame+1][0])):
            
            distance_glob.append(np.sqrt((tab_donnes[frame][0][i][0][0] - tab_donnes[frame+1][0][j][0][0])**2 + (tab_donnes[frame][0][i][0][1] - tab_donnes[frame+1][0][j][0][1])**2))
            
        distance_min.append([i,np.argmin(distance_glob)])
    return distance_min #[[paquetx im1,paquetx im2],...]

#Cette fonction retourne 
def calculate_vitesses(frame,tab_donnes):
    list_vitesses=[]
    linked_paquets=assign_paquets(frame,tab_donnes)
    for i in range(len(linked_paquets)):#attention range of frame
        
        t1=tab_donnes[frame][1]
        t2=tab_donnes[frame+1][1]
        vx= (tab_donnes[frame][0][linked_paquets[i][0]][0][0]-tab_donnes[frame+1][0][linked_paquets[i][1]][0][0])/(t1-t2)
        vy= (tab_donnes[frame][0][linked_paquets[i][0]][0][1]-tab_donnes[frame+1][0][linked_paquets[i][1]][0][1])/(t1-t2)
        list_vitesses.append([[vx,vy],[tab_donnes[frame+1][0][linked_paquets[i][1]][0][0],tab_donnes[frame+1][0][linked_paquets[i][1]][0][1]]])
    return list_vitesses #[[[vx,vy],[x2,y2]],...]

#Cette fonction retourne une liste avec les vitesses et points de départ de ces derniers pour chaque marque et chaque image
def video_vitesses(tab_donnes):
    video_vitesses=[]
    for frame in range(len(tab_donnes)-1):
        list_vitesses=calculate_vitesses(frame,tab_donnes)
        video_vitesses.append(list_vitesses)
    return video_vitesses

#On définit les vecteurs perpendiculaires à tous les vecteurs vitesse des centroides
def cal_perpendiculaires(list_vitesses):
    n=len(list_vitesses)
    for k in range(n):
        vect_perpendiculaire=list_vitesses
        vect_perpendiculaire[k][0][0][0],vect_perpendiculaire[k][0][0][1]=-vect_perpendiculaire[k][0][0][1],vect_perpendiculaire[k][0][0][0]
        vect_perpendiculaire[k][1][0][0],vect_perpendiculaire[k][1][0][1]=-vect_perpendiculaire[k][1][0][1],vect_perpendiculaire[k][1][0][0]
    return vect_perpendiculaire

'''''
#Ancienne methode de calcul de CIR pour seulement 2 marques
def cir(list_centroids): #probleme car pas forcement que deux paquets, ou faire varier la formule en fonction du nombre de points
    list_perpendiculaires=cal_perpendiculaires(list_centroids)
    n=len(list_centroids)
    CIR=[]
            
    for k in range(n):
        Vx1=list_perpendiculaires[k][0][0][0]
        Vy1=list_perpendiculaires[k][0][0][1]
        x1=list_perpendiculaires[k][0][1][0]
        y1=list_perpendiculaires[k][0][1][1]
        Vx2=list_perpendiculaires[k][1][0][0]
        Vy2=list_perpendiculaires[k][1][0][1]
        x2=list_perpendiculaires[k][1][1][0]
        y2=list_perpendiculaires[k][1][1][1]
        Px = ((Vy1 * x1 - Vx1 * y1) * (Vx2 * Vy2) - (Vx1 * y1 - Vy1 * x1) * (Vx2 * Vy2)) / (Vx1 * Vy2 - Vy1 * Vx2)
        Py = ((Vy1 * x1 - Vx1 * y1) * (Vx2 * Vy2) - (Vx1 * y1 - Vy1 * x1) * (Vx2 * Vy2)) / (Vx1 * Vy2 - Vy1 * Vx2)
        CIR.append([Px,Py])
    return CIR
'''

#Cette fonction retourne les paramètres a et b des fonctions de type y=ax+b. La fonction est la droite perpendiculaire de chaque vecteur vitesse
def Param_Droites(list_perpendiculaires, frame):
    
    params=[]
    for i in range(len(list_perpendiculaires[0])):
        
        
        a=list_perpendiculaires[frame][i][0][1]/list_perpendiculaires[frame][i][0][0] #Vy/Vx pour la perpendiculaire
        b=-(list_perpendiculaires[frame][i][0][1]/list_perpendiculaires[frame][i][0][0])*list_perpendiculaires[frame][i][1][0]+list_perpendiculaires[frame][i][1][1] #-Vy/Vx*x1+y1
        
        params.append([a,b])
    
        
    return  params

#Cette fonction permet de calculer les distances
def distance_to_lines(point, *params):
    x, y = point
    distances = []
    
    for i in range(len(params[0])):
        a=params[0][i][0]
        b=params[0][i][1]
        
        # Calcul de la distance entre le point et la droite
        distance = abs(a*x + b - y) / np.sqrt(a**2 + 1)
        distances.append(distance)
    
    return sum(distances)

#Cette fonction permet de calculer le CIR c'est à dire le point le plus proche de toutes les droites perpendiculaires aux vecteurs vitesses des marque sur le solide.
def CIR(params):
    # Point initial
    initial_point = [0, 0]

    # Minimisation de la distance
    result = minimize(distance_to_lines, initial_point,args=(params,), method='Nelder-Mead')
    closest_point = result.x


    return closest_point

#Cette  fonction regroupe les CIR (x,y) en pixels de toutes les images dans une liste
def calcul_video_CIR(vect_perpendiculaire):
    video_CIR=[]
    for frame in range(len(vect_perpendiculaire)):
        params=Param_Droites(vect_perpendiculaire, frame)
        closest_point=CIR(params)
        video_CIR.append(closest_point)
    return video_CIR




#Cette fonction prend notamment en entrée le chemin d'accès des images avec un poiunt marquant le centroid de chaque marque.
#Elle permet d'afficher sur les images les vecteurs vitesses. Cependant ces vecteurs vitesses dépassent de l'image on diminue leur taille pour plus de lisibilisté notamment grace à un facteur x. 
#Cette solution est provisoire et nous devrons trouver un moyen d'adapter cette diminution à la taille de l'image et valeur des vectreurs vitesses
#(par exemple :laisser à l'utilisateur de choisir le x).
def affichage_vector(paths_centre,tab_donnes,nb_labels,nom_fichier,debut):

    paths_vector=[]
    path_prem_image="/static/cinema_teach/cache/"+nom_fichier + "_centre_"+ str(int(debut))+".png"
    paths_vector.append(path_prem_image)
    
    for frame in range(1,len(paths_centre)):
        nom2 = "cinema_teach/static/cinema_teach/cache/"+ nom_fichier + "_centre_"+ str(int(frame+debut))+".png"
        
        image=cv.imread(nom2)
        list_vitesses=calculate_vitesses(frame-1,tab_donnes)
        
        for i in range(nb_labels):
            
            
            
            
        
            
            x=0.5
            start=[int(list_vitesses[i][1][0]),int(list_vitesses[i][1][1])]
           
            vector=[int(list_vitesses[i][0][0]*x),int(list_vitesses[i][0][1]*x)]
            
           
            
            end_point = [start[0] + vector[0], start[1] + vector[1]]
            
            image=cv.arrowedLine(image, start, end_point, (0, 0, 255), thickness=2)
            
            
        path="/static/cinema_teach/cache/"+nom_fichier + "_vecteur_"+ str(int(frame+debut))+".png"
        paths_vector.append(path)    
        cv.imwrite(f'cinema_teach/static/cinema_teach/cache/{nom_fichier + "_vecteur_"+ str(int(frame+debut))}.png',image)
    return paths_vector
   


#Cette fonction permet de remplir dans le tableau des données. En l'occurenc on ajoute le spositions des CIR (en pixels). Il faudra surement changer cette échelle par la suite.
def fill_table_solide(tab_donnees):
     #Remplissage du tableau
        data = []
        
        list_vitesses=video_vitesses(tab_donnees)
        
        vect_perpendiculaires=cal_perpendiculaires(list_vitesses)
        video_CIR=calcul_video_CIR(vect_perpendiculaires)
        n = len(video_CIR)
        
        for i in range(n):
            item = {
                "image": i+1,
                "cir_x": round(video_CIR[i][0], 2),
                "cir_y": round(video_CIR[i][1], 2),
            }
            data.append(item)
        
        res = {
            "total": len(data),
            "totalNotFiltered": len(data),
            "rows": data
        }

        json_data = res

        return json_data
    
            
   





