import fonctions

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


print(max(3, 6))


document = pd.read_csv("EIVP_KM.csv", sep=';')

temperature=document['temp']
hum=document['humidity']
carbone=document['co2']
date=document['sent_at']

print(document)


#_______________________________________________________________________________


# Date :

def separer_date(date_elementaire):         # a-b-c ...
    l=[]
    a=''
    for x in date_elementaire:
        if x=='-':
            l.append(int(a))
            a=''
        if x==' ':
            l.append(int(a))
            break

        if x!='-':
            a+=x

    return l                                # [a,b,c]


def separer_date_liste(date_liste):
    L=[]
    n=len(date_liste)
    for k in range(n):
        l=separer_date(date_liste[k])
        L.append(l)
    return L


def separer_date_liste_num(date_liste):
    L=[]
    n=len(date_liste)
    for k in range(n):
        l=separer_date(date_liste[k])
        num=[k]
        num.append(l)
        L.append(num)
    return L


def trier_date(L):
    return L



#_______________________________________________________________________________


# Courbe :

def Afficher_carbone(start_date='2019-01-01',end_date='2019-02-01'):
    x = date
    y = carbone

    #plt.subplot(2, 1, 2)

    plt.plot(x, y, '.-')
    plt.xlabel('Temps')
    plt.ylabel('Carbone')
    plt.title('Evolution carbone')
    
    plt.show()


def Afficher_temperature(start_date='2019-01-01',end_date='2019-02-01'):
    x = temperature
    y = carbone

    #plt.subplot(2, 1, 2)

    plt.plot(x, y, '.-')
    plt.xlabel('Température')
    plt.ylabel('Carbone')
    plt.title('Evolution température')
    
    plt.show()


def Afficher_humidite(start_date='2019-01-01',end_date='2019-02-01'):
    x = date
    y = carbone

    #plt.subplot(2, 1, 2)

    plt.plot(x, y, '.-')
    plt.xlabel('Temps')
    plt.ylabel('Carbone')
    plt.title('Evolution carbone')
    
    plt.show()




































