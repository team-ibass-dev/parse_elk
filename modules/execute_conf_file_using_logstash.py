# coding:utf8
'''
Created on 13 sept. 2018

@author: marius
'''
import os
import signal
from modules import recuperer_configurations as conf


def Execute_conf_file_using_logstash(path_conf_file):
    config=conf.recuperer_configuration()

    try:
        os.system(config["path_stop"]+" stop")
        os.system(config["path_run_conf_file"]+" -f "+path_conf_file)
    except:
        return "Une erreur s'est produite au cours de l'opération !. \nVérifiez vos inputs et rassurer vous également que logstash est lancé"
        
        
        