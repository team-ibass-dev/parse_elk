# coding:utf8
'''
Created on 16 sept. 2018

@author: marius
'''
import re

def recuperer_configuration():
    fichier_conf=open("config","r")
    contenu=fichier_conf.readlines()
    conf=dict()
    fichier_conf.close()
    liste=list()
    for ligne in contenu: 
        #print re.match(r"^#.*",ligne)
        if re.match(r"^#.*",ligne) is None and re.match(r"\s$",ligne) is  None:
            liste=ligne.split("=")
            if(len(liste)==1):
                conf[liste[0]]=""
            else:
                conf[liste[0]]=liste[1].replace("\n","")
    return conf