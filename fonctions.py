import numpy as np


        # Fonctions de base


# Operation :

def exp_rapide(n,x=np.e):
    if n==0:
        return 1
    if n==1:
        return x
    if n%2==0:
        return exp_rapide(n//2,x)*exp_rapide(n//2,x)
    else:
        return exp_rapide(n//2,x)*exp_rapide((n//2)+1,x)
    

def exp(x):
    n=int(x)
    d=x-int(x)
    e_entier=exp_rapide(n)
    e_fract=np.e**d
    return e_entier*e_fract


#____________________________________________________________


# Max / Min / Abs:

def max(x,y):
    if x>y:
        return x
    else:
        return y


def min(x,y):
    if x>y:
        return y
    else:
        return x


def abs(x):
    if x>=0:
        return x
    else:
        return -x


#____________________________________________________________


# Tri :

def swap(a,i,b,j,L):
    L[i]=b
    L[j]=a


    # Tri bulle

def bubbleSort(L):
    n=len(L)
    for k in range(n):
        for i in range(n-1-k):
            a=L[i]
            b=L[i+1]
            if a>b:
                swap(a,i,b,i+1,L)
    return L
    
    
    # Tri par inserction
    
def insertionSort(L):
    n=len(L)
    for i in range(1,n):
        ref=L[i]
        j=i
        while j>0:
            a=L[j-1]
            if ref<a:
                swap(a,j-1,ref,j,L)
                j=j-1
            else:
                break
    return L


    # Tri rapide

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
        madiane=moyenne((a,b))
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
    var=moyen_carree-moyen
    return var


def ecart_type(l):
    var=variance(l)
    return var**(1/2)


#____________________________________________________________


# Indice humidex :

def humidex_unite(Tair,Trosee):
    e=exp(5417.7530*((1/273.16)-(1/(273.15+Trosee))))
    H=Tair+0.5555*(6.11*e-10)
    return H


def humidex(start_date='2019-01-01',end_date='2019-02-01'):
    # Pour annee entre annee_date, pour mois entre moi_date, pour jour entre jour_date
    
    Tair, Trosee=20,20
    
    H=humidex_unite(Tair,Trosee)
    
    return H













