# coding:utf8
'''
Created on 12 sept. 2018

@author: marius
'''
import os


def Generer_json_file(liste_resultat,liste_titre,path_dest_file,file_name):
 
    if len(liste_resultat)==0 or len(liste_titre)==0:
        return "la liste des resulats ou des titres est vide "
    if not os.path.exists(path_dest_file):
        return "le dossier de destination indiqué est introuvable !"
    elif not os.path.isdir(path_dest_file):
        return "la destination indiquée n'est pas un repertoire !"
    if len(liste_titre)!=len(liste_resultat[0]):
        return "le nombre de titres spécifiés ne correspond pas au nombre de données à extraire"   
  
    liste_ligne=list()
    
    for liste in liste_resultat:
        k=0
        dico=dict()
        while k<len(liste):
            if type(liste[k]).__name__=='str':
                dico[liste_titre[k]]="\""+liste[k].replace("\"","")+"\""
            elif type(liste[k]).__name__=='list':
                if len(liste[k])>0:
                    valeur="[\""+'\",\"'.join(liste[k])+"\"]"
                else:
                    valeur="[]"
                dico[liste_titre[k]]=valeur
            k=k+1
        liste_ligne.append(dico)
    fichier=open(path_dest_file+"/"+file_name+".json","w")
    
    for d in liste_ligne:
        ligne="{ "
        for t in d:
            ligne=ligne+"\""+t+"\" : "+d[t]+","
        taille=len(ligne)
        if taille>0:
#             ligne[taille-1]="}"
            ligne2=""
            k=0
            for c in ligne:
                ligne2=ligne2+c
                k=k+1
                if(k+1)==taille:
                    break
#             k=0
#             while k<taille-1:
#                 ligne2=ligne2+ligne[k]
#                 k=k+1
            ligne2=ligne2+"}"
            fichier.write(ligne2+"\n")
    
    fichier.close()
    return "ok"
    
    
    
    