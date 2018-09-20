# coding:utf8
'''
Created on 12 sept. 2018

@author: marius
'''
import os
import re
from modules import parse_cisco_command_using_template as p
from modules import extraire_une_partie_de_liste as ext


def parse_vpc_status_nxos(path_src_file):
    
    # path_src_file=r""+path_src_file.decode('utf8').encode('utf8')
    if not os.path.exists(path_src_file):
        return "Le fichier source est introuvable"
    elif not os.path.isfile(path_src_file):
        return "Le chemin indiqué ne correspond pas à celui d'un fichier !"
    # lecture du contenu du fichier
    fichier=open(path_src_file,"r")
    contenu=fichier.readlines()
    fichier.close()
    contenu_=list()
    for x in contenu:
        if re.match("^\s$$",x) is None and re.match("^-",x) is None:
            contenu_.append(x)
    contenu_=ext.Extraire_une_partie_de_liste(contenu_,r"^id\s+Port\s+Status\s+Consistency\s+Reason\s+Active\s+vlans",r"^[^\d+\s]")
   
    liste=list()
    k=0
    #print(len(contenu))
    while k<len(contenu_):
        l=' '.join(contenu_[k].split())
        if re.match(r"^\d+\s+",contenu_[k]) is None:
            if re.match(r"^\s+Applicable",contenu_[k]) is None:
                liste[len(liste)-1]=liste[len(liste)-1]+l
        else:
            liste.append(l)
        k=k+1
    temp_file=open("temp/__temp.txt","w")
    for l in liste:
        temp_file.write(l+"\n")
    temp_file.close()
    parse_result,titres=p.parse_cisco_command("temp/__temp.txt","templates/cisco_nxos/secondaires/cisco_nxos_show_vpc.template")
    parse_result1=list()
    for p1 in parse_result:
        l=list()
        for q in p1:
            if type(q).__name__=='str':
                s=q.replace('Not','Not Applicable')
#                 t=q.replace('Consistency Check Not','Consistency Check Not Performed')
#                 l.append(t)
                l.append(s)
#                 print(s+"-")
            else:
                l.append(q)

        parse_result1.append(l)
    #os.system("rm __temp.txt")
    return parse_result1,titres
    
    
    
    
