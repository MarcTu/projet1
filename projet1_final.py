import fonctions as f

from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


donnee = pd.read_csv("post-32566-EIVP_KM.csv", sep=';')

temperature=donnee['temp']
hum=donnee['humidity']
carbone=donnee['co2']
lum=donnee['lum']
bruit=donnee['noise']
date=donnee['sent_at']



#_______________________________________________________________________________


# Date :


def transformer_date(date_elementaire):
    return int(date_elementaire[0:4]+date_elementaire[5:7]+date_elementaire[8:10])


def completer_date(d,max):        # n est la longueur de la liste réelle et max la lonngueur voulue
    n=len(d)
    if n<10:
        m=10-n
        X=''
        for k in range(m):
            X+='0'
        d=d+X
    return d


def new_date(date_list):
    date_new=[]
    for date in date_list:
        date_new.append(int(date[0:4]+date[5:7]+date[8:10]))
    return date_new


def new_heure(date_list):
    heure_new=[]
    for heure in date_list:
        heure_new.append(int(heure[11:13]+heure[14:16]+heure[17:19]))
    return heure_new



# Agrandi donnée en ajoutant une colonne de date et une autre d'heure, pour trier par date puis heure

date2,heure2=new_date(date),new_heure(date)
donnee['date2']=date2
donnee['heure2']=heure2


def trouver_first_date(date_elementaire):       # Retourne la première index de la date 
    d=transformer_date(date_elementaire)
    index=0
    while d>date2[index]:
        index+=1
        if index==len(date2):
            break
    return index


def trouver_last_date(date_elementaire):        # Retourne la dernière index de la date
    d=transformer_date(date_elementaire)
    index=0
    while d>=date2[index]:
        index+=1
        if index==len(date2):
            break
    return index


#_______________________________________________________________________________

    # Tri les donnée en fonction de la date puis de l'heure

def swap(a,i,b,j,L):
    L[i]=b
    L[j]=a


def trier_date(L,date_list):                    # date_list est la liste avec laquelle on trie le tableau
    n=len(date_list)                            # Normalement, len(date)=len(heure)
    for k in range(n):
        for i in range(n-1-k):
            a=int(date_list[i])
            b=int(date_list[i+1])
            if a>b:
                swap(a,i,b,i+1,date_list)
                for col in L:
                    x=col[i]
                    y=col[i+1]
                    swap(x,i,y,i+1,col)


def trier_heure2(L,heure_list):                    # heure_list est la liste avec laquelle on trie la liste L
    heure=heure_list                                # Il faut donc la garder non-trié pour les autres colonnes
    n=len(heure_list)                           
    for k in range(n):
        for i in range(n-1-k):
            a=int(heure[i])
            b=int(heure[i+1])
            if a>b:
                swap(a,i,b,i+1,heure)
                x=L[i]
                y=L[i+1]
                swap(x,i,y,i+1,L)


def trier_heure(L,date_elementaire,heure):            # On utilise le fait que tableau est déjà trié avec la date
    i=trouver_first_date(str(date_elementaire))
    j=trouver_last_date(str(date_elementaire))
    for col in L:
        trier_heure2(col,heure[i:j])
    

    #La stratégie consiste à transformer le tableau dataframe en une liste de liste
    #Car les opérations sont plus connus. Puis de la retransformer en dateframe

def transformer_en_liste(dataframe):
    L=[]
    for c in dataframe:
        col=dataframe[str(c)].tolist()
        L.append(col)
    return L


def transformer_en_dataframe(liste,dataframe):
    k=0
    for c in dataframe:
        dataframe[str(c)]=liste[k]
        k+=1
    return dataframe


def Trier_tableau(L,date,heure):           # L est le tableau des données
    l=transformer_en_liste(L)
    trier_date(l,date)
    list_date_possible=[]
    for date_elementaire in date:           # On énumère toutes les dates possibles
        if date_elementaire not in list_date_possible:
            list_date_possible.append(date_elementaire)
    for date_elementaire in list_date_possible:
        trier_heure(l,date_elementaire,heure)
    L=transformer_en_dataframe(l,L)
    return L


    
# On pourrait executer la fonction Trier_tableau :
# donnee=Trier_tableau(donnee,date2,heure2)
# Mais elle est très lente (2.3min avec le module time)

# On privilégira :
donnee.sort_values(by=['date2','heure2'])          
# environ 0.0127s



#_______________________________________________________________________________


# Courbe :

def Afficher_carbone(start_date='2019-08-11',end_date='2019-08-25'):
    i=trouver_first_date(start_date)
    j=trouver_last_date(end_date)
    x = date.tolist()[i:j]
    y = carbone.tolist()[i:j]
    x,nbr_jour=abscisse(x)  

    majorLocator = MultipleLocator((nbr_jour*24)/8)              # Les grandes graduations de n en n
    majorFormatter = FormatStrFormatter('%d')
    minorLocator = MultipleLocator(((nbr_jour*24)/8)/3)          # Les petites graduations de n en n
   
    fig, ax = plt.subplots()
    plt.plot(x, y, '.-',color='black', label="Carbone")
    
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_major_formatter(majorFormatter)
    ax.xaxis.set_minor_locator(minorLocator)
    
    plt.xlabel('Temps (h)')
    plt.ylabel('Carbone')

    plt.title('Evolution carbone')
    
    plt.show()
    return None


def Afficher_temperature(start_date='2019-08-11',end_date='2019-08-25'):
    i=trouver_first_date(start_date)
    j=trouver_last_date(end_date)
    x = date.tolist()[i:j]
    y = temperature.tolist()[i:j]
    x,nbr_jour=abscisse(x)  

    majorLocator = MultipleLocator((nbr_jour*24)/8)              # Les grandes graduations de n en n
    majorFormatter = FormatStrFormatter('%d')
    minorLocator = MultipleLocator(((nbr_jour*24)/8)/3)          # Les petites graduations de n en n
   
    fig, ax = plt.subplots()
    plt.plot(x, y, '.-',color='blue', label="Température")
    
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_major_formatter(majorFormatter)
    ax.xaxis.set_minor_locator(minorLocator)
    
    plt.xlabel('Temps (h)')
    plt.ylabel('Température')

    plt.title('Evolution température')
    
    plt.show()
    return None


def Afficher_luminosite(start_date='2019-08-11',end_date='2019-08-25'):
    i=trouver_first_date(start_date)
    j=trouver_last_date(end_date)
    x = date.tolist()[i:j]
    y = donnee.lum.tolist()[i:j]
    x,nbr_jour=abscisse(x)  

    majorLocator = MultipleLocator((nbr_jour*24)/8)              # Les grandes graduations de n en n
    majorFormatter = FormatStrFormatter('%d')
    minorLocator = MultipleLocator(((nbr_jour*24)/8)/3)          # Les petites graduations de n en n
   
    fig, ax = plt.subplots()
    plt.plot(x, y, '.-',color='yellow', label="Luminosité")
    
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_major_formatter(majorFormatter)
    ax.xaxis.set_minor_locator(minorLocator)

    plt.xlabel('Temps (h)')
    plt.ylabel('Luminosité')

    plt.title('Evolution luminosité')
    
    plt.show()
    return None
    

def Afficher_bruit(start_date='2019-08-11',end_date='2019-08-25'):
    i=trouver_first_date(start_date)
    j=trouver_last_date(end_date)
    x = date.tolist()[i:j]
    y = donnee.noise.tolist()[i:j]
    x,nbr_jour=abscisse(x)  

    majorLocator = MultipleLocator((nbr_jour*24)/8)              # Les grandes graduations de n en n
    majorFormatter = FormatStrFormatter('%d')
    minorLocator = MultipleLocator(((nbr_jour*24)/8)/3)          # Les petites graduations de n en n
   
    fig, ax = plt.subplots()
    plt.plot(x, y, '.-',color='green', label="Bruit")
    
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_major_formatter(majorFormatter)
    ax.xaxis.set_minor_locator(minorLocator)
    
    plt.xlabel('Temps (h)')
    plt.ylabel('Bruit')

    plt.title('Evolution bruit')
    
    plt.show()
    return None


def Afficher_humidite(start_date='2019-08-11',end_date='2019-08-25'):
    i=trouver_first_date(start_date)
    j=trouver_last_date(end_date)
    x = date.tolist()[i:j]
    y = hum.tolist()[i:j]
    x,nbr_jour=abscisse(x)  

    majorLocator = MultipleLocator((nbr_jour*24)/8)              # Les grandes graduations de n en n
    majorFormatter = FormatStrFormatter('%d')
    minorLocator = MultipleLocator(((nbr_jour*24)/8)/3)          # Les petites graduations de n en n
   
    fig, ax = plt.subplots()
    plt.plot(x, y, '.-',color='cyan', label="Humidité")
    
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_major_formatter(majorFormatter)
    ax.xaxis.set_minor_locator(minorLocator)
    
    plt.xlabel('Temps (h)')
    plt.ylabel('Humidité')

    plt.title('Evolution humidité')
    
    plt.show()
    return None


def Afficher_courbe(start_date='2019-08-11',end_date='2019-08-25'):
    i=trouver_first_date(start_date)
    j=trouver_last_date(end_date)
    x = date.tolist()[i:j]
    y = carbone.tolist()[i:j]
    x,nbr_jour=abscisse(x) 
    
    majorLocator = MultipleLocator((nbr_jour*24)/8)           
    majorFormatter = FormatStrFormatter('%d')
    minorLocator = MultipleLocator(((nbr_jour*24)/8)/3)       
   
    fig, ax = plt.subplots()
    plt.plot(x, y, '.-',color='black', label="Carbone")
    y2 = temperature.tolist()[i:j]
    plt.plot(x, y2, '.-',color='blue', label="Température")
    y3 = donnee.lum.tolist()[i:j]
    plt.plot(x, y3, '.-',color='yellow', label="Luminosité")
    y4 = donnee.noise.tolist()[i:j]
    plt.plot(x, y4, '.-',color='green', label="Bruit")
    y5 = hum.tolist()[i:j]
    plt.plot(x, y5, '.-',color='cyan', label="Humidité")
    
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_major_formatter(majorFormatter)
    ax.xaxis.set_minor_locator(minorLocator)
    plt.xlabel('Temps (h)')
    
    plt.legend(bbox_to_anchor=(0.8, 1), loc='upper left', borderaxespad=0.)
    if start_date==end_date:
        plt.title('Donnée du '+start_date)
    else:
        plt.title('Donnée entre le '+start_date+' et le '+end_date)
    
    plt.show()
    return None


def Afficher_correlation(col1,col2,start_date,end_date):
    i=trouver_first_date(start_date)
    j=trouver_last_date(end_date)
    x = date.tolist()[i:j]
    y = col1.tolist()[i:j]
    x,nbr_jour=abscisse(x)  

    majorLocator = MultipleLocator((nbr_jour*24)/8)              # Les grandes graduations de n en n
    majorFormatter = FormatStrFormatter('%d')
    minorLocator = MultipleLocator(((nbr_jour*24)/8)/3)          # Les petites graduations de n en n
   
    fig, ax = plt.subplots()
    plt.plot(x, y, '.-',color='black')
    
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_major_formatter(majorFormatter)
    ax.xaxis.set_minor_locator(minorLocator)

    y2 = col2.tolist()[i:j]
    plt.plot(x, y2, '.-',color='blue')
    
    plt.xlabel('Temps (h)')
    
    k,j,i=anomalie_list_plusieurs_jour(y,donnee.heure3,x)
    plt.scatter(i,j,color='red',label="anomalie")
    
    plt.legend(bbox_to_anchor=(0.8, 1), loc='upper left', borderaxespad=0.)
    plt.title('Donnée entre le '+start_date+' et le '+end_date)
    
    plt.show()
    return None


#____________________________________________________________


# Courbe avec statistique :

    # Il faudrait avoir deux lignes horizontales de couleur pour le max et le min

def ligne(periode,valeur):           # On défini une fonction qui nous génère une ligne  
    x=periode
    y=[valeur for k in periode]
    return x,y
    
    
def droite_verticale(abscisse,max,min):      # On défini une fonction qui nous génère une droite verticale 
    x=[abscisse for k in range(3)]
    y=[min,(max+min)/2,max]
    return x,y
    

def transformer_heure(h):
    h=h/10000
    hint=int(h)                 # heure entière
    h2=(h-hint)*100
    hmin=int(h2)                # minute
    h3=(h2-hmin)*100
    hs=int(h3)                  # seconde
    h=hint+(hmin/60)+(hs/3600)
    return h


def abscisse(x):            # Transformer '2019-08-17 12:50:26 +2:00' en 12,83
    D,H=new_date(x),new_heure(x)
    L=[]
    n=len(D)
    date=D[0]
    i=0
    index=[]
    m=0
    
    for k in range(n):      # Compter le len pour les différents jours, puis rajouter 24 pour le jour d'après
        if date!=D[k]:
            date=D[k]
            index.append(k)
            i=1
        else:
            i+=1
            
    for k in range(n):      
        if k in index:
            m+=1

        heure=transformer_heure(H[k])+m*24
        L.append(heure)
    return L,len(index)+1


def Afficher_carbone_stat(start_date='2019-08-11',end_date='2019-08-25'):
    i=trouver_first_date(start_date)
    j=trouver_last_date(end_date)
    x = date.tolist()[i:j]
    y = carbone.tolist()[i:j]
    plt.plot(x, y, '.-',color='black', label="Carbone")
    plt.xlabel('Temps (h)')
    plt.ylabel('Carbone')
    
    x,maxi=ligne(x,f.max_col(y))                               # On ajoute la ligne du max
    plt.plot(x,maxi, '--', color='lightgrey', label='max/min')
    
    x,mini=ligne(x,f.min_col(y))                               # On ajoute la ligne du min
    plt.plot(x,mini, '--',color='lightgrey')

    mean=f.mediane(y)          
    moy=f.moyenne(y)
    e="{0:.2f}".format(ecart_type(y))       # "{0:.2f}".format(nombre) permet d'arrondir nombre à deux chiffre après la virgule
    v="{0:.2f}".format(variance(y))
    
    plt.plot(0,moy,color='None',label='médiane = '+str(mean))
    plt.plot(0,moy,color='None',label='moyenne = '+str(moy))
    plt.plot(0,moy,color='None',label='écart-type = '+str(e))
    plt.plot(0,moy,color='None',label='variance = '+str(v))
    
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.tight_layout()
    
    plt.title('Evolution carbone')
    plt.show()
    return None


    # Sur le même modèle, on généralise cette fonction pour toutes les colonnes

def recup(var):
    if var=='Carbone':
        return donnee.co2
    elif var=='Température':
        return donnee.temp
    elif var=='Luminosité':
        return donnee.lum
    elif var=='Bruit':
        return donnee.noise
    elif var=='Humidité':
        return donnee.humidity
    elif var=='Humidex':
        return donnee.temp, donnee.hum


def Afficher_stat(col,start_date='2019-08-11',end_date='2019-08-25'):
    i=trouver_first_date(start_date)
    j=trouver_last_date(end_date)
    x = date.tolist()[i:j]
    x,nbr_jour=abscisse(x)  

    majorLocator = MultipleLocator((nbr_jour*24)/8)              # Les grandes graduations de n en n
    majorFormatter = FormatStrFormatter('%d')
    minorLocator = MultipleLocator(((nbr_jour*24)/8)/3)          # Les petites graduations de n en n

    y = recup(col)
    y=y.tolist()[i:j]      
    fig, ax = plt.subplots()
    plt.plot(x, y, '.-',color='black', label=str(col))
    
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_major_formatter(majorFormatter)
    ax.xaxis.set_minor_locator(minorLocator)
    
    plt.xlabel('Temps (h)')
    plt.ylabel(str(col))
    
    x,maxi=ligne(x,f.max_col(y))                               # On ajoute la ligne du max
    plt.plot(x,maxi, '--', color='lightgrey', label='max/min')
    
    x,mini=ligne(x,f.min_col(y))                               # On ajoute la ligne du min
    plt.plot(x,mini, '--',color='lightgrey')

    mean=f.mediane(y)       
    moy=f.moyenne(y)
    e=f.ecart_type(y)
    v=f.variance(y)
    
    mean_valeur="{0:.2f}".format(mean)      # "{0:.2f}".format(nombre) permet d'arrondir nombre à deux chiffre après la virgule
    moy_valeur="{0:.2f}".format(moy) 
    e_valeur="{0:.2f}".format(e)       
    v_valeur="{0:.2f}".format(v)
    
    x,mean2=ligne(x,mean)
    x,moy2=ligne(x,moy)
    x,e_sup=ligne(x,moy+e)
    x,e_inf=ligne(x,moy-e)
    x,v_sup=ligne(x,moy+v)
    x,v_inf=ligne(x,moy-v)
    
    plt.plot(x,mean2,color='purple',label='médiane = '+str(mean_valeur))
    plt.plot(x,moy2,color='red',label='moyenne = '+str(moy_valeur))
    plt.plot(x,e_sup,color='orange',label='écart-type = '+str(e_valeur))
    plt.plot(x,e_inf,color='orange')
    #plt.plot(x,v_sup,color='cyan',label='variance = '+str(v_valeur))
    #plt.plot(x,v_inf,color='cyan')
    
    plt.legend(bbox_to_anchor=(0.75, 1), loc='upper left', borderaxespad=0.)
    
    if nbr_jour==1:
        plt.title("Evolution "+str(col).lower()+" du "+start_date[8:10]+" août 2019\n")
    else:
        plt.title("Evolution "+str(col).lower()+" entre le "+start_date[8:10]+" et le "+end_date[8:10]+" août 2019\n")
    
    plt.show()
    return None



#_______________________________________________________________________________

# Corrélation :


def Afficher_correlation(col1,col2,start_date,end_date):
    i=p.trouver_first_date(start_date)
    j=p.trouver_last_date(end_date)
    donnee1=recup(col1)
    donnee2=recup(col2)
    x = p.date.tolist()[i:j]
    y = donnee1.tolist()[i:j]
    x,nbr_jour=abscisse(x)  

    majorLocator = MultipleLocator((nbr_jour*24)/8)              # Les grandes graduations de n en n
    majorFormatter = FormatStrFormatter('%d')
    minorLocator = MultipleLocator(((nbr_jour*24)/8)/3)          # Les petites graduations de n en n
   
    fig, ax = plt.subplots()
    plt.plot(x, y, '.-',color='black',label=str(col1))
    
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_major_formatter(majorFormatter)
    ax.xaxis.set_minor_locator(minorLocator)

    y2 = donnee2.tolist()[i:j]
    plt.plot(x, y2, '.-',color='blue',label=str(col2))
    
    plt.xlabel('Temps (h)')
    plt.legend(bbox_to_anchor=(0.8, 1), loc='upper left', borderaxespad=0.)
    indice="{0:.2f}".format(f.correlation(donnee1,donnee2))
    plt.title("Corrélation entre "+str(col1).lower()+" et "+str(col2).lower()+" : "+str(indice))
    
    plt.show()
    return None


#_______________________________________________________________________________

# Anomalie :

def is_anomalie(col,id):
    C=col
    m=moyenne(col)
    if abs(col[id]-m)>ecart_type(col):
        return True
    return False


def find_anomalie_id_value(col,first,last):
    C=col[first:last]
    l=[]
    L=[]
    n=len(C)
    for i in range(n):
        if is_anomalie(col,i):
            l.append(i)
            L.append(col[i])
    return l,L


# Dérive :

def derive(L,T):                # Il faut que len(T)=len(L)>0
    l=[]
    n=len(L)
    for k in range(n-1):
        x=(float(L[k+1])-float(L[k]))/(float(T[k+1])-float(T[k]))
        l.append(x)
    return l


def vitesse(L,T):
    return derive(L,T)
    
    
def acceleration(L,T):
    n=len(T)-1
    return vitesse(vitesse(L,T),T[0:n])


# Heure :

def Heure(H):
    heure=[]
    for h in H:
        h=h/10000
        hint=int(h)                 # heure entière
        h2=(h-hint)*100
        hmin=int(h2)                # minute
        h3=(h2-hmin)*100
        hs=int(h3)                  # seconde
        h=hint+(hmin/60)+(hs/3600)
        heure.append(h)
    return heure


heure3=Heure(donnee.heure2)
donnee['heure3']=heure3


# Définition de "e", la plus grande variatiion de l'acceleration possible (sans anomalie)

e=1000


def is_anomalie2(acc,id):          # acc=acceleration(col,date2)
    if abs(acc[id])>e:
        return True
    return False


def anomalie_list(col,T):
    index=[]
    value=[]
    acc=acceleration(col,T)
    for i in range(len(col)-2):
        if is_anomalie2(acc,i):
            index.append(i)
            value.append(col[i])
    return index,value


def anomalie_list_plusieurs_jour(col,T,date):
    index=[]
    value=[]
    D=[]
    acc=acceleration(col,T)
    for i in range(len(col)-2):
        if is_anomalie2(acc,i):
            index.append(i)
            value.append(col[i])
            D.append(date[i])
    return index,value,D


def anomalie_list_une_journee(col,T,heure):
    index=[]
    value=[]
    h=[]
    acc=acceleration(col,T)
    for i in range(len(col)-2):
        if is_anomalie2(acc,i):
            index.append(i)
            value.append(col[i])
            h.append(heure[i])
    return index,value,h


#_______________________________________________________________________________

# Inutile : Enlever les anomalies

def drop_anomalie(col,T):
    index=anomalie_list(col,T)
    donnee.drop(index)
    return None


def drop_anomalie_donnee(L):        # L = donnee
    D=donnee.date2
    drop_anomalie(donnee.co2,D)
    drop_anomalie(donnee.temp,D)
    drop_anomalie(donnee.humidity,D)
    drop_anomalie(donnee.noise,D)
    drop_anomalie(donnee.lum,D)
    return None


#_______________________________________________________________________________


    # Affichage des anomalies, en utilisant l'accélération :

def Afficher_un_jour_avec_anomalie(jour):
    if len(str(jour))>8:
        jour,h=separer_date(str(jour))
    jour=int(jour)
    carbone_journee,temperature_journee,hum_journee,bruit_journee,lum_journee,date_journee,heure_journee=separer_une_journee(jour)
    
    jour2=jour-20190800

    x = [x/10000 for x in heure_journee]
    y = carbone_journee
    y2 = temperature_journee
    y3 = bruit_journee
    y4 = hum_journee
    y5 = lum_journee
    
    plt.plot(x, y,color='black',label="carbone")
    plt.plot(x, y2,color='blue',label="température")
    plt.plot(x, y3,color='green',label="bruit")
    plt.plot(x, y4,color='cyan',label="humidité")
    plt.plot(x, y5,color='yellow',label="luminosité")
    
    k,j,i=anomalie_list_une_journee(lum_journee,donnee.heure3,heure_journee)
    i=[x/10000 for x in i]
    plt.scatter(i,j,color='red',label="anomalie")
    
    plt.xlabel('Temps')
    plt.title('Donnée de la journee du '+str(jour2)+' août 2019')
    plt.legend(bbox_to_anchor=(0.8, 1), loc='upper left', borderaxespad=0.)
    plt.show()
    return None


def Afficher_un_jour_avec_anomalie_carbone(jour):
    if len(str(jour))>8:
        jour,h=separer_date(str(jour))
    jour=int(jour)

    carbone_journee,temperature_journee,hum_journee,bruit_journee,lum_journee,date_journee,heure_journee=separer_une_journee(jour)

    jour2=jour-20190800

    x = [x/10000 for x in heure_journee]
    y = carbone_journee
    plt.plot(x, y,color='black',label="carbone")
    
    k,j,i=anomalie_list_une_journee(carbone_journee,donnee.heure3,heure_journee)
    i=[x/10000 for x in i]
    plt.scatter(i,j,color='red',label="anomalie")
    
    plt.xlabel('Temps')
    plt.title('Donnée de la journee du '+str(jour2)+' août 2019')
    plt.legend(bbox_to_anchor=(0.8, 1), loc='upper left', borderaxespad=0.)
    plt.show()
    return None


#_______________________________________________________________________________


# Courbe avec anomalie :


def Afficher_courbe_anomalie(start_date='2019-08-11',end_date='2019-08-25'):
    i=trouver_first_date(start_date)
    j=trouver_last_date(end_date)
    x = date.tolist()[i:j]
    y = carbone.tolist()[i:j]
    plt.plot(x, y, '.-',color='black', label="Carbone")
    y2 = temperature.tolist()[i:j]
    plt.plot(x, y2, '.-',color='blue', label="Température")
    y3 = donnee.lum.tolist()[i:j]
    plt.plot(x, y3, '.-',color='yellow', label="Luminosité")
    y4 = donnee.noise.tolist()[i:j]
    plt.plot(x, y4, '.-',color='green', label="Bruit")
    y5 = hum.tolist()[i:j]
    plt.plot(x, y5, '.-',color='cyan', label="Humidité")
    
    plt.xlabel('Temps')
    
    k,j,i=anomalie_list_plusieurs_jour(y,donnee.heure3,x)
    plt.scatter(i,j,color='red',label="anomalie")
    
    plt.legend(bbox_to_anchor=(0.8, 1), loc='upper left', borderaxespad=0.)
    plt.title('Donnée entre le '+start_date+' et le '+end_date)
    
    plt.show()
    return None









