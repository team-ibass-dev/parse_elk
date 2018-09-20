# -*- coding:utf-8 -*-

import os
import shutil
from elasticsearch import Elasticsearch
from modules import generate_csv_file_conf
from modules import generate_pcap_conf
from modules import generated_json_file_conf
from modules import parser_fichiers_repertoire
from modules import json_to_elk

def stop_logstash():
    os.system("/etc/init.d/logstash stop")

def get_projet_path():
    projet_path = os.path.dirname(os.path.dirname(__file__))

    return projet_path

def create_execute_dir():

    if os.path.exists(get_projet_path()+'/temp'):
        shutil.rmtree(get_projet_path()+'/temp')
        os.mkdir(get_projet_path() + "/temp")
    else:
        os.mkdir(get_projet_path() + "/temp")

    if os.path.exists(get_projet_path()+'/results'):
        shutil.rmtree(get_projet_path()+'/results')
        os.mkdir(get_projet_path()+"/results")
    else:
        os.mkdir(get_projet_path() + "/results")



def execute():
    os.system("/opt/logstash/bin/logstash -f '"+get_projet_path()+"/temp/*.conf'")


def generated_type_file(chaine,file_name,type_file):

    if type_file=="conf":
        path_pattern = get_projet_path()+"/temp/"
    else:
        path_pattern = get_projet_path()+"/results/"

    file = open(path_pattern + file_name + "." + type_file, "w")

    file.write(chaine)

    return path_pattern + file_name + "." + type_file


def return_index(index,i=1):
    es = Elasticsearch("127.0.0.1:9200")
    result = es.indices.exists(index)
    if result==False:
        return index
    else:
        return return_index(index+"-new-"+str(i),i+1)

def create_list_dir(directory,type_file,type_input):
    list_file = {}
    if type_input == "dir":
        if directory[-1]!="/":
            directory = directory + "/"
        list = os.listdir(directory)
        for i in list:
            if os.path.splitext(os.path.basename(directory + i))[1] == type_file:
                list_file[os.path.splitext(os.path.basename(directory + i))[0]]=directory+i
    else:
        if os.path.splitext(os.path.basename(directory))[1] == type_file:
            list_file[os.path.splitext(os.path.basename(directory))[0]]=directory

    return list_file


def action(directory,action,index=None,switch=None,type_input="dir"):

    stop_logstash()
    create_execute_dir()

    if action=="cte":

        list_dir = create_list_dir(directory, ".csv", type_input)
        for i in list_dir:
            if type_input == "dir":
                index=i.lower()
            chaine_conf = generate_csv_file_conf.generate(list_dir[i],i)
            generated_type_file(chaine_conf,index,"conf")

        execute()

    elif action=="jte":

        list_dir = create_list_dir(directory, ".json", type_input)
        for i in list_dir:
            if type_input == "dir":
                index=i.lower()
            json_to_elk.json_to_elk(list_dir[i],index)

        execute()

    elif action=="pcte":

        list_dir = create_list_dir(directory,".pcap",type_input)
        for i in list_dir:
            if type_input == "dir":
                index=i.lower()
            path_csv_pcap = generated_type_file(generate_pcap_conf.generate(list_dir[i]),i,"csv")
            chaine_conf = generate_csv_file_conf.generate(path_csv_pcap, index)
            generated_type_file(chaine_conf, i, "conf")

        execute()

    elif action=="pste":

        if type_input=="file":
            parser_fichiers_repertoire.parser_fichier(directory,switch)
        elif type_input=="dir":
            parser_fichiers_repertoire.parser_fichiers_repertoire(directory,switch)


    elif action=="alte":
        pass
