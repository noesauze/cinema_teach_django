import numpy as np

from scipy.optimize import minimize
import matplotlib as plt
import cv2 as cv



def assign_paquets(frame,tab_donnes):
    
    distance_min=[]
    
    for i in range(len(tab_donnes[frame])):
        
        distance_glob=[]
        for j in range(len(tab_donnes[frame+1])):
            
            distance_glob.append(np.sqrt((tab_donnes[frame][0][i][0][0] - tab_donnes[frame+1][0][j][0][0])**2 + (tab_donnes[frame][0][i][0][1] - tab_donnes[frame+1][0][j][0][1])**2))
            
        distance_min.append([i,np.argmin(distance_glob)])
    return distance_min #[[paquetx im1,paquetx im2],...]


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


def video_vitesses(tab_donnes):
    video_vitesses=[]
    for frame in range(len(tab_donnes)-1):
        list_vitesses=calculate_vitesses(frame,tab_donnes)
        video_vitesses.append(list_vitesses)
    return video_vitesses

#On définit les vecteurs perpendiculaires à tous les vecteurs vitesse des centroides
def cal_perpendiculaires(list_centroids):
    n=len(list_centroids)
    for k in range(n):
        vect_perpendiculaire=list_centroids
        vect_perpendiculaire[k][0][0][0],vect_perpendiculaire[k][0][0][1]=-vect_perpendiculaire[k][0][0][1],vect_perpendiculaire[k][0][0][0]
        vect_perpendiculaire[k][1][0][0],vect_perpendiculaire[k][1][0][1]=-vect_perpendiculaire[k][1][0][1],vect_perpendiculaire[k][1][0][0]
    return vect_perpendiculaire

'''''
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


def Param_Droites(list_perpendiculaires, frame):
    
    params=[]
    for i in range(len(list_perpendiculaires[0])):
        
        
        a=list_perpendiculaires[frame][i][0][1]/list_perpendiculaires[frame][i][0][0] #Vy/Vx pour la perpendiculaire
        b=-(list_perpendiculaires[frame][i][0][1]/list_perpendiculaires[frame][i][0][0])*list_perpendiculaires[frame][i][1][0]+list_perpendiculaires[frame][i][1][1] #-Vy/Vx*x1+y1
        
        params.append([a,b])
    
        
    return  params

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


def CIR(params):
    # Point initial
    initial_point = [0, 0]

    # Minimisation de la distance
    result = minimize(distance_to_lines, initial_point,args=(params,), method='Nelder-Mead')
    closest_point = result.x


    return closest_point


def calcul_video_CIR(vect_perpendiculaire):
    video_CIR=[]
    for frame in range(len(vect_perpendiculaire)):
        params=Param_Droites(vect_perpendiculaire, frame)
        closest_point=CIR(params)
        video_CIR.append(closest_point)
    return video_CIR





def affichage_vector(paths_centre,tab_donnes,nb_labels,nom_fichier,debut):
    
    paths_vector=[]
    path_prem_image="/static/cinema_teach/cache/"+nom_fichier + "_centre_"+ str(int(debut))+".png"
    paths_vector.append(path_prem_image)
    for frame in range(1,len(paths_centre)):
        nom2 = "cinema_teach/static/cinema_teach/cache/"+ nom_fichier + "_centre_"+ str(int(frame+debut))+".png"

        image=cv.imread(nom2)
        
        for i in range(nb_labels):
            
            
            
            
            list_vitesses=calculate_vitesses(frame-1,tab_donnes)
            
            x=0.08
            start=[int(list_vitesses[i][1][0]),int(list_vitesses[i][1][1])]
            vector=[int(list_vitesses[i][0][0]*x),int(list_vitesses[i][0][1]*x)]
            
           
            
            end_point = [start[0] + vector[0], start[1] + vector[1]]
            image=cv.arrowedLine(image, start, end_point, (0, 0, 255), thickness=2)
            
        path="/static/cinema_teach/cache/"+nom_fichier + "_vecteur_"+ str(int(frame+debut))+".png"
        paths_vector.append(path)    
        cv.imwrite(f'cinema_teach/static/cinema_teach/cache/{nom_fichier + "_vecteur_"+ str(int(frame+debut))}.png',image)
    return paths_vector
   



        
    
            
   





