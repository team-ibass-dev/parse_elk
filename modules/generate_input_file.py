# -*- coding:utf-8 -*-

from modules.app_conf import *

def generate_input_file(path,index,start_position=None,sincedb_path=None,delimiter=None,codec=None):

    if start_position!=None:
        start_position={"start_position":start_position}
    if sincedb_path!=None:
        sincedb_path={"sincedb_path":sincedb_path}
    if delimiter!=None:
        delimiter={"delimiter":delimiter}
    if codec!=None:
        codec={"codec":codec}

    file = '''
            file {
                    path => "'''+path+'''"'''
    file = add_field_not_required(file,start_position)
    file = add_field_not_required(file,sincedb_path)
    file = add_field_not_required(file,delimiter)
    file = add_field_not_required(file,codec)

    file = file + '''
                    type => "'''+index+'''"
            }
    '''
    return  file
