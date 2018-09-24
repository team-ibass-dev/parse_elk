# -*- coding:utf-8 -*-

import os
from modules.generate_input_file import generate_input_file
from modules.generate_output_elasticsearch import generate_output_elasticsearch

def createColumns(header):
    columns = "["
    for field in header:
        if field != header[-1]:
            columns = columns + field + ","
        else:
            columns = columns + field


def generate_filter_csv(columns,separator,skip_header,skip_empty_columns="false",skip_empty_rows="true"):
    filter = '''
            csv {
                columns => '''+str(columns)+'''
                separator => "'''+separator+'''"
                skip_header => '''+skip_header+'''
                skip_empty_columns => '''+skip_empty_columns+'''
                skip_empty_rows => '''+skip_empty_rows+'''
            }
    '''

    return filter


def generate(path,index,separator=",",header=None,skip_header="true",hosts="127.0.0.1:9200",document_type="_doc",sincedb_path="/dev/null",start_position="beginning",skip_empty_columns="false",skip_empty_rows="true",document_id=None,user=None,password=None):
    if os.path.exists(path):
        if header == None:
            with open(path,"r") as f:
                columns=f.readline()
                columns = columns.replace("\n","")
                columns=columns.split(",")
                skip_header = "true"
        else:
            columns = header
            skip_header = skip_header

        input = '''
        input {
            '''+generate_input_file(path,index,start_position,sincedb_path)+'''
        } 
        '''
        filter = '''
        filter {
            '''+generate_filter_csv(columns,separator,skip_header,skip_empty_columns,skip_empty_rows)+'''
        }
        '''
        output = '''
        output {
            '''+generate_output_elasticsearch(index,hosts,document_id,user,password)+'''
        }
        '''

        file = input + filter + output

        return file
    else:

        error = "\n ---->  Le chemin passé en paramètre n'est pas correct"

        return error


