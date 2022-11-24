# Tobias Lepoutre (20177637)
# Largo Mas (20175474)
# Aghiles Battou (20190397)

# 2 Mai 2021


## Ce programme web permet de jouer au jeu "La somme des symboles". 
## Il s'agit d'un jeu à un jour qui nécessite un imput pour chaque devinette.
## Le but étant de deviner la valeur de chaque symbole grâce à la somme totale
## affichée à l'extrêmité de chaque ligne et chaque colonne.
## REMARQUE: on considere que le joueur ne clique jamais sur ANNULER
## lorsqu'on lui demande d'entrer l'input.

import random

tab=[[1,"circle",0],[2,"pyramide",0],[3,"penta",0],[4,"star",0],[5,"cube",0]]
grille=[]

# Créer la grille de jeu avec la position de chaque symbole dans grille et 
# la valeur de chacun de ces symboles dans tab.

def creerGrille():
    grille.clear()
    for _ in range(0,25):   # Pour chaque case du tableau: 
        tmp=int(random.random()*5)+1   # Déterminer aléatoirement
        grille.append(tmp)             # quel symbole afficher
    # S'il n'y a pas 5 symboles différents 
    if (1 or 2 or 3 or 4 or 5) not in grille:
        creerGrille()
    
    calc=0
    while calc<5:    # Déterminer pour chaque type de symbole:         
        tmp=int(random.random()*20)+1  # sa valeur
        valid=True
        for i in range(5):       # Vérifier qu'un autre symbole
            if tmp==tab[i][2]:   # n'ait pas la même valeur
                valid=False
        if valid==True:       # Sinon:
            tab[calc][2]=tmp     # Ajouter la valeur dans tab
            calc+=1 


# Raccourcis pour accéder au contenu de l'elementID dans le code HTML. 

def elem(elementID):
    return document.querySelector("#" + elementID)


# Modifie le code HTML pour afficher la valeur val sur les symboles symb.

def afficheValue(symb,val):
    for i in range (0,25):  # Pour chaque case du tableau:
        if tab[grille[i]-1][1]==symb:   # S'il s'agit du symbole symb:
            tmp = "case" + str(i+1)
            elem(tmp).innerHTML = str(val)   # Afficher val


# Applique les changements aux sommes totales des colonnes/lignes, 
# différentié par caseID, contenant le symbole deviné et enregistre 
# les changements grâce aux variables: var, tabNum, win, lose.

def changerSommes(caseID,symbole):
    global  var, tabNum, win, somme
    for i in range(0,5):  # Dans chaque ligne/colonne:
        somme=0
        for cell in range(0,5):   # Pour chaque cellule:

            if caseID=="caseLigne":   # S'il s'agit d'une ligne:
                cellNum=i * 5 + cell + 1
            else:                     # Sinon(colonne):
                cellNum=i + 1 + cell * 5

            case="case" + str(cellNum)
            tmp=elem(case).innerHTML
            if tab[grille[cellNum-1]-1][1]==symbole:  # Si symbole deviné:
                somme += int(tmp)    # Calculer la somme à soustraire

                var=int(tmp)               # Valeur soustraite
                tabNum=grille[cellNum-1]-1 # Index du symbole dans tab
        # Case de la valeur totale de i(ligne/colonne):
        case=caseID + str(i+1)
        tmp=elem(case).innerHTML
        somme= int(tmp) - somme      # Soustraire la somme au total
        elem(case).innerHTML=str(somme)  # Afficher le nouveau total
        # Vérifier si la somme totale implique qu'il n'a pas gagné
        if somme!=0:
            win=False


# Vérifie et annonce si le joueur a gagné, perdu ou si il doit continuer 
# de jouer après avoir cliqué sur le symbole deviné, donné en paramètre.

def verification(symbole):
    global win
    win=True
    lose=False
    changerSommes("caseLigne",symbole)
    changerSommes("caseCol",symbole)
    tab[tabNum][2]-=var  # Mettre à jour la valeur du symbole
    if somme!=0:  # Si la somme totale implique qu'il n'a pas gagné
        win=False
    if tab[tabNum][2]<0:  # Si la valeur entrée est en exces:
        lose=True
    # Afficher l'état du jeu
    if lose==True:
        elem("message").innerHTML = 'VOUS AVEZ PERDU...'
    if win==True:
        elem("message").innerHTML = 'VOUS AVEZ GAGNÉ!!!'

  
# On réinitialise le jeu si le joueur le demande, sinon on demande la
# valeur du symbole cliqué et on applique les changements en conséquence
# tant que le jeu n'est pas fini.

def clic(case):
    if case == 100: # Si on clic sur le bouton "Nouvelle Partie"
        init()
    # Si le jeu n'est pas fini:
    if elem("message").innerHTML=="JOUER!" and case!=100:
        a=input("Veuillez saisir un entier compris entre 1 et 20")
        # Vérifier qu'il s'agit d'un entier entre 1 et 20
        while not a.isdecimal() or int(a) <= 0 or int(a) > 20:
            a=input(
            'SAISIE INCORRECTE...\n'+\
            'Veuillez saisir un entier compris entre 1 et 20')
        # Changements à faire sur l'HTML
        symbole= tab[grille[int(case)-1]-1][1]
        afficheValue(symbole,a)
        verification(symbole)


# Sous-fonction de init() qui calcul, dans une boucle, la somme totale
# initiale pour chaque type, ligne ou colonne.

def sommeInit(type,nb):
    total=0
    if type=="ligne":  # Si c'est une ligne:
        var=nb*5
        for i in range(0,5):  # Pour chaque cellule:
            total+=tab[grille[i+var]-1][2]
    else:              # Sinon:
        var=nb
        for i in range(0,5):
            total+=tab[grille[var]-1][2]
            var+=5
    return total


# Fonction principale du jeu qui initialise le code HTML en fonction 
# des variables tab et grille défini aléatoirement par creerGrille().

def init():
    creerGrille()  # Création aléatoire des paramètres de jeu
    # Écriture du code HTML dans #main:
    main = document.querySelector("#main")
    # CSS pour l'affichage de la grille de jeu
    page =  """
    <style>
        #jeu table { float: none; }
        #jeu table td {
            border: 1px solid black; 
            padding: 1px 2px;
            width: 80px;
            height: 80px;
            font-family: Helvetica; 
            font-size: 20px; 
            text-align: center;
        }
        #jeu table td img {
            display: block;
            margin-left: auto;
            margin-right: auto;
            object-fit: contain;
            width: 80%;
            height: 80%;
        }
		.overlay-image {
			position: relative;
			width: 100%;
		}
   		.container {
			position: relative;
			text-align: center;
			color: black;
            font-size: 16px;
            font-weight: bold;
		}
        .centered {
			position: absolute;
			top: 50%;
			left: 50%;
			transform: translate(-50%, -50%);
		}
    </style><body>"""
    # Boutton "Nouvelle Partie"
    page += '<br> <td id="case100"> <button onclick=clic(100)>\
    Nouvelle partie</button> </td> </br>'
    # CSS du #message d'état de jeu
    page += '<div id="message" style="color:red; font-size:35px;\
    font-weight:bold; text-indent:1em;">JOUER!</div>'
    # HTML pour l'affichage de la grille de jeu
    page += '<table><div id="jeu">'
    for i in range (0,5):
        page += '<tr>'
        for j in range (0,5):
            case = (j+1) + i * 5
            icon= tab[grille[case-1]-1][1]
            page += '<td><div class="container">\
            <img src="symboles/'+icon+'.svg" onclick=clic('+str(case)+')\
            style="width:100%;">\
            <div class="centered" id="case'+str(case)+'"></div>\
            </div></td>' 
        total=sommeInit("ligne",i)      
        page += '<td id="caseLigne' + str(i+1) + '">' + str(total) + '</td>'
        page += '</tr>'
    for i in range (0,5):
        total=sommeInit("colonne",i)
        page += '<td id="caseCol' + str(i+1) + '">' + str(total) +  '</td>'
    page += '</tr>' 
    page += '</div></table>'
    # Code HTML complet envoyé dans #main
    main.innerHTML = page 