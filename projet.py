import fonctions as f
import projet1_final as p
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

import sys



    # Exit

def sortir(message='Exit'):
    print("\n\n\n____________________________________________________________________________________")
    print("\n                            Le programme a été intérompu                            ")
    print("                     Cause : "+message+"")
    print("____________________________________________________________________________________\n\n\n")
    return sys.exit()


    # Fonction pour vérifier la date

def bonne_date(date,endroit):
    date=p.completer_date(date,10)
    annee,mois,jour,tiret1,tiret2=date[:4],date[5:7],date[8:10],date[4],date[7]
    while type(date)!=str or len(date)!=10 or int(annee)!=2019 or int(mois)!=8 or int(jour)>21 or int(jour)<11 or tiret1!='-' or tiret2!='-':
        print("La date de "+endroit+" n'est pas sous la bonne forme, est incomplète ou n'est pas comprise dans la bonne plage")
        date=input("Veuillez la réécrire sous la forme 'aaaa-mm-jj'' et entre '2019-08-11' et '2019-08-25' : ")
        date=p.completer_date(date,10)
        annee,mois,jour,tiret1,tiret2=date[:4],date[5:7],date[8:10],date[4],date[7]
        if date=='sortir':
            sortir()
    return date



#____________________________________________________________



# Ecrire sous la forme : python MONSCRIPT.py <action> <var> <start_date> <end_date>

print("Ce script permet d'effectuer une action pour une variable en fonction du temps sur la plage voulue \n(sans les dates précisées, la plage sera automatiquement prise entre le '2019-08-11' et le '2019-08-25')\n")
print("Pour cela, veuillez écrire sous la forme : \n   python projet.py <action> <variable> <date de début> <date de fin>")
print("En cas de bug, pour quitter le programme, tapez 'sortir'\n")




#_______________________________________________________________________________


# Définition de l'action

try:
    action=sys.argv[1]
except Exception:
    sortir("Il manque une action")


    # On défini la liste d'action qui existe (Ainsi, on poura en rajouter ou en enlever)

ACT=['Display','DisplayStat','Corrélation']

DIS=['Display','display','courbe']
STAT=['DisplayStat','displaystat','Displaystat','displayStat','Stat','stat']
CORR=['Corrélation','corrélation','Correlation','correlation','corr']

ACT_repetition=[DIS,STAT,CORR]

S=''
n=len(ACT)
for k in range(n):
    if k<n-1:
        S=S+ACT[k]+' | ' 
    else:
        S+=ACT[k]

    
    # On ragarde si l'action existe

act_test=None
for L in ACT_repetition:
    if action in L:
        action=L[0]
        act_test=action
while act_test==None:
    for L in ACT_repetition:
        if action in L:
            action=L[0]
            act_test=action
    action=input("Cette action n'existe pas.\nVeuillez la réecrire (ou tapez 'action' pour voir la liste des actions) : ")
    if action=='action':
        action=input("Veuillez choisir entre les variables : "+S+" : ")
    if action=='sortir':
        sortir()


    # A présent, l'action est bien défini
    

#_______________________________________________________________________________


    # Vérifions qu'on a pas trop d'argument

if action!='Corrélation':
    if len(sys.argv)>5:
        sortir("Trop d'arguments (seulement 4 sont attendus)")
else:
    if len(sys.argv)>6:
        sortir("Trop d'arguments (seulement 5 sont attendus)")


#_______________________________________________________________________________


# Définition de la ou des variable(s)


    # On défini la liste de variable qui existe (Ainsi, on poura en rajouter ou en enlever)
    
VAR=['Carbone','Température','Luminosité','Bruit','Humidité','Humidex']

CA=['Carbone','carbone','co2','CO2']
TEMP=['Température','Temperature','temperature','temp']
LUM=['Luminosité','luminosité','luminosite','Luminosite','lum']
BRUIT=['Bruit','bruit','noise']
HUM=['Humidité','humidité','Humidite','humidite','hum']
Hum=['Humidex','humidex']

VAR_repetition=[CA,TEMP,LUM,BRUIT,HUM,Hum]


    # On prépare le message à afficher
S=''
n=len(VAR)
for k in range(n):
    if k<n-1:
        S=S+VAR[k]+' | ' 
    else:
        S+=VAR[k]



#____________On_défini_une_fonction_pour_prendre_les_variables__________________


def def_var(var):
    
        # On ragarde si la variable existe
    var_test=None
    for L in VAR_repetition:
        if var in L:
            var=L[0]
            var_test=var
    while var_test==None:
        var=input("Cette variable : "+var+", n'existe pas.\nVeuillez la réecrire (ou tapez 'variable' pour voir la liste des variables) : ")
        if var=='variable':
            var=input("Veuillez choisir entre les variables : "+S+" : ")
        if var=='sortir':
            sortir()
        for L in VAR_repetition:
            if var in L:
                var=L[0]
                var_test=var
    return var

#_______________________________________________________________________________


    # Si l'action est display ou displayStat, on ne demande qu'une seule variable
    # On s'assure qu'il y a une variable

if action!='Corrélation':
    try:
        var=sys.argv[2]
    except Exception:
        sortir("Il manque une variable")
    var=def_var(var)
    k=3                         # k est l'indice de la prochaine variable à entrer dans le cmd

    # Sinon, il faut qu'il y ait deux variables
else:
    try:
        var1=sys.argv[2]
    except Exception:
        sortir("Il manque un couple de variable")
    var1=def_var(var1)
    try:
        var2=sys.argv[3]
    except Exception:
        sortir("Il manque la seconde variable")
    var2=def_var(var2)
    k=4
    
    
    # On vérifie que les deux variables ne sont pas les mêmes
    while var1==var2:
        print("\nProblème : Les deux variables sont les mêmes. Veuillez redéfinir le couple de variables")
        choix=input("Pour redéfinir la première variable, tapez 1 | Pour la seconde, tapez 2 | Pour changer les deux, tapez 3 : ")
        if choix=='1':
            var1=input("Veuillez réécrire la première variable. La seconde variable étant "+var2+" : ")
            var1=def_var(var1)
        elif choix=='2':
            var2=input("Veuillez réécrire la seconde variable. La première variable étant "+var1+" : ")
            var2=def_var(var2)
        elif choix=='3':
            var1=input("Veuillez réécrire la première variable : ")
            var2=input("Veuillez réécrire la seconde variable. La première variable étant "+var1+" : ")
        elif choix=='sortir':
            sortir()
        else:
            print(" \nCe choix : "+choix+", n'existe pas. Pour quitter, tapez sortir\n ")


    # A présent, la ou les variables sont bien définies
    


#_______________________________________________________________________________


# Définition de la date de départ

try:
    start_date=sys.argv[k]
    start_date=bonne_date(start_date,'début')
except Exception:
    start_date='2019-08-11'



#_______________________________________________________________________________


# Définition de la date de fin

try:
    end_date=sys.argv[k+1]
    end_date=bonne_date(end_date,'fin')
except Exception:
    end_date='2019-08-25'





#_______________________________________________________________________________


# Ici on a les deux dates, ils faut vérifier que la première soit plus petite que la seconde

while start_date[8:10]>end_date[8:10]:
    print("Problème : La date de départ est plus grande que la date de fin. Veuillez redéfinir les dates")
    choix=input("Pour redéfinir la première date, tapez 1 | Pour la seconde, tapez 2 | Pour changer les deux, tapez 3 | Pour inverser les deux dates, tapez 4 | Pour utiliser les dates par défaux, tapez 5 : ")
    if choix=='1':
        start_date=input("Veuillez réécrire la date de début. La date de fin étant "+end_date+" : ")
        start_date=bonne_date(start_date,'début')
    elif choix=='2':
        end_date=input("Veuillez réécrire la date de fin. La date de début étant "+start_date+" : ")
        end_date=bonne_date(end_date,'fin')
    elif choix=='3':
        start_date=input("Veuillez réécrire la date de début : ")
        start_date=bonne_date(start_date,'début')
        end_date=input("Veuillez réécrire la date de fin. La date de début est "+start_date+" : ")
        end_date=bonne_date(end_date,'fin')
    elif choix=='4':
        start_date,end_date=end_date,start_date
    elif choix=='5':
        start_date,end_date='2019-08-11','2019-08-25'
    elif choix=='sortir':
        sortir()
    else:
        print(" \nCe choix : "+choix+", n'existe pas. Pour quitter, tapez sortir\n ")


# A présent les dates sont aux bon format et dans l'ordre


#_______________________________________________________________________________


    # Récapitulons : On a l'action, la ou les variable(s) et la borne de temps
    
    
k=0                             # k permet de garder en mémoire l'action qu'on a
if action=='Display':
    k=1
    print("\nBut : Afficher l'évolution de "+var)
elif action=='DisplayStat':
    k=2
    print("\nBut : Afficher la courbe de "+var+" avec des valeurs statistiques")
else:
    k=3
    print("\nBut : Calculer la corrélation entre "+var1+" et "+var2)
print("entre le "+start_date+" et le "+end_date+"\n")  


entrer=input("Tapez 1, pour voir les anomalies\nSinon, press 'entrer' pour continuer\n     ")      
    # Ceci permet d'afficher les messages avant de charger les courbes
if entrer=='sortir':
    sortir()



if k==1:        # Ici, on affiche une courbe
    if entrer!='1':         # Sans les anomalies
        if var=='Carbone':
            p.Afficher_carbone(start_date,end_date)
        elif var=='Température':
            p.Afficher_temperature(start_date,end_date)
        elif var=='Luminosité':
            p.Afficher_luminosite(start_date,end_date)
        elif var=='Bruit':
            p.Afficher_bruit(start_date,end_date)
        elif var=='Humidité':
            p.Afficher_humidite(start_date,end_date)
        elif var=='Humidex':
            temp=p.donnee.temp.tolist()
            hum=p.donnee.humidity.tolist()
            humidex=p.humidex(temp,hum,start_date,end_date)
            p.Afficher_humidex(humidex,start_date,end_date)
    else:               # Affichage des courbes avec anomalies
        p.Afficher_colonne_avec_anomalie_n(var,start_date,end_date)
    
elif k==2:        # Ici, on affiche une courbe avec les valeurs statistiques : min, max, écart-type, moyenne, variance, médiane
    p.Afficher_stat(var,start_date,end_date,entrer=='1')
    
    
elif k==3:       # Ici, on affiche une courbe avec les deux variables avec leur indice de corrélation
    # On récupère la colonne de la variable
    col1=p.recup(var1)
    col2=p.recup(var2)
        
    corr=f.correlation(col1,col2)

    print("\nL'indice de corrélation entre "+var1+" et "+var2+" sur toute la période vaut :\n          "+str(corr))
    p.Afficher_correlation(var1,var2,start_date,end_date,entrer=='1')



    # Lorsque le script se termine, il est important de l'indiquer


print("\n\n\n____________________________________________________________________________________")
print("\n                                          FIN                                          ")
print("____________________________________________________________________________________\n\n\n")



























