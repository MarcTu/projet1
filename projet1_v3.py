import fonctions

from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


donnee = pd.read_csv("post-32566-EIVP_KM.csv", sep=';')

temperature=donnee['temp']
hum=donnee['humidity']
carbone=donnee['co2']

date=donnee['sent_at']



#_______________________________________________________________________________


# Date :

def separer_date_heure(date_elementaire):
    if len(date_elementaire)>=19:
        d=date_elementaire[0:10]
        h=date_elementaire[11:19]
    else:
        d=date_elementaire[0:10]
        h=[]
    return d,h


def separer_date(date_elementaire):         # a-b-c ...
    d,h=separer_date_heure(date_elementaire)
    a=''
    b=''
    for x in d:
        if x!='-':
            a+=x
    if h==[]:
        b=0
    else:
        for y in h:
            if y!=':':
                b+=y
    return int(a),int(b)                          # [abc]


def separer_date2(date_elementaire):         # a-b-c ...
    D=[]
    H=[]
    d,h=separer_date_heure(date_elementaire)
    a=''
    b=''
    for x in d:
        if x=='-':
            D.append(int(a))
            a=''
        if x!='-':
            a+=x
    D.append(int(a))
    for y in h:
        if y==':':
            H.append(int(b))
            b=''
        if y!=':':
            b+=y
    H.append(int(b))
    return D,H                           # [a,b,c]


def separer_date_liste(date_liste):
    L=[]
    H=[]
    n=len(date_liste)
    for k in range(n):
        l,h=separer_date(date_liste[k])
        L.append(l)
        H.append(h)
    return L,H


def separer_date_liste_num(date_liste):
    L=[]
    n=len(date_liste)
    for k in range(n):
        l,h=separer_date(date_liste[k])
        num=[k]
        num.append(l)
        L.append(num)
    return L


def completer_date(d,max):        # n est la longueur de la liste réelle et max la lonngueur voulue
    n=len(d)
    if n<10:
        m=10-n
        X=''
        for k in range(m):
            X+='0'
        d=d+X
    return d


# Agrandi donnee en ajoutant une colonne de date et une autre d'heure

date2,heure2=separer_date_liste(date)
donnee['date2']=date2
donnee['heure2']=heure2


def trouver_first_date(date_elementaire):       # Retourne la première index de la date 
    d,h=separer_date(date_elementaire)
    index=0
    while d>date2[index]:
        index+=1
        if index==len(date2):
            break
    return index


def trouver_last_date(date_elementaire):        # Retourne la dernière index de la date
    d,h=separer_date(date_elementaire)
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
    heure=heure_list
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
    

    #La stratégie consiste a transformer le tableau dataframe en une liste de liste
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
    #donnee=Trier_tableau(donnee,date2,heure2)
# Mais elle est très lente (envirron 2.3min)

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
  
    fig, ax = plt.subplots()
    plt.plot(x, y, '.-',color='black', label="Carbone")

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
    
    plt.legend(bbox_to_anchor=(0.8, 1), loc='upper left', borderaxespad=0.)
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

# Courbe avec anomalie :

def Afficher_carbone_anomalie(start_date='2019-08-11',end_date='2019-08-25'):
    i=trouver_first_date(start_date)
    j=trouver_last_date(end_date)
    x = date.tolist()[i:j]
    y = carbone.tolist()[i:j]
    plt.plot(x, y, '.-',color='black', label="Carbone")
    plt.xlabel('Temps')
    plt.ylabel('Carbone')
    
    k,j,i=anomalie_list_plusieurs_jour(y,donnee.heure3,x)
    plt.scatter(i,j,color='red',label="anomalie")
    
    plt.legend(bbox_to_anchor=(0.8, 1), loc='upper left', borderaxespad=0.)
    plt.title('Evolution carbone')
    
    plt.show()
    return None


def Afficher_temperature_anomalie(start_date='2019-08-11',end_date='2019-08-25'):
    i=trouver_first_date(start_date)
    j=trouver_last_date(end_date)
    x = date.tolist()[i:j]
    y = temperature.tolist()[i:j]
    plt.plot(x, y, '.-',color='blue', label="Température")
    plt.xlabel('Temps')
    plt.ylabel('Température')
    
    k,j,i=anomalie_list_plusieurs_jour(y,donnee.heure3,x)
    plt.scatter(i,j,color='red',label="anomalie")
    
    plt.legend(bbox_to_anchor=(0.8, 1), loc='upper left', borderaxespad=0.)
    plt.title('Evolution température')
    
    plt.show()
    return None


def Afficher_luminosite_anomalie(start_date='2019-08-11',end_date='2019-08-25'):
    i=trouver_first_date(start_date)
    j=trouver_last_date(end_date)
    x = date.tolist()[i:j]
    y = donnee.lum.tolist()[i:j]
    plt.plot(x, y, '.-',color='yellow', label="Luminosité")
    plt.xlabel('Temps')
    plt.ylabel('Luminosité')
    
    k,j,i=anomalie_list_plusieurs_jour(y,donnee.heure3,x)
    plt.scatter(i,j,color='red',label="anomalie")
    
    plt.legend(bbox_to_anchor=(0.8, 1), loc='upper left', borderaxespad=0.)
    plt.title('Evolution luminosité')
    
    plt.show()
    return None
    

def Afficher_bruit_anomalie(start_date='2019-08-11',end_date='2019-08-25'):
    i=trouver_first_date(start_date)
    j=trouver_last_date(end_date)
    x = date.tolist()[i:j]
    y = donnee.noise.tolist()[i:j]
    plt.plot(x, y, '.-',color='green', label="Bruit")
    plt.xlabel('Temps')
    plt.ylabel('Bruit')
    
    k,j,i=anomalie_list_plusieurs_jour(y,donnee.heure3,x)
    plt.scatter(i,j,color='red',label="anomalie")
    
    plt.legend(bbox_to_anchor=(0.8, 1), loc='upper left', borderaxespad=0.)
    plt.title('Evolution bruit')
    
    plt.show()
    return None


def Afficher_humidite_anomalie(start_date='2019-08-11',end_date='2019-08-25'):
    i=trouver_first_date(start_date)
    j=trouver_last_date(end_date)
    x = date.tolist()[i:j]
    y = hum.tolist()[i:j]
    plt.plot(x, y, '.-',color='cyan', label="Humidité")
    plt.xlabel('Temps')
    plt.ylabel('Humidité')
    
    k,j,i=anomalie_list_plusieurs_jour(y,donnee.heure3,x)
    plt.scatter(i,j,color='red',label="anomalie")
    
    plt.legend(bbox_to_anchor=(0.8, 1), loc='upper left', borderaxespad=0.)
    plt.title('Evolution humidité')
    
    plt.show()
    return None


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



#____________________________________________________________


# Statistique : Moyenne, mediane, variance :

def moyenne(l):
    moyen=0
    n=len(l)
    for x in l:
        moyen+=x
    moyen=moyen/n
    return moyen

def mediane(l):
    l=quickSort(l)
    mediane=0
    n=len(l)
    if n%2==0:
        a=l[n//2]
        b=l[(n//2)+1]
        mediane=moyenne((a,b))
    else:
        mediane=l[n//2]
    return mediane
        

def variance(l):        # E(x**2)-E(x)**2
    Lcarree=[]
    var=0
    moyen=moyenne(l)
    for x in l:
        Lcarree.append(x**2)
    moyen_carree=moyenne(Lcarree)
    var=moyen_carree-moyen**2
    return var


def covariance(X,Y):
    n=len(X)
    m=len(Y)
    if n!=m:
        return None
    S=0
    x=moyenne(X)
    y=moyenne(Y)
    for i in range(n):
        S+=X[i]*Y[i]
    S=S/n
    covar=S-x*y
    return covar


def ecart_type(l):
    var=variance(l)
    return var**(1/2)


# Tri :

def swap(a,i,b,j,L):
    L[i]=b
    L[j]=a


def partitionner(T, first, last, pivot):
    n=len(T)
    
    swap(T[pivot],pivot,T[last],last,T)         # échange le pivot avec le dernier du tableau , le pivot devient le dernier du tableau
    j = first
    for i in range(first,last):                 # la boucle se termine quand i = (dernier-1).
        if T[i] <= T[last]:
            swap(T[i],i,T[j],j,T)
            j = j + 1
    swap(T[last],last,T[j],j,T)
    return j


def choix_pivot(T,first, last):
    return (first+last)//2


def tri_rapide(T,first,last):
    if first<last:
        pivot = choix_pivot(T, first, last)
        pivot = partitionner(T, first, last, pivot)
        tri_rapide(T, first, pivot-1)
        tri_rapide(T, pivot+1, last)


def quickSort(T):
    
    tri_rapide(T,0,len(T)-1)
    
    return T


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
    D,H=separer_date_liste(x)
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
    
    x,maxi=ligne(x,max_col(y))                               # On ajoute la ligne du max
    plt.plot(x,maxi, '--', color='lightgrey', label='max/min')
    
    x,mini=ligne(x,min_col(y))                               # On ajoute la ligne du min
    plt.plot(x,mini, '--',color='lightgrey')

    mean=mediane(y)          
    moy=moyenne(y)
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
    
    y = recup(col)
    y=y.tolist()[i:j]      
    
    plt.plot(x, y, '.-',color='black', label=str(col))
    plt.xlabel('Temps')
    plt.ylabel(str(col))
    
    x,maxi=ligne(x,max_col(y))                               # On ajoute la ligne du max
    plt.plot(x,maxi, '--', color='lightgrey', label='max/min')
    
    x,mini=ligne(x,min_col(y))                               # On ajoute la ligne du min
    plt.plot(x,mini, '--',color='lightgrey')

    mean=mediane(y)          
    moy=moyenne(y)
    e="{0:.2f}".format(ecart_type(y))       # "{0:.2f}".format(nombre) permet d'arrondir nombre à deux chiffre après la virgule
    v="{0:.2f}".format(variance(y))
    
    plt.plot(0,moy,color='None',label='médiane = '+str(mean))
    plt.plot(0,moy,color='None',label='moyenne = '+str(moy))
    plt.plot(0,moy,color='None',label='écart-type = '+str(e))
    plt.plot(0,moy,color='None',label='variance = '+str(v))
    
    plt.legend(bbox_to_anchor=(0.75, 1), loc='upper left', borderaxespad=0.)
    plt.title("Evolution "+str(col).lower()+" en fonction du temps\n")
    plt.show()
    return None



#_______________________________________________________________________________

# Moyenne des journée : Transformer la tableau de donnée en tableau moyenné par jour/Avec un filtre

    # Avec list_une_journee, on selectionne toutes les données d'une journée, 
    # puis on en fait la moyenne sur une ligne, et on les ajoute à un nouveau tableau 


def list_jour_moyen(L, first='2019-08-11', last='2019-08-25'):      #L est la liste de donnée
    first,h=separer_date(first)
    last,h=separer_date(last)
    donnee_tous_jours=[]
    
    carbone_tous_jours,temperature_tous_jours,hum_tous_jours,bruit_tous_jours,lum_tous_jours,date_tous_jours=[],[],[],[],[],[]
    
    n=last-first
    
    for i in range(n+1):
        jour=first+i
        jour2=jour-20190800
        donnee_une_journee=list_une_journee(donnee,jour)
        
        carbone_tous_jours.append(moyenne(donnee_une_journee.co2))
        temperature_tous_jours.append(moyenne(donnee_une_journee.temp))
        hum_tous_jours.append(moyenne(donnee_une_journee.humidity))
        bruit_tous_jours.append(moyenne(donnee_une_journee.noise))
        lum_tous_jours.append(moyenne(donnee_une_journee.lum))
        date_tous_jours.append(jour2)
        
    return carbone_tous_jours, temperature_tous_jours, hum_tous_jours, bruit_tous_jours, lum_tous_jours, date_tous_jours
    

def Afficher_jours_moyen(first='2019-08-11', last='2019-08-25'):
    carbone_tous_jours, temperature_tous_jours, hum_tous_jours, bruit_tous_jours, lum_tous_jours, date_tous_jours=list_jour_moyen(donnee)
    
    x = date_tous_jours
    y = carbone_tous_jours
    y2 = temperature_tous_jours
    y3 = bruit_tous_jours
    y4 = hum_tous_jours
    y5 = lum_tous_jours

    plt.plot(x, y,color='black',label="carbone")
    plt.plot(x, y2,color='red',label="température")
    plt.plot(x, y3,color='green',label="bruit")
    plt.plot(x, y4,color='cyan',label="humidité")
    plt.plot(x, y5,color='yellow',label="luminosité")
    
    plt.xlabel('Jours')
    plt.title('Donnée entre le '+str(date_tous_jours[0])+' et le '+str(date_tous_jours[-1])+' août 2019')
    plt.legend(bbox_to_anchor=(0.8, 1), loc='upper left', borderaxespad=0.)
    
    plt.show()
    return None


def Afficher_moyen(col,first='2019-08-11', last='2019-08-25'):
    carbone_tous_jours, temperature_tous_jours, hum_tous_jours, bruit_tous_jours, lum_tous_jours, date_tous_jours=list_jour_moyen(donnee)
    x = date_tous_jours
    
    if col=='co2':
        y = carbone_tous_jours
        plt.title('Evolution de carbone entre le '+str(date_tous_jours[0])+' et le '+str(date_tous_jours[-1])+' août 2019')
    elif col=='temp':
        y = temperature_tous_jours
        plt.title('Evolution de la température entre le '+str(date_tous_jours[0])+' et le '+str(date_tous_jours[-1])+' août 2019')
    elif col=='noise':
        y = bruit_tous_jours
        plt.title('Evolution du bruit entre le '+str(date_tous_jours[0])+' et le '+str(date_tous_jours[-1])+' août 2019')
    elif col=='hum':
        y = hum_tous_jours
        plt.title("Evolution de l'humidité entre le "+str(date_tous_jours[0])+' et le '+str(date_tous_jours[-1])+' août 2019')
    elif col=='lum':
        y = lum_tous_jours
        plt.title('Evolution de la luminosité entre le '+str(date_tous_jours[0])+' et le '+str(date_tous_jours[-1])+' août 2019')
    else:
        return "Cette colonne n'existe pas"

    plt.plot(x, y)
    plt.xlabel('Jours')
    plt.show()
    return None


def Afficher_moyen2(*col,first='2019-08-11', last='2019-08-25'):
    carbone_tous_jours, temperature_tous_jours, hum_tous_jours, bruit_tous_jours, lum_tous_jours, date_tous_jours=list_jour_moyen(donnee)
    x = date_tous_jours
    
    for k in col:
        k=str(k)
        if k=='co2':
            y = carbone_tous_jours
            plt.plot(x, y,color='black',label="carbone")
        elif k=='temp':
            y2 = temperature_tous_jours
            plt.plot(x, y2,color='red',label="température")
        elif k=='noise':
            y3 = bruit_tous_jours
            plt.plot(x, y3,color='green',label="bruit")
        elif k=='hum':
            y4 = hum_tous_jours
            plt.plot(x, y4,color='cyan',label="humidité")
        elif k=='lum':
            y5 = lum_tous_jours
            plt.plot(x, y5,color='yellow',label="luminosité")
            
        else:
            print("La colonne "+k+" n'existe pas")
    
    plt.xlabel('Jours')
    plt.title('Donnée entre le '+str(date_tous_jours[0])+' et le '+str(date_tous_jours[-1])+' août 2019')
    plt.legend(bbox_to_anchor=(0.8, 1), loc='upper left', borderaxespad=0.)

    plt.show()
    return None


#_______________________________________________________________________________

# Une journée :

def list_une_journee(L,jour):      #L est la liste de donnée
    donnee_une_journee=donnee[donnee.date2==jour]
    donnee_une_journee.sort_values(by='heure2')
    return donnee_une_journee


def separer_une_journee(jour):
    donnee_une_journee=list_une_journee(donnee,jour)
    
    carbone_journee=donnee_une_journee.co2.tolist()
    temperature_journee=donnee_une_journee.temp.tolist()
    hum_journee=donnee_une_journee.humidity.tolist()
    bruit_journee=donnee_une_journee.noise.tolist()
    lum_journee=donnee_une_journee.lum.tolist()
    date_journee=donnee_une_journee.date2
    heure_journee=donnee_une_journee.heure2.tolist()
    
    return carbone_journee,temperature_journee,hum_journee,bruit_journee,lum_journee,date_journee,heure_journee

    
def Afficher_une_journee(jour):
    donnee_une_journee=list_une_journee(donnee,jour)
    donnee_une_journee.sort_values(by='heure2')
    x = donnee_une_journee.heure2
    y = donnee_une_journee.co2
    y2 = donnee_une_journee.temp
    y3 = donnee_une_journee.noise
    y4 = donnee_une_journee.humidity
    y5 = donnee_une_journee.lum

    plt.plot(x, y,color='black')
    plt.plot(x, y2,color='red')
    plt.plot(x, y3,color='green')
    plt.plot(x, y4,color='cyan')
    plt.plot(x, y5,color='yellow')
    
    plt.xlabel('Temps')
    plt.title('Donnée sur une journée')
    
    plt.show()
    return None


def Afficher_journee(jour,col=None):
    if col==None:
        return Afficher_une_journee(jour)
    
    donnee_une_journee=list_une_journee(donnee,jour)
    donnee_une_journee.sort_values(by='heure2')
    x = donnee_une_journee.heure2
    y = donnee_une_journee.col

    plt.plot(x, y)
    
    plt.xlabel('Temps')
    plt.title('Donnée sur une journée')
    
    plt.show()
    return None


def Afficher_une_journee2(jour):
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
    plt.plot(x, y2,color='red',label="température")
    plt.plot(x, y3,color='green',label="bruit")
    plt.plot(x, y4,color='cyan',label="humidité")
    plt.plot(x, y5,color='yellow',label="luminosité")
    
    plt.xlabel('Temps')
    plt.title('Donnée de la journee du '+str(jour2)+' août 2019')
    plt.legend(bbox_to_anchor=(0.8, 1), loc='upper left', borderaxespad=0.)
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


def Afficher_anomalie(col,start_date='2019-08-11',end_date='2019-08-25'):
    x = date
    y = col
    first=0
    last=10
    id,value=find_anomalie_id_value(col,first,last)
    plt.plot(x, y, '.-')
    plt.xlabel('Temps')
    plt.ylabel(col)
    plt.title('Anomalie')
    
    plt.show()
    return None






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



def Afficher_derive(col,start_date='2019-08-11',end_date='2019-08-25'):
    i=trouver_first_date(start_date)
    j=trouver_last_date(end_date)
    x = date.tolist()[i:j]
    x,nbr_jour=abscisse(x) 
    
    if col=='Humidex':
        a,b = recup(col)
        y=humidex(a.tolist(),b.tolist(),start_date,end_date)
    else:
        y = recup(col)
        y=y.tolist()[i:j]   

    majorLocator = MultipleLocator((nbr_jour*24)/8)              # Les grandes graduations de n en n
    majorFormatter = FormatStrFormatter('%d')
    minorLocator = MultipleLocator(((nbr_jour*24)/8)/3)          # Les petites graduations de n en n
      
    fig, ax = plt.subplots()
    plt.plot(x, y, '.-',color='blue', label=str(col))
    
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_major_formatter(majorFormatter)
    ax.xaxis.set_minor_locator(minorLocator)
    
    plt.xlabel('Temps (h)')
    plt.ylabel(str(col))
    
    y2=derive(y,donnee.heure3.tolist())
    plt.plot(x[:len(x)-1], y2, '.-',color='red', label="dérivé")


    plt.legend(bbox_to_anchor=(0.75, 1), loc='upper left', borderaxespad=0.)
    
    if nbr_jour==1:
        plt.title("Evolution "+str(col).lower()+" du "+start_date[8:10]+" août 2019\n")
    else:
        plt.title("Dérivé de "+str(col).lower()+" entre le "+start_date[8:10]+" et le "+end_date[8:10]+" août 2019\n")
    
    plt.show()
    return None



def Afficher_derive2(col,start_date='2019-08-11',end_date='2019-08-25'):  
    i=trouver_first_date(start_date)
    j=trouver_last_date(end_date)
    donnee1=recup(col)                                     # On récupère les colonnes (listes) de donnée
    x = date.tolist()[i:j]
    y = donnee1.tolist()[i:j]
    x,nbr_jour=abscisse(x)  

    if col=='Humidex':
        a,b = recup(col)
        y=humidex(a.tolist(),b.tolist(),start_date,end_date)
    else:
        y = recup(col)
        y=y.tolist()[i:j]   


    majorLocator = MultipleLocator((nbr_jour*24)/8)              # Les grandes graduations de n en n
    majorFormatter = FormatStrFormatter('%d')
    minorLocator = MultipleLocator(((nbr_jour*24)/8)/3)          # Les petites graduations de n en n
   
    fig, ax = plt.subplots()
    ax.set_xlabel('Temps (h)')
    ax.set_ylabel(str(col))
    ax.plot(x, y, '.-',color='tab:blue')
    ax.tick_params(axis='y', labelcolor='tab:blue')
    
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_major_formatter(majorFormatter)
    ax.xaxis.set_minor_locator(minorLocator)
    
    y2 = derive(y,donnee.heure3.tolist())
    ax2 = ax.twinx() 
    ax2.set_ylabel("dérivé")
    ax2.plot(x[:len(x)-1], y2, '.-',color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')
    
    mean=mediane(y2)       
    moy=moyenne(y2)
    e=ecart_type(y2)*2
    
    mean_valeur="{0:.2f}".format(mean)      # "{0:.2f}".format(nombre) permet d'arrondir nombre à deux chiffre après la virgule
    moy_valeur="{0:.2f}".format(moy) 
    e_valeur="{0:.2f}".format(e)       
    
    x,mean2=ligne(x,mean)
    x,moy2=ligne(x,moy)
    x,e_sup=ligne(x,moy+e)
    x,e_inf=ligne(x,moy-e)
    
    plt.plot(x,mean2,color='black',label='médiane = '+str(mean_valeur))
    plt.plot(x,moy2,color='black',label='moyenne = '+str(moy_valeur))
    plt.plot(x,e_sup,color='orange',label='écart-type = '+str(e_valeur))
    plt.plot(x,e_inf,color='orange')

    plt.title("Dérivé de "+str(col).lower())
    plt.legend(bbox_to_anchor=(0.75, 1), loc='upper left', borderaxespad=0.)
    fig.tight_layout()
    plt.show()
    return None


# On peut donc considérer que tout les point de la dérivé en dehors de 2*écart-type de la moyenne est une anomalie

def is_anomalie3(der,m,ecart,id):          # der est la liste des derive
    if abs(der[id])>2*ecart+m:
        return True
    return False


def anomalie_list3(col,T):
    index=[]
    value=[]
    heure=[]
    der=derive(col,T)
    moyen,ecart=moyenne(der),ecart_type(der)
    for i in range(len(col)-1):
        if is_anomalie3(der,moyen,ecart,i):
            index.append(i)
            value.append(col[i])
            heure.append(T[i])
    return index,value,heure



def Afficher_colonne_avec_anomalie(col,start_date='2019-08-11',end_date='2019-08-25'):
    i=trouver_first_date(start_date)
    j=trouver_last_date(end_date)
    x = date.tolist()[i:j]
    x,nbr_jour=abscisse(x) 
    
    if col=='Humidex':
        a,b = recup(col)
        y=humidex(a.tolist(),b.tolist(),start_date,end_date)
    else:
        y = recup(col)
        y=y.tolist()[i:j]   

    majorLocator = MultipleLocator((nbr_jour*24)/8)              # Les grandes graduations de n en n
    majorFormatter = FormatStrFormatter('%d')
    minorLocator = MultipleLocator(((nbr_jour*24)/8)/3)          # Les petites graduations de n en n
      
    fig, ax = plt.subplots()
    plt.plot(x, y, '.-',color='blue', label=str(col),zorder=1)
    
    k,j,i=anomalie_list3(y,x)
    plt.scatter(i,j,marker='o',color='red',label="anomalie",zorder=2)
    
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_major_formatter(majorFormatter)
    ax.xaxis.set_minor_locator(minorLocator)
    
    plt.xlabel('Temps (h)')
    plt.ylabel(str(col))
    
    plt.title("Evolution de "+str(col).lower()+" avec anomalies")
    plt.legend(bbox_to_anchor=(0.75, 1), loc='upper left', borderaxespad=0.)
    fig.tight_layout()
    plt.show()
    return None














