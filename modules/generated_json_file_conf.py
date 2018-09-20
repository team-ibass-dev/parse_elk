# coding: utf8
'''
Created on 11 sept. 2018

@author: marius
'''
import os
from os.path import basename
import re
from modules import Verifier_si_fichier_json as verif
from modules import recuperer_configurations as conf


def Generate_json_file_conf(path_src,path_dst,index,document_type,type_json,file_name):
    config=conf.recuperer_configuration()
    host=config["hosts"]
    password=config["password"]
    user=config["user"]
    if document_type=="":
        document_type="doc"
    dico = dict()
    if user!="":
        dico["user"]=user
    if password!="":
        dico["password"]=password
    # path_src=r""+path_src.decode('utf8').encode('utf8')
    # path_dst=r""+path_dst.decode('utf8').encode('utf8')
    
    if re.match("[lLMm]{1}",type_json) is None:
        return "Désolé ce type de fichier json n'est pas pris en charge !"
    else:
        type_json=type_json.upper()
#     if not os.path.exists(path_src):
#         return "Désolé le fichier source indiqué n'existe pas !"
#     else:
#         if not os.path.isfile(path_src):
#             return "Désolé le chemin source ne correspond pas à un fichier !"
#         else:
#             if verif.Verifier_si_fichier_json(path_src) is False:
#                 return "Désolé le fichier source n'est pas un fichier json !"
    if not os.path.exists(path_dst):
        return "Désolé le dossier de destination indiqué n'existe pas !"
    else:
        if not os.path.isdir(path_dst):
            return "Désolé le chemin de destination indiqué n'est pas un dossier !"
    
    codec=""
    if type_json=="L":
        json="json => json_lines"
    else:
        json='''codec => multiline
                {
                    pattern => '^\{'
                    negate => true
                    what => previous
                }'''
    auth1=""
    auth2=""
    k=0
    for c in dico:
        if k==0:
            auth1=c+ " => \"" + dico[c]+"\""
        else:
            auth2=c+ " => \"" + dico[c]+"\""
        k=k+1
    authentif=""
    authentif="    "+auth1+'''
        '''+ auth2
      
    
    config='''input
{
    file
    {
         path => [\"'''+path_src+'''\"]
         start_position => \"beginning\"
         sincedb_path => "/dev/null\"
         exclude => \"*.gz\"
     '''+codec+'''  
    }
    
}
filter
{
    mutate
    {
        gsub => [ 'message','\\n','']
    }
    if [message] =~ /^{.*}$/
    {
        json {
            source => message
        }
    }
}
output
{
    elasticsearch
    {
        hosts => \"'''+host+'''\"
        index => \"'''+index+'''\"
        document_type => \"'''+document_type+'''\"
        codec => json
    '''+authentif+'''
    }
}'''

    conf_file=open(path_dst+"/"+file_name+".conf","w")
    conf_file.write(config)
    conf_file.close()
    return "ok"


def Generate_json_file_conf2(path_src, path_dst, index, document_type, type_json, file_name,input_type):
    config = conf.recuperer_configuration()
    host = config["hosts"]
    password = config["password"]
    user = config["user"]
    if document_type == "":
        document_type = "doc"
    dico = dict()
    if user != "":
        dico["user"] = user
    if password != "":
        dico["password"] = password
    # path_src=r""+path_src.decode('utf8').encode('utf8')
    # path_dst=r""+path_dst.decode('utf8').encode('utf8')

    if re.match("[lLMm]{1}", type_json) is None:
        return "Désolé ce type de fichier json n'est pas pris en charge !"
    else:
        type_json = type_json.upper()
    #     if not os.path.exists(path_src):
    #         return "Désolé le fichier source indiqué n'existe pas !"
    #     else:
    #         if not os.path.isfile(path_src):
    #             return "Désolé le chemin source ne correspond pas à un fichier !"
    #         else:
    #             if verif.Verifier_si_fichier_json(path_src) is False:
    #                 return "Désolé le fichier source n'est pas un fichier json !"
    if not os.path.exists(path_dst):
        return "Désolé le dossier de destination indiqué n'existe pas !"
    else:
        if not os.path.isdir(path_dst):
            return "Désolé le chemin de destination indiqué n'est pas un dossier !"

    codec = ""
    if type_json == "L":
        json = "json => json_lines"
    else:
        json = '''codec => multiline
                {
                    pattern => '^\{'
                    negate => true
                    what => previous
                }'''
    auth1 = ""
    auth2 = ""
    k = 0
    for c in dico:
        if k == 0:
            auth1 = c + " => \"" + dico[c] + "\""
        else:
            auth2 = c + " => \"" + dico[c] + "\""
        k = k + 1
    authentif = ""
    authentif = "    " + auth1 + '''
        ''' + auth2

    config = '''input
{
    file
    {
         path => [\"''' + path_src + '''\"]
         start_position => \"beginning\"
         sincedb_path => "/dev/null\"
         type => \"'''+input_type+'''\"
         exclude => \"*.gz\"
     ''' + codec + '''  
    }

}
filter
{
    mutate
    {
        gsub => [ 'message','\\n','']
    }
    if [message] =~ /^{.*}$/
    {
        json {
            source => message
        }
    }
}
output
{
    if [type] == \"'''+input_type+'''\" {
        elasticsearch
        {
            hosts => \"''' + host + '''\"
            index => \"''' + index + '''\"
            document_type => \"''' + document_type + '''\"
            codec => json
        ''' + authentif + '''
        }
    }
}'''

    conf_file = open(path_dst + "/" + file_name + ".conf", "w")
    conf_file.write(config)
    conf_file.close()
    return "ok"