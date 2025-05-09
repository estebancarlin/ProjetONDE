from numpy import *
import numpy as np
from random import *
from matplotlib.pyplot import *
import matplotlib.pyplot as plt
import os


### On étudie la cicatrisation d'une plaie

### On utilise une matrice avec des valeurs numériques pour chaque coefficient

### Correspondance état de la peau / couleur
### PEAU INTACTE = -1
### PEAU BLESSEE = 0
### PEAU EN CICATRISATION = 1
### PEAU CICATRISEE = 2



####################### FONCTIONS PRÉLIMINAIRES ######################



"Créer une peau vierge (intacte)"
def peau_vierge (n):
    M = np.zeros((n+2,n+2),int)
    for i in range (n + 2) : 
        for j in range (n + 2) : 
            M[i,j] = -1
    return M


"Créer une plaie 'sur' la peau intacte"
def zone_blessee (n) : 
    M = peau_vierge (n)
    n = len(M)
    for i in range ( int(n/4) , int((3*n)/4) ) : 
        for j in range (  int(n/4) , int((3*n)/4)) : 
            M[i,j] = 0                                    # On a décidé arbitrairement de prendre une zone carrée centrée dans la matrice M
    for i in range ( int(n/4) , int((3*n)/4)  ) :         # On apporte aléatoirement des modifications locales pour plus de réalisme
        r = uniform(0,1)
        if r >= 0.25 : 
            M[i,int(n/4)] = -1                            # 1ère 'couche' de cellules blessées, les plus proches de la peau intacte
        r = uniform(0,1)
        if r >= 0.25 : 
            M[i,int((3*n)/4)-1] = -1
        r = uniform(0,1)
        if r >= 0.5 :                                     # 2ème couche, moins intacte que la 1ère car plus proche du centre de la plaie
            M[i,int((n)/4)+1] = -1
        r = uniform(0,1)
        if r >= 0.5 : 
            M[i,int((3*n)/4)-2] = -1
        r = uniform(0,1)
        if r >= 0.75 : 
            M[i,int((n)/4)+2] = -1                        # 3ème couche, moins intacte que la 2ème car plus proche du centre de la plaie
        r = uniform(0,1)
        if r >= 0.75 : 
            M[i,int((3*n)/4)-3] = -1
    for j in range ( int(n/4) , int((3*n)/4)  ) :         # Suite des modifications aléatoires
        r = uniform(0,1)
        if r >= 0.25 : 
            M[int(n/4), j] = -1
        r = uniform(0,1)
        if r >= 0.25 : 
            M[int((3*n)/4)-1, j] = -1
        r = uniform(0,1)
        if r >= 0.5 : 
            M[int((n)/4)+1, j] = -1
        r = uniform(0,1)
        if r >= 0.5 : 
            M[int((3*n)/4)-2, j] = -1
        r = uniform(0,1)
        if r >= 0.75 : 
            M[int((n)/4)+2, j] = -1
        r = uniform(0,1)
        if r >= 0.75 : 
            M[int((3*n)/4)-3, j] = -1
    
    return M


"Créer la 1ère couche de cicatrisation pour lancer le reste du processus, cette couche est aussi aléatoire"
def zone_cicatrisant (n) :
    M = zone_blessee (n)
    n = len(M)
    liste_peau_cicatrisee = []
    liste_peau_en_cicatrisation = []
    for i in range ( int(n/4) , int((3*n)/4) ) : 
        for j in range (  int(n/4) , int((3*n)/4)) :                # Seules les cellules blessées peuvent commencer à cicatriser, les intactes ne le peuvent pas
            if M[i-1,j] == -1 :                 
                if M[i,j-1] == -1 :                                 # Les cellules sur les bords ou proches de bords cicatriseront plus vite car localement 
                    if M[i,j] == 0 :                                # elles bénéficient d'un meilleur apport de nutrients et autres molécules
                      M[i,j] = 1                                    # Plus on est loin des bords plus il est compliqué d'être en état de cicatrisation tôt
                      liste_peau_en_cicatrisation.append([i,j])
                elif M[i,j+1] == -1 :
                    if M[i,j] == 0 : 
                      M[i,j] = 1
                      liste_peau_en_cicatrisation.append([i,j])
                else : 
                    r = uniform(0,1)
                    if r >= 0.33 : 
                        if M[i,j] == 0 : 
                          M[i,j] = 1
                          liste_peau_en_cicatrisation.append([i,j])
            if M[i+1,j] == -1 :
                if M[i,j-1] == -1 : 
                    if M[i,j] == 0 : 
                      M[i,j] = 1
                      liste_peau_en_cicatrisation.append([i,j])
                elif M[i,j+1] == -1 : 
                    if M[i,j] == 0 : 
                      M[i,j] = 1
                      liste_peau_en_cicatrisation.append([i,j])
                else : 
                    r = uniform(0,1)
                    if r >= 0.33 : 
                      if M[i,j] == 0 : 
                        M[i,j] = 1
                        liste_peau_en_cicatrisation.append([i,j])
            if M[i,j-1] == -1 :
                r = uniform(0,1)
                if r >= 0.33 :
                  if M[i,j] == 0 :  
                    M[i,j] = 1
                    liste_peau_en_cicatrisation.append([i,j])
            if M[i,j+1] == -1 :
                r = uniform(0,1)
                if r >= 0.33 : 
                  if M[i,j] == 0 : 
                    M[i,j] = 1
                    liste_peau_en_cicatrisation.append([i,j])  
            if M[i-2,j] == -1 :
                if M[i,j-2] == -1 : 
                    r = uniform(0,1)
                    if r >= 0.5 : 
                      if M[i,j] == 0 : 
                        M[i,j] = 1
                        liste_peau_en_cicatrisation.append([i,j])
                elif M[i,j+2] == -1 : 
                    r = uniform(0,1)
                    if r >= 0.5 : 
                      if M[i,j] == 0 : 
                        M[i,j] = 1
                        liste_peau_en_cicatrisation.append([i,j])
                else : 
                    r = uniform(0,1)
                    if r >= 0.5 : 
                      if M[i,j] == 0 : 
                        M[i,j] = 1
                        liste_peau_en_cicatrisation.append([i,j])
            if M[i+2,j] == -1 :
                if M[i,j-2] == -1 : 
                    r = uniform(0,1)
                    if r >= 0.33 : 
                      if M[i,j] == 0 : 
                        M[i,j] = 1
                        liste_peau_en_cicatrisation.append([i,j])
                elif M[i,j+2] == -1 : 
                    r = uniform(0,1)
                    if r >= 0.33 : 
                      if M[i,j] == 0 : 
                        M[i,j] = 1
                        liste_peau_en_cicatrisation.append([i,j])
                else : 
                    r = uniform(0,1)
                    if r >= 0.5 : 
                      if M[i,j] == 0 : 
                        M[i,j] = 1
                        liste_peau_en_cicatrisation.append([i,j])
            if M[i,j-2] == -1 :
                r = uniform(0,1)
                if r >= 0.5 :
                  if M[i,j] == 0 :  
                    M[i,j] = 1
                    liste_peau_en_cicatrisation.append([i,j])
            if M[i,j+2] == -1 :                                    # On est allés jusqu'à la 3ème couche après la frontière avec la peau intacte
                r = uniform(0,1)
                if r >= 0.5 : 
                  if M[i,j] == 0 : 
                    M[i,j] = 1
                    liste_peau_en_cicatrisation.append([i,j])

    return ( M, liste_peau_en_cicatrisation, liste_peau_cicatrisee)


"Renvoie la liste des cellules voisines"
def voisins (coord):                  
    X,Y = coord[0], coord[1]
    return ( [[X-1, Y-1], [X-1,Y], [X-1,Y+1], [X,Y-1], [X,Y+1], [X+1,Y-1], [X+1,Y], [X+1,Y+1]] )




############################## FONCTIONS POUR LA CICATRISATION ######################


def décompte_cellules_contours (M, coord) :
    n = len(M)
    assert n > 5
    
    i,j = coord[0], coord[1]
    contour_A = []
    contour_B = []
    
    colonne_A_g, colonne_A_d = [[i-1,j-1], [i,j-1], [i+1, j-1]], [[i-1,j+1], [i,j+1], [i+1, j+1]]
    colonne_A_g_, colonne_A_d_ = [[i,j-1]], [[i,j+1]]
    ligne_A_b, ligne_A_h = [ [i+1,j-1],[i+1,j],[i+1,j+1] ], [ [i-1,j-1],[i-1,j],[i-1,j+1] ]
    ligne_A_b_, ligne_A_h_ = [[i+1,j]], [[i-1,j]]

    colonne_B_g, colonne_B_d = [ [i-2,j-2],[i-1,j-2],[i,j-2],[i+1,j-2],[i+2,j-2] ], [ [i-2,j+2], [i-1,j+2],[i,j+2],[i+1,j+2],[i+2,j+2] ]
    colonne_B_g_, colonne_B_d_ = [ [i-1,j-2],[i,j-2],[i+1,j-2] ], [ [i-1,j+2],[i,j+2],[i+1,j+2] ]

    ligne_B_b, ligne_B_h = [ [i+2,j-2],[i+2,j-1], [i+2,j], [i+2,j+1],[i+2,j+2] ], [ [i-2,j-2],[i-2,j-1], [i-2,j], [i-2,j+1],[i-2,j+2] ]     
    ligne_B_b_, ligne_B_h_ = [[i+2,j-1], [i+2,j], [i+2,j+1]], [[i-2,j-1], [i-2,j], [i-2,j+1]] 


# #---------------- contour_A ------------
    if i > 1 and i < n-2 and j > 1 and j < n-2 :
        contour_A += colonne_A_d + colonne_A_g + ligne_A_b_ + ligne_A_h_
    

    if i == 1 and j == 1 :
        contour_A += ligne_A_b_ + colonne_A_d_ + [[i+1,j+1]]
    if i == 1 and j == n-2 :
        contour_A += ligne_A_b_ + colonne_A_g_ + [[i+1,j-1]]
    if i == 1 and j > 1 and j < n-2 :
        contour_A += ligne_A_b + colonne_A_d_ + colonne_A_g_
        
        
    if i == n-2 and j == 1 :
        contour_A += ligne_A_h_ + colonne_A_d_ + [[i-1,j+1]]
    if i == n-2 and j == n-2 :
          contour_A += ligne_A_h_ + colonne_A_g_ + [[i-1,j-1]]
    if i == n-2 and j > 1 and j < n-2 :
        contour_A += ligne_A_h + colonne_A_d_ + colonne_A_g_
        
    
    if j == 1 and i > 1 and i < n-2 :
        contour_A += ligne_A_b_ + ligne_A_h_ + colonne_A_d
        

    if j == n-2 and i > 1 and i < n-2 :
        contour_A += ligne_A_b_ + ligne_A_h_ + colonne_A_g
        

#---------------- contour_B ------------

    if i > 2 and i < n-3 and j > 2 and j < n-3 :
        contour_B += colonne_B_d + colonne_B_g + ligne_B_b_ + ligne_B_h_       
                
    if i == 1 and j == 1 :
        contour_B += [[i+2,j] , [i+2,j+1] , [i+2,j+2] , [i,j+2] , [i+1,j+2]]
    if i == 1 and j == 2 :
        contour_B += ligne_B_b_ + [[i+2,j+2] , [i+1,j+2] , [i,j+2]]
    if i == 1 and j == n-3 :
        contour_B += ligne_B_b_ + [[i,j-2] , [i+1,j-2] , [i+2,j-2]]
    if i == 1 and j == n-2 :
        contour_B += [[i,j-2] , [i+1,j-2] , [i+2,j-2] , [i+2,j-1] , [i+2,j]]
    if i == 1 and j > 2 and j < n-3 :
        contour_B += ligne_B_b + [[i,j-2] , [i+1,j-2] , [i,j+2] , [i+1,j+2]]
        
    if i == 2 and j == 1 :
        contour_B += colonne_B_d_ + [[i+2,j] , [i+2,j+1] , [i+2,j+2]]
    if i == 2 and j == 2 :
        contour_B += ligne_B_b_ + colonne_B_d_ + [[i+2,j+2]]
    if i == 2 and j == n-3 :
        contour_B += ligne_B_b_ + colonne_B_g_ + [[i+2,j-2]]
    if i == 2 and j == n-2 :
        contour_B += colonne_B_g_ +  [ [i+2,j] , [i+2,j-1] , [i+2,j-2] ]
    if i == 2 and j > 2 and j < n-3 :
         contour_B += ligne_B_b + colonne_B_d_ + colonne_B_g_
        
    if i == n-3 and j == 1 :
        contour_B += colonne_B_d_ + [ [i-2,j] , [i-2,j+1] , [i-2,j+2] ]
    if i == n-3 and j == 2 :
        contour_B += ligne_B_h_ + colonne_B_d_ + [[i-2,j+2]]
    if i == n-3 and j == n-3 :
        contour_B += ligne_B_h_ + colonne_B_g_ + [[i-2,j-2]]
    if i == n-3 and j == n-2 :
        contour_B += colonne_B_g_ + [ [i-2,j-2] , [i-2,j-1] , [i-2,j]]
    if i == n-3 and j > 2 and j < n-3 :
        contour_B += ligne_B_h + colonne_B_d_ + colonne_B_g_
        
    if i == n-2 and j == 1 :
        contour_B += [[i-2,j] , [i-2,j+1] , [i-2,j+2] , [i-1,j+2] , [i,j+2]]
    if i == n-2 and j == 2 :
        contour_B += ligne_B_h_ + [[i-2,j+2] , [i-1,j+2] , [i,j+2]]
    if i == n-2 and j == n-3 :
        contour_B += ligne_B_h_ + [ [i-2,j-2] , [i-1, j-2] , [i,j-2]]
    if i == n-2 and j == n-2 :
        contour_B += [[i,j-2] , [i-1,j-2] , [i-2,j-2] , [i-2,j-1] , [i-2,j]]
    if i == n-2 and j > 2 and j < n-3 :
        contour_B += ligne_B_h + [ [i,j-2] , [i-1,j-2] , [i-1,j+2] , [i,j+2]]
    
    
    somme_A,somme_B = 0,0
    for k in contour_A :
        if M[ k[0],k[1] ] == 1:
            somme_A += 1

    for k2 in contour_B :
        if M[ k2[0], k2[1]] == 1:
            somme_B += 1
            
    return (somme_A, somme_B)



### Fonction qui renvoit la matrice M après une étape de cicatrisation
def étape_cicatrisation (M, liste_peau_cicatrisee , liste_peau_en_cicatrisation ) :        
    (p1, p2) = (0.33, 0.33)                                                                  

    nouvelle_liste_peau_en_cicatrisation = []
    nouvelle_liste_peau_cicatrisee = []
    nouvelle_liste_peau_intacte = []
    
    décompte = 0
    somme_B = 0

    for k in liste_peau_en_cicatrisation :
        if random() < p2 :                           # Probabilité p2 que la cellule en cicatrisation devienne cicatrisée
            M [ k[0],k[1] ] = 2                            
            nouvelle_liste_peau_cicatrisee.append(k)
            
        liste_cellules_environnantes = voisins (k)
            
        for k2 in range (0,8) :                              # On étudie les cellules_environnantes de la cellule "k" étudiée
            # print('k2',k2)
            i,j = liste_cellules_environnantes [k2][0],  liste_cellules_environnantes[k2][1]

            if random() < p1 and M[i,j] == 0 and k2 not in nouvelle_liste_peau_en_cicatrisation :
                (A,B) = décompte_cellules_contours (M,k)
                M[i,j] = 1                                  # Probabilité p1 que la cellule blessée commence à cicatriser
                nouvelle_liste_peau_en_cicatrisation.append ([i,j])


### ### ### ### ### ### ### ### ### ### ### ###

# Modélisation AVEC LASER :   # On fait disparaître la peau cicatrisee pour laisser place à une régénération de la peau en peau intacte

    for k in liste_peau_cicatrisee :                        
        if random() < p2 :                          
            M [ k[0],k[1] ] = -1                             
            nouvelle_liste_peau_intacte.append(k)
            
        liste_cellules_environnantes = voisins (k)
            
        for k2 in range (0,8) :                              
            # print('k2',k2)
            i,j = liste_cellules_environnantes [k2][0],  liste_cellules_environnantes[k2][1]
            
            if random() < p1 and M[i,j] == 2 and k2 not in nouvelle_liste_peau_cicatrisee :
                (A,B) = décompte_cellules_contours (M,k)
                M[i,j] = -1                                 
                nouvelle_liste_peau_intacte.append ([i,j])
                
### ### ### ### ### ### ### ### ### ### ### ###


    for k in nouvelle_liste_peau_cicatrisee :   
        liste_peau_en_cicatrisation.remove(k)

    liste_peau_en_cicatrisation += nouvelle_liste_peau_en_cicatrisation
    liste_peau_cicatrisee += nouvelle_liste_peau_cicatrisee


    return (M, liste_peau_en_cicatrisation, liste_peau_cicatrisee, [somme_B, décompte])




### Fonction qui renvoit l'état de la peau après 'Nb_étapes' étapes.

def simulation_centre (n, Nb_étapes ):
    
    (M, liste_peau_en_cicatrisation , liste_peau_cicatrisee) = zone_cicatrisant (n) 
    for k in range (Nb_étapes):
        (M, liste_peau_en_cicatrisation, liste_peau_cicatrisee, D) = étape_cicatrisation (M, liste_peau_en_cicatrisation, liste_peau_cicatrisee )

    # Réglage des couleurs d'affichage en fonction de l'état des cellules
    if Nb_étapes == 0 or Nb_étapes == 1:
        cmap = matplotlib.colors.ListedColormap(['navajowhite', 'tomato', 'lightsalmon'])
    else:
        cmap = matplotlib.colors.ListedColormap(['navajowhite', 'tomato', 'lightsalmon', 'antiquewhite'])
    
    imshow(M, cmap=cmap)
    gca().get_xaxis().set_visible(False)
    gca().get_yaxis().set_visible(False)
    show ()
    
    return (M, liste_peau_en_cicatrisation , liste_peau_cicatrisee )



############################## ENREGISTREMENT DES IMAGES  ######################

"pas, le nombre d'étapes séparant deux clichés de la simulation"
"P est le nombre de ligne lors de l'affichage et Nb_fenêtres = P**2"
def affichage_subplot(p, taille_peau, Nb_étapes):

    if Nb_étapes > p**2 :
        pas = Nb_étapes//(p**2)
        Nb_clichés = p**2
    else :
        pas = 1
        Nb_clichés = Nb_étapes


    étape = "Étape 1"
    title(étape)
    (M, liste_peau_en_cicatrisation , liste_peau_cicatrisee ) = simulation_centre (taille_peau, 0)

    my_path = os.path.abspath('/Users/pepouille/Desktop/ProjetONDES')
    my_file = 'Étape 1.jpeg'
    savefig(os.path.join(my_path, my_file))

    for k in range (1,Nb_clichés):

        for k2 in range (pas):
            (M, liste_peau_en_cicatrisation, liste_peau_cicatrisee ) = étape_cicatrisation (M, liste_peau_en_cicatrisation, liste_peau_cicatrisee) 


        "Réglage des couleurs d'affichage en fonction de l'état de chaque cellule ."
        if len(liste_peau_cicatrisee) == 0:
            cmap = matplotlib.colors.ListedColormap(['navajowhite', 'tomato', 'lightsalmon'])
        else :
            cmap = matplotlib.colors.ListedColormap(['navajowhite', 'tomato', 'lightsalmon', 'antiquewhite'])
        étape = "Étape "+str(k*pas+1)
        title (étape)
        imshow(M, cmap=cmap)

        gca().get_xaxis().set_visible(False)
        gca().get_yaxis().set_visible(False)

        my_path = os.path.abspath('/Users/pepouille/Desktop/ProjetONDES')
        my_file = étape + '.jpeg'
        savefig(os.path.join(my_path, my_file))
    return ()



def enregistrement_images (intervalle_étapes, taille_peau, Nb_étapes) :
    t1 = time.process_time()
    Nb_clichés = int(Nb_étapes/intervalle_étapes)
    print('intervalle_étapes = '+ str(intervalle_étapes) +'\n'+ 'taille_peau = '+ str(taille_peau) +'\n'+ 'Nb_étapes = '+ str(Nb_étapes))

    étape = "Étape 1"
    title(étape)
    (M, liste_peau_en_cicatrisation, liste_peau_cicatrisee ) = simulation_centre (taille_peau, 0)

    my_path = os.path.abspath('/Users/pepouille/Desktop/ProjetONDES')
    my_file = 'Étape 1.jpeg'
    savefig(os.path.join(my_path, my_file))

    for k in range (1,Nb_clichés):
        for k2 in range (intervalle_étapes):
            (M, liste_peau_en_cicatrisation, liste_peau_cicatrisee, D) = étape_cicatrisation (M, liste_peau_en_cicatrisation, liste_peau_cicatrisee )


        "Réglage des couleurs d'affichage en fonction de l'état des cellules"
        if len(liste_peau_cicatrisee) == 0:
            cmap = matplotlib.colors.ListedColormap(['navajowhite', 'tomato', 'lightsalmon'])
        else :
            cmap = matplotlib.colors.ListedColormap(['navajowhite', 'tomato', 'lightsalmon', 'antiquewhite'])


        étape = "Étape "+str(k*intervalle_étapes+1)
        title (étape)
        my_path = os.path.abspath('/Users/pepouille/Desktop/ProjetONDES')
        my_file = étape + '.jpeg'
        savefig(os.path.join(my_path, my_file))
        imshow(M, cmap=cmap)
    t2 = time.process_time()
    durée = t2 - t1
    print (durée, "s")
    # print("IMAGES NON ENREGISTRÉES")
    return ()

enregistrement_images(1, 80, 50)
