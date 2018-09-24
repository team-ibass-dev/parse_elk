# -*- coding:utf-8 -*-

from modules.app_conf import *

def generate_output_elasticsearch(index,hosts="127.0.0.1:9200",document_id=None,user=None,password=None):

    if hosts!=None:
        hosts = {"hosts":hosts}
    if document_id != None:
        document_id = {"document_id":document_id}
    if user != None:
        user = {"user": user}
    if password != None:
        password = {"password": password}

    elasticsearch = '''
            if [type] == "'''+index+'''" {
                elasticsearch {'''
    elasticsearch = add_field_not_required(elasticsearch,hosts)
    elasticsearch = add_field_not_required(elasticsearch, document_id)
    elasticsearch = add_field_not_required(elasticsearch, user)
    elasticsearch = add_field_not_required(elasticsearch, password)

    elasticsearch = elasticsearch + '''
                    index => "'''+index+'''"
                    document_type => "doc"
                    codec => line
                }
            }
    '''
    return elasticsearch
