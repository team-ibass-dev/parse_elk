# coding:utf8
'''
Created on 12 sept. 2018

@author: marius
'''
import os
import textfsm


def parse_cisco_command(path_src_file,path_template_file):
    
    # path_src_file=r""+path_src_file.decode('utf8').encode('utf8')
    # path_template_file=r""+path_template_file.decode('utf8').encode('utf8')
    
    if not os.path.exists(path_src_file):
        return "Désolé le fichier source indiqué est introuvable !"
    elif not os.path.isfile(path_src_file):
        return "Désolé le chemin source ne correspond pas à celui d'un fichier"
    
    if not os.path.exists(path_template_file):
        return "Désolé le fichier template indiqué est introuvable !"
    elif not os.path.isfile(path_template_file):
        return "Désolé le chemin vers fichier template ne correspond pas à celui d'un fichier"
    
    template_file=open(path_template_file,"r")
    template_data=textfsm.TextFSM(template_file)
    template_file.close()
    
    src_file=open(path_src_file,"r")
    src_data=src_file.read()
    src_file.close()
    
    parse_result=list()
    titres=template_data.header
    try:
        parse_result =  template_data.ParseText(src_data)
        return parse_result,titres
    except:
        return "Une erreur est survenue au cours de l'opération !",titres
    
    
    
    
    
    
    
    
    
    