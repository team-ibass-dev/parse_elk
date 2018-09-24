# coding:utf8
'''
Created on 12 sept. 2018

@author: marius
'''
import re

def Extraire_une_partie_de_liste(liste,pattern_deb,pattern_fin):
    resultat=list()
    i=-1
    for elt in liste:
        if re.match(pattern_deb,elt) is not None:
            i=0
        
        if i>=1:
            if re.match(pattern_fin,elt) is None:
                resultat.append(elt)
            else:
                break
        if i==0:
            i=i+1
    return resultat

def Extraire_une_partie_de_liste2(liste,pattern_deb,nbre_ligne):
    resultat=list()
    i=-1
    for elt in liste:
        if re.match(pattern_deb,elt) is not None:
            i=0
        
        if i>=1:
            if len(resultat)<nbre_ligne:
                resultat.append(elt)
            else:
                break
        if i==0:
            i=i+1
    return resultat

