# coding:utf8
from modules import generated_json_file_conf as g
import os

def json_to_elk(path_src,index,):
    file_name=os.path.basename(path_src).replace(".json","")
    g.Generate_json_file_conf2(path_src,"temp",index,"doc","m",file_name,index)


