# -*- coding:utf-8 -*-

def add_field_not_required(file,field=None):
    if field==None:
        return  file
    else:
        key = list(field.keys())
        key = key[0]
        file = file + '''
                    '''+key+''' => "'''+field[key]+'''"'''
        return file
