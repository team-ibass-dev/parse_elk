# coding: utf8
'''
Created on 11 sept. 2018

@author: marius
'''
from macpath import basename
import re
from pickle import FALSE

def Verifier_si_fichier_json(path):
    file_name=basename(path)
    parties=file_name.split(".")
    _pattern="[Jj]{1}[sS]{1}[oO]{1}[nN]{1}"
    if re.match(_pattern,parties[len(parties)-1]) is None:
        return False
    else:
        return True
