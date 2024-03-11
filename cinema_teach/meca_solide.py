import numpy as np

def calculate_vitesses(frame,tab_donnes):
    list_vitesses=[]
    linked_paquets=assign_paquets(frame,tab_donnes)
    for i in range(len(linked_paquets)):#attention range of frame
        t1=tab_donnes[frame][1]
        t2=tab_donnes[frame+1][1]
        vx= np.abs(tab_donnes[frame][0][linked_paquets[0]][0]-tab_donnes[frame+1][0][linked_paquets[1]][0])/np.abs(t2-t1)
        vy= np.abs(tab_donnes[frame][0][linked_paquets[0]][1]-tab_donnes[frame+1][0][linked_paquets[1]][1])/np.abs(t2-t1)

        list_vitesses.append([[vx,vy],[tab_donnes[frame+1][linked_paquets[1]][0],tab_donnes[frame+1][linked_paquets[1]][1]]])
    return list_vitesses #[[(vx,vy),(x2,y2)],...]

def assign_paquets(frame,tab_donnes):
    
    distance_min=[]
    for i in range(len(tab_donnes[frame])):
        distance_glob=[]
        for j in range(len(tab_donnes[frame])):
            distance_glob.append(np.sqrt((tab_donnes[frame][0][i][0] - tab_donnes[frame+1][0][j][0])**2 + (tab_donnes[frame][0][i][1] - tab_donnes[frame+1][0][j][1])**2))
        distance_min.append([i,np.argmin(distance_glob)])
    return distance_min #[[paquetx im1,paquetx im2],...]

def video_vitesses(tab_donnes):
    video_vitesses=[]
    for frame in range(len(tab_donnes)-1):
        list_vitesses=calculate_vitesses(frame,tab_donnes)
        video_vitesses.append(list_vitesses)