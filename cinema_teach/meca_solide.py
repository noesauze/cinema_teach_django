import numpy as np
from .meca_point import video_en_image

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
        vx= tab_donnes[frame][0][linked_paquets[i][0]][0][0]-tab_donnes[frame+1][0][linked_paquets[i][1]][0][0]/t1-t2
        vy= tab_donnes[frame][0][linked_paquets[i][0]][0][1]-tab_donnes[frame+1][0][linked_paquets[i][1]][0][1]/t1-t2
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
