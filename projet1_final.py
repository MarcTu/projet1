import fonctions as f

from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


donnee = pd.read_csv("post-32566-EIVP_KM.csv", sep=';')

    # On récupère des données :
    
temperature=donnee['temp']
hum=donnee['humidity']
carbone=donnee['co2']
lum=donnee['lum']
bruit=donnee['noise']
date=donnee['sent_at']

donnee1=donnee[ donnee['id'] == 1 ]
donnee2=donnee[ donnee['id'] == 2 ]
donnee3=donnee[ donnee['id'] == 3 ]
donnee4=donnee[ donnee['id'] == 4 ]
donnee5=donnee[ donnee['id'] == 5 ]
donnee6=donnee[ donnee['id'] == 6 ]

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



def trouver_first_date(date_elementaire,date_list):       # Retourne la première index de la date 
    d=transformer_date(date_elementaire)                  # Si on prend tout le tableau donnee, date_list=date2
    index=0                                               # Sinon, on prend date_list=new_date(donneei.sent_at)
    while d>date_list[index]:
        index+=1
        if index==len(date2):
            break
    return index


def trouver_last_date(date_elementaire,date_list):        # Retourne la dernière index de la date
    d=transformer_date(date_elementaire)                  # Si on prend tout le tableau donnee, date_list=date2
    index=0                                               # Sinon, on prend date_list=new_date(donneei.sent_at)
    while d>=date_list[index]:
        index+=1
        if index==len(date_list):
            break
    return index


# Transformation en heure pour l'affichage des abscisses :

def transformer_heure(h):
    h=h/10000
    hint=int(h)                 # heure entière
    h2=(h-hint)*100
    hmin=int(h2)                # minute
    h3=(h2-hmin)*100
    hs=int(h3)                  # seconde
    h=hint+(hmin/60)+(hs/3600)
    return h


def Heure(H):
    heure=[]
    for h in H:
        heure.append(transformer_heure(h))
    return heure


def abscisse(x):            # Transformer '2019-08-17 12:50:26 +2:00' en 12,83
    if x==[]:
        return x,0
    D,H=new_date(x),new_heure(x)
    L=[]
    n=len(D)
    date=D[0]
    nbr_jour=int(D[n-1])-date+1
    for k in range(n):      
        heure=transformer_heure(H[k])+24*(D[k]-date)
        L.append(heure)
    return L,nbr_jour

heure3=Heure(donnee.heure2)
donnee['heure3']=heure3


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


def trier_heure2(L,heure_list):           # heure_list est la liste avec laquelle on trie la liste L
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
    i=trouver_first_date(str(date_elementaire),date2)
    j=trouver_last_date(str(date_elementaire),date2)
    for k in range(len(L)):
        trier_heure2(L[k][i:j],heure[i:j])


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
    for i in range(11,26):
        trier_heure(l,'2019-08-'+str(i),heure)
    L=transformer_en_dataframe(l,L)
    return L

"""import time as time
d=time.time()
On pourrait executer la fonction Trier_tableau :
donnee=Trier_tableau(donnee,date2,heure2)
print(time.time()-d)
# Mais elle est très lente (1.47min avec le module time), même si elle est plus rapide qu'avant (2.3min)"""

# On privilégira :
donnee=donnee.sort_values(by=['date2','heure2'])          
# environ 0.0127s





#_______________________________________________________________________________


# Courbe :

def Afficher_courbe(col,doc,start_date='2019-08-11',end_date='2019-08-25'):
    i=trouver_first_date(start_date,new_date(doc.sent_at))
    j=trouver_last_date(end_date,new_date(doc.sent_at))
    x = doc.sent_at.tolist()[i:j]
    y=recup(col,doc)
    y = y.tolist()[i:j]
    x,nbr_jour=abscisse(x) 
    
    majorLocator = MultipleLocator((nbr_jour*24)/8)           
    majorFormatter = FormatStrFormatter('%d')
    minorLocator = MultipleLocator(((nbr_jour*24)/8)/3)       
   
    fig, ax = plt.subplots()
    plt.plot(x, y, '.-',color='black', label=str(col))
    
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_major_formatter(majorFormatter)
    ax.xaxis.set_minor_locator(minorLocator)
    plt.xlabel('Temps (h)')
    plt.ylabel(str(col)+" (en "+unite(col)+")")
    
    plt.legend(bbox_to_anchor=(0.8, 1), loc='upper left', borderaxespad=0.)
    if start_date==end_date:
        plt.title('Evolution de '+str(col).lower()+' du '+start_date)
    else:
        plt.title('Evolution de '+str(col).lower()+' entre le '+start_date+' et le '+end_date)
    
    plt.show()
    return None


def appeler_une_donnee(col,doc,start_date,end_date,couleur,num):
    i=trouver_first_date(start_date,new_date(doc.sent_at.tolist()))
    j=trouver_last_date(end_date,new_date(doc.sent_at.tolist()))
    x = doc.sent_at.tolist()[i:j]
    y = recup(col,doc)
    y=y.tolist()[i:j]
    x,nbr_jour=abscisse(x) 
    plt.plot(x, y, '.-',color=couleur, label=str(col)+str(num))


def Afficher_courbe_tout_donnee(col,start_date='2019-08-11',end_date='2019-08-25'):
    nbr_jour=transformer_date(end_date)-transformer_date(start_date)+1
    majorLocator = MultipleLocator((nbr_jour*24)/8)           
    majorFormatter = FormatStrFormatter('%d')
    minorLocator = MultipleLocator(((nbr_jour*24)/8)/3)       
   
    fig, ax = plt.subplots()
    
    appeler_une_donnee(col,donnee,start_date,end_date,'black','')
    appeler_une_donnee(col,donnee1,start_date,end_date,'blue',1)
    appeler_une_donnee(col,donnee2,start_date,end_date,'green',2)
    appeler_une_donnee(col,donnee3,start_date,end_date,'yellow',3)
    appeler_une_donnee(col,donnee4,start_date,end_date,'cyan',4)
    appeler_une_donnee(col,donnee5,start_date,end_date,'orange',5)
    appeler_une_donnee(col,donnee6,start_date,end_date,'pink',6)

    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_major_formatter(majorFormatter)
    ax.xaxis.set_minor_locator(minorLocator)
    plt.xlabel('Temps (h)')
    plt.ylabel(str(col)+" (en "+unite(col)+")")
    
    plt.legend(bbox_to_anchor=(0.8, 1), loc='upper left', borderaxespad=0.)
    if start_date==end_date:
        plt.title('Donnée du '+start_date)
    else:
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


def Afficher_carbone_stat(start_date='2019-08-11',end_date='2019-08-25'):
    i=trouver_first_date(start_date,new_date(doc.sent_at.tolist()))
    j=trouver_last_date(end_date,new_date(doc.sent_at.tolist()))
    x = date.tolist()[i:j]
    y = carbone.tolist()[i:j]
    plt.plot(x, y, '.-',color='black', label="Carbone (en g)")
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

def recup(var,doc):
    if var=='Carbone':
        return doc.co2
    elif var=='Température':
        return doc.temp
    elif var=='Luminosité':
        return doc.lum
    elif var=='Bruit':
        return doc.noise
    elif var=='Humidité':
        return doc.humidity
    elif var=='Humidex':
        return doc.temp, doc.humidity


UNITE={'Carbone':'g','Température':'°C','Luminosité':'lx','Bruit':'dB','Humidité':'%','Humidex':'°C'}


def unite(col):
    Unite=UNITE[str(col)]
    return Unite


def Afficher_stat(col,doc,start_date='2019-08-11',end_date='2019-08-25',anomalie=False):
    i=trouver_first_date(start_date,new_date(doc.sent_at.tolist()))
    j=trouver_last_date(end_date,new_date(doc.sent_at.tolist()))
    x = doc.sent_at.tolist()[i:j]
    x,nbr_jour=abscisse(x) 
    
    if col=='Humidex':
        a,b = recup(col,doc)
        y=humidex(a.tolist(),b.tolist(),doc,start_date,end_date)
    else:
        y = recup(col,doc)
        y=y.tolist()[i:j]   

    majorLocator = MultipleLocator((nbr_jour*24)/8)              # Les grandes graduations de n en n
    majorFormatter = FormatStrFormatter('%d')
    minorLocator = MultipleLocator(((nbr_jour*24)/8)/3)          # Les petites graduations de n en n
      
    fig, ax = plt.subplots()
    plt.plot(x, y, '.-',color='black', label=str(col))
    
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_major_formatter(majorFormatter)
    ax.xaxis.set_minor_locator(minorLocator)
    
    if anomalie:
        if j-i==len(donnee) and col!='Humidex':
            appeler_anomalie2(x,y,col,doc)
        else:
            appeler_anomalie(x,y)
    
    plt.xlabel('Temps (h)')
    plt.ylabel(str(col)+" (en "+str(unite(col))+")")
    
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
    
    plt.legend(bbox_to_anchor=(0.75, 1), loc='upper left', borderaxespad=0.)
    
    if anomalie:
        if nbr_jour==1:
            plt.title("Evolution de "+str(col).lower()+" du "+start_date[8:10]+" août 2019 avec anomalie\n")
        else:
            plt.title("Evolution de "+str(col).lower()+" entre le "+start_date[8:10]+" et le "+end_date[8:10]+" août 2019 avec anomalie\n")
    else:
        if nbr_jour==1:
            plt.title("Evolution de "+str(col).lower()+" du "+start_date[8:10]+" août 2019\n")
        else:
            plt.title("Evolution de "+str(col).lower()+" entre le "+start_date[8:10]+" et le "+end_date[8:10]+" août 2019\n")
    plt.show()
    return None


#____________________________________________________________


    # Indice humidex :


def humidex_unite(Tair,hum):
    H=Tair+(5/9)*(6.112*10**(7.5*Tair/(237.7+Tair))*(hum/100)-10)
    return H


def humidex(temp,hum,doc,start_date,end_date):
    H=[]
    i=trouver_first_date(start_date,new_date(doc.sent_at.tolist()))
    j=trouver_last_date(end_date,new_date(doc.sent_at.tolist()))
    temp,hum=temp[i:j],hum[i:j]
    n=len(temp)
    for k in range(n):
        H.append(humidex_unite(temp[k],hum[k]))
    return H
    
    
    # Courbe de l'évolution de l'indice humidex :


def Afficher_humidex(humidex,doc,start_date,end_date):
    i=trouver_first_date(start_date,new_date(doc.sent_at.tolist()))
    j=trouver_last_date(end_date,new_date(doc.sent_at.tolist()))
    x = doc.sent_at.tolist()[i:j]
    x,nbr_jour=abscisse(x)  

    majorLocator = MultipleLocator((nbr_jour*24)/8)              # Les grandes graduations de n en n
    majorFormatter = FormatStrFormatter('%d')
    minorLocator = MultipleLocator(((nbr_jour*24)/8)/3)          # Les petites graduations de n en n

    y = humidex 
    fig, ax = plt.subplots()
    plt.plot(x, y, '.-',color='blue', label="Indice humidex")
    
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_major_formatter(majorFormatter)
    ax.xaxis.set_minor_locator(minorLocator)
    
    plt.xlabel('Temps (h)')
    plt.ylabel('Humidex (en °C)')
    
    (xmin, xmax, ymin, ymax)=plt.axis()
    
    x,inconfort1=ligne(x,15)                                  # On rajoute les seuils d'inconfort
    x,inconfort2=ligne(x,30)
    
    if ymax>30 and ymin<15:
        plt.fill_between(x,inconfort2,p.ligne(x,ymax)[1],hatch="///",edgecolor="r",facecolor='white',label="Zone d'inconfort")     
        plt.fill_between(x,inconfort1,p.ligne(x,ymin)[1],hatch="///",edgecolor="r",facecolor='white')     
    else:
        if ymax>30:
            plt.fill_between(x,inconfort2,ligne(x,ymax)[1],hatch="///",edgecolor="r",facecolor='white',label="Zone d'inconfort")     
        if ymin<15:
            plt.fill_between(x,inconfort1,ligne(x,ymin)[1],hatch="///",edgecolor="r",facecolor='white',label="Zone d'inconfort")     
    
    plt.legend(bbox_to_anchor=(0.75, 1), loc='upper left', borderaxespad=0.)
    
    if nbr_jour==1:
        plt.title("Evolution de l'indice humidex du "+start_date[8:10]+" août 2019\n")
    else:
        plt.title("Evolution de l'indice humidex entre le "+start_date[8:10]+" et le "+end_date[8:10]+" août 2019\n")
    fig.tight_layout()
    plt.show()
    return None



#____________________________________________________________


# Courbe avec la corrélation de deux variables :


def Afficher_correlation(col1,col2,doc,start_date,end_date,anomalie=False):     # col1 et col2 sont les noms de colonne
    i=trouver_first_date(start_date,new_date(doc.sent_at.tolist()))
    j=trouver_last_date(end_date,new_date(doc.sent_at.tolist()))
    cor1=recup(col1,doc)                                     # On récupère les colonnes (listes) de donnée
    cor2=recup(col2,doc)
    x = doc.sent_at.tolist()[i:j]
    y = cor1.tolist()[i:j]
    x,nbr_jour=abscisse(x)  

    majorLocator = MultipleLocator((nbr_jour*24)/8)              # Les grandes graduations de n en n
    majorFormatter = FormatStrFormatter('%d')
    minorLocator = MultipleLocator(((nbr_jour*24)/8)/3)          # Les petites graduations de n en n
   
    fig, ax = plt.subplots()
    ax.set_xlabel('Temps (h)')
    ax.set_ylabel(str(col1)+" (en "+str(unite(col1))+")", color='tab:green')
    ax.plot(x, y, color='tab:green')
    ax.tick_params(axis='y', labelcolor='tab:green')
    if anomalie:
        if j-i==len(donnee):
            appeler_anomalie2(x,y,col1,doc)
        else:
            appeler_anomalie(x,y)
    
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_major_formatter(majorFormatter)
    ax.xaxis.set_minor_locator(minorLocator)

    y2 = cor2.tolist()[i:j]
    ax2 = ax.twinx() 
    ax2.set_ylabel(str(col2)+" (en "+str(unite(col2))+")", color='tab:blue')
    ax2.plot(x, y2, color='tab:blue')
    ax2.tick_params(axis='y', labelcolor='tab:blue')
    
    if anomalie:
        if j-i==len(donnee):
            appeler_anomalie2(x,y2,col2,doc)
        else:
            appeler_anomalie(x,y2)
    
    indice="{0:.2f}".format(f.correlation(y,y2))
    if anomalie:
        plt.legend(bbox_to_anchor=(0.75, 1), loc='upper left', borderaxespad=0.)
        if nbr_jour==1:
            plt.title("Corrélation entre "+str(col1).lower()+" et "+str(col2).lower()+" : "+indice+"\ndu "+start_date[8:10]+" août 2019 avec anomalie\n")
        else:
            plt.title("Corrélation entre "+str(col1).lower()+" et "+str(col2).lower()+" : "+indice+"\nentre le "+start_date[8:10]+" et le "+end_date[8:10]+" août 2019 avec anomalie\n")
    else:
        if nbr_jour==1:
            plt.title("Corrélation entre "+str(col1).lower()+" et "+str(col2).lower()+" : "+indice+"\ndu "+start_date[8:10]+" août 2019\n")
        else:
            plt.title("Corrélation entre "+str(col1).lower()+" et "+str(col2).lower()+" : "+indice+"\nentre le "+start_date[8:10]+" et le "+end_date[8:10]+" août 2019\n")
    fig.tight_layout()
    plt.show()
    return None



#_______________________________________________________________________________


#Detection anomalies avec distance interquartile
 
def interQ_detect(document,col):
    q1 = recup(col,document).quantile(0.25)
    q3 = recup(col,document).quantile(0.75)
    iqr = q3-q1 #distance Interquartile 
    limite_inf  = q1-1.5*iqr
    limite_sup = q3+1.5*iqr
    n=len(document.index)
    l=[]
    L=[]
    a=0
    column=' '
    if col=='Bruit':
        a=2
        column='noise'
    elif col=='Température':
        a=3
        column='temp'
    elif col=='Humidité':
        a=4
        column='humidity'
    elif col=='Luminosité':
        a=5
        column='lum'
    elif col=='Carbone':
        a=6
        column='co2'
    for i in range(n):
        if document.loc[document.index[i],column]<= limite_inf or document.loc[document.index[i],column]>= limite_sup :
            l.append(document.iloc[i,a])        #liste de valeurs associées à la variable choisie entre les deux dates
            L.append(document.iloc[i,7])        #liste de dates associées à la variable choisie entre les deux dates

    date=Heure(new_heure(L))
    D=[]
    for k in range (len(L)):
        D.append(date[k]+24*(int(L[k][8:10])-11))
    return(l,D)



    # Dérive :

def derive(L,T):                # Il faut que len(T)=len(L)>0
    l=[]
    n=len(L)
    for k in range(n-1):
        try:
            x=(float(L[k+1])-float(L[k]))/(float(T[k+1])-float(T[k]))
        except:
            x=(float(L[k+1])-float(L[k]))/(float(T[k+1])-float(T[k])+0.1)
        l.append(x)
    return l



    # Courbe anomalie :

def Afficher_derive2(col,doc,start_date='2019-08-11',end_date='2019-08-25'):  
    i=trouver_first_date(start_date,new_date(doc.sent_at.tolist()))
    j=trouver_last_date(end_date,new_date(doc.sent_at.tolist()))
    y=recup(col,doc)                                     # On récupère les colonnes (listes) de donnée
    x = doc.sent_at.tolist()[i:j]
    y = y.tolist()[i:j]
    x,nbr_jour=abscisse(x)  

    if col=='Humidex':
        a,b = recup(col,doc)
        y=humidex(a.tolist(),b.tolist(),start_date,end_date)
    else:
        y = recup(col,doc)
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
    
    mean=f.mediane(y2)       
    moy=f.moyenne(y2)
    e=f.ecart_type(y2)*3
    
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
    if abs(der[id])>3*ecart+m:
        return True
    return False


def anomalie_list3(col,T):
    index=[]
    value=[]
    heure=[]
    der=derive(col,T)
    moyen,ecart=f.moyenne(der),f.ecart_type(der)
    for i in range(len(col)-1):
        if is_anomalie3(der,moyen,ecart,i):
            index.append(i)
            value.append(col[i])
            heure.append(T[i])
    return index,value,heure



def Afficher_colonne_avec_anomalie(col,doc,start_date='2019-08-11',end_date='2019-08-25'):
    i=trouver_first_date(start_date,new_date(doc.sent_at.tolist()))
    j=trouver_last_date(end_date,new_date(doc.sent_at.tolist()))
    x = doc.sent_at.tolist()[i:j]
    x,nbr_jour=abscisse(x) 
    
    if col=='Humidex':
        a,b = recup(col,doc)
        y=humidex(a.tolist(),b.tolist(),start_date,end_date)
    else:
        y = recup(col,doc)
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


""" On peut donc considérer que tout les point de la dérivé en dehors de n*écart-type de la moyenne est une anomalie. Plus n est grand et plus le pic de l'anomalie détecté est grande, donc plus la valeur est anormalement éloignée. On fait donc la même chose mais en fonction de n """


def is_anomalie_n(der,m,ecart,id,n):          # der est la liste des derive
    if abs(der[id])>n*ecart+m:
        return True
    return False


def anomalie_list_n(col,T,n):
    index=[]
    value=[]
    heure=[]
    der=derive(col,T)
    moyen,ecart=f.moyenne(der),f.ecart_type(der)
    for i in range(len(col)-1):
        if is_anomalie_n(der,moyen,ecart,i,n):
            index.append(i)
            value.append(col[i])
            heure.append(T[i])
    return index,value,heure


# On prend n arbitrairement égale au plus grand n tel qu'il existe une anomalie
n=10


def Afficher_colonne_avec_anomalie_n(col,doc,start_date='2019-08-11',end_date='2019-08-25'):
    i=trouver_first_date(start_date,new_date(doc.sent_at.tolist()))
    j=trouver_last_date(end_date,new_date(doc.sent_at.tolist()))
    x = doc.sent_at.tolist()[i:j]
    x,nbr_jour=abscisse(x) 
    
    if col=='Humidex':
        a,b = recup(col,doc)
        y=humidex(a.tolist(),b.tolist(),doc,start_date,end_date)
    else:
        y = recup(col,doc)
        y=y.tolist()[i:j]   

    majorLocator = MultipleLocator((nbr_jour*24)/8)              # Les grandes graduations de n en n
    majorFormatter = FormatStrFormatter('%d')
    minorLocator = MultipleLocator(((nbr_jour*24)/8)/3)          # Les petites graduations de n en n
      
    fig, ax = plt.subplots()
    plt.plot(x, y, '.-',color='blue', label=str(col),zorder=1)
    
    if j-i==len(donnee) and col!='Humidex':
        appeler_anomalie2(x,y,col,doc)
    else:
        appeler_anomalie(x,y)
        
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_major_formatter(majorFormatter)
    ax.xaxis.set_minor_locator(minorLocator)
    
    plt.xlabel('Temps (h)')
    plt.ylabel(str(col)+" (en"+unite(col)+")")
    
    plt.legend(bbox_to_anchor=(0.75, 1), loc='upper left', borderaxespad=0.)
    if nbr_jour==1:
        plt.title("Evolution de "+str(col).lower()+" du "+start_date[8:10]+" août 2019 avec anomalie\n")
    else:
        plt.title("Evolution de "+str(col).lower()+" entre le "+start_date[8:10]+" et le "+end_date[8:10]+" août 2019 avec anomalie\n")

    fig.tight_layout()
    plt.show()
    return None


# Plutôt que de réécrire toutes les fonctions, on peut choisir d'ajouter ou non l'affichage des anomalies dans les autres fonctions d'affichage


def appeler_anomalie(x,y):
    k,j,i=anomalie_list3(y,x)
    plt.scatter(i,j,marker='o',color='red',label="anomalie",zorder=2,s=3**2)
    for p in range(3,n+1):
        k,j,i=anomalie_list_n(y,x,p)
        plt.scatter(i,j,marker='o',color='red',zorder=p,s=(p+1)**2)
    return None


def appeler_anomalie2(x,y,col,doc):
    k,j,i=anomalie_list3(y,x)
    plt.scatter(i,j,marker='o',color='red',label="anomalie",zorder=2,s=3**2)
    for p in range(3,n+1):
        k,j,i=anomalie_list_n(y,x,p)
        plt.scatter(i,j,marker='o',color='red',zorder=p,s=(p+1)**2)
    j,i=interQ_detect(doc,col)
    plt.scatter(i,j,marker='o',color='purple',label="anomalie2",zorder=2,s=3**2)
    return None



#_______________________________________________________________________________

    # Trouver les période d'occupation des bureaux

def periode_presence_bureau():
    document,col=donnee,'Bruit'
    q1 = recup(col,document).quantile(0.25)
    q3 = recup(col,document).quantile(0.75)
    iqr = q3-q1 #distance Interquartile 
    limite_inf  = q1-1.5*iqr
    limite_sup = q3+1.5*iqr
    n=len(document.index)
    l=[]
    L=[]
    a=0
    column=' '
    if col=='Bruit':
        a=2
        column='noise'
    elif col=='Température':
        a=3
        column='temp'
    elif col=='Humidité':
        a=4
        column='humidity'
    elif col=='Luminosité':
        a=5
        column='lum'
    elif col=='Carbone':
        a=6
        column='co2'
    for i in range(n):
        if document.loc[document.index[i],column]<= limite_inf or document.loc[document.index[i],column]>= limite_sup :
            l.append(document.iloc[i,a])        #liste de valeurs associées à la variable choisie entre les deux dates
            L.append(document.iloc[i,7])        #liste de dates associées à la variable choisie entre les deux dates

        # L=liste de date+heure

    D=[]
    heure1,heure2=[],[]
    date_possible=[]
    date_list=[]
    for date in L:
        if transformer_date(date) not in date_possible:
            date_possible.append(transformer_date(date))
            date_list.append(date)

    for date in date_list:
        i=trouver_first_date(date,new_date(L))
        j=trouver_last_date(date,new_date(L))
        x,y=L[i],L[j-1]
        heure1.append(transformer_heure(int(x[11:13]+x[14:16]+x[17:19])))
        heure2.append(transformer_heure(int(y[11:13]+y[14:16]+y[17:19])))
        D.append("Jour "+str(transformer_date(x))[6:8]+" : occupation de "+str(transformer_heure(int(x[11:13]+x[14:16]+x[17:19])))+" à "+str(transformer_heure(int(y[11:13]+y[14:16]+y[17:19])))+"\n")
    S=""
    for date in D:
        S+=date
    print(S)
    
    moy1="{0:.2f}".format(f.moyenne(heure1))
    moy2="{0:.2f}".format(f.moyenne(heure2))
    print("\nLa moyenne des occupations sur un jour est de : "+str(moy1)+"h à "+str(moy2)+"h")
    return None





























