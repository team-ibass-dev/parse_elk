# coding:utf8
'''
Created on 15 sept. 2018

@author: marius
'''
from macpath import basename
import os

from modules import execute_conf_file_using_logstash as exe
from modules import generated_json_file_conf as gcf
from modules import generer_json_file as g
from modules import parse_cisco_command_using_template as p
from modules import parse_show_interface_trunk_cisco_nxos_ as thk
from modules import parse_vpc_status_nxos as vpc


def parser_fichier(path_src, switch_type):
    # path_src=r""+path_src.encode('utf8')
    if os.path.exists("temp"):
        os.system("rm -rf temp")
    os.mkdir("temp")
    switch_type = switch_type.lower()
    if not os.path.exists(path_src):
        return "Le fichier source est introuvable"
    if not os.path.exists("templates/" + switch_type):
        return "Ce type de switch n'est pas pris en compte"
    file_name = os.path.basename(path_src)
    file_name = os.path.splitext(file_name)[0]
    file_name = file_name.lower()
    liste_templates = os.listdir("templates/" + switch_type + "/principaux")
    for t in liste_templates:
        template_name = os.path.splitext(t)[0]
        if template_name[1] != ".py":
            parse_result = list()
            titres = list()
            parse_result, titres = p.parse_cisco_command(path_src, "templates/" + switch_type + "/principaux/" + t)
            if type(parse_result).__name__ == 'list' and len(parse_result) > 0:
                if not os.path.exists("results/" + file_name):
                    os.mkdir("results/" + file_name)
                g.Generer_json_file(parse_result, titres, "results/" + file_name, template_name)
                gcf.Generate_json_file_conf2("/parse_elk/results/" + file_name + "/" + template_name + ".json",
                                            "temp", file_name + "_" + template_name, "doc", "l",file_name + "_" + template_name,file_name + "_" + template_name)
                #exe.Execute_conf_file_using_logstash("results/" + file_name + "/" + template_name + ".conf")
    if switch_type == "cisco_nxos":
        file_name = os.path.basename(path_src)
        file_name = os.path.splitext(file_name)[0]
        file_name = file_name.lower()
        parse_result, titres = thk.parse_show_interface_trunk_cisco_nxos(path_src)
        if type(parse_result).__name__ == 'list' and len(parse_result) > 0:
            if not os.path.exists("results/" + file_name):
                os.mkdir("results/" + file_name)
            g.Generer_json_file(parse_result, titres, "results/" + file_name, "show_interfaces_trunk")
            gcf.Generate_json_file_conf2("/parse_elk/results/" + file_name + "/show_interfaces_trunk.json",
                                        "temp", file_name + "_show_interfaces_thrunk", "doc", "l",file_name + "_show_interfaces_thrunk",file_name + "_show_interfaces_thrunk")
           # exe.Execute_conf_file_using_logstash("results/" + file_name + "/show_interfaces_thrunk.conf")
        parse_result, titres = vpc.parse_vpc_status_nxos(path_src)
        if type(parse_result).__name__ == 'list' and len(parse_result) > 0:
            if not os.path.exists("results/" + file_name):
                os.mkdir("results/" + file_name)
            g.Generer_json_file(parse_result, titres, "results/" + file_name, "show_vpc")
            gcf.Generate_json_file_conf2("/parse_elk/results/" + file_name + "/show_vpc.json", "temp",
                                        file_name + "_show_vpc", "doc", "l",file_name + "_show_vpc",file_name + "_show_vpc")
            #exe.Execute_conf_file_using_logstash("results/" + file_name + "/show_vpc.conf")
    exe.Execute_conf_file_using_logstash("'temp/*.conf'")

def parser_fichiers_repertoire(path_repertoire, switch_type):
    # path_repertoire=r""+path_repertoire.encode('utf8')
    #print(switch_type)
    if os.path.exists("temp"):
        os.system("rm -rf temp")
    os.mkdir("temp")
    switch_type = switch_type.lower()
    if not os.path.exists(path_repertoire):
        return "Le repertoire source est introuvable"
    elif not os.path.isdir(path_repertoire):
        return "Le chemin spécifier ne correspond pas celui d'un repertoire"

    if not os.path.exists("templates/" + switch_type):
        return "Ce type de switch n'est pas pris en compte"
    liste_fichiers = os.listdir(path_repertoire)
    liste_templates = os.listdir("templates/" + switch_type + "/principaux")

    for t in liste_templates:
        template_name = os.path.splitext(t)[0]
        if template_name[1] != ".py":
            for f in liste_fichiers:
                file_name = os.path.splitext(f)[0]
                file_name = file_name.lower()
                parse_result = list()
                titres = list()
                parse_result, titres = p.parse_cisco_command(path_repertoire + "/" + f,
                                                             "templates/" + switch_type + "/principaux/" + t)
                if type(parse_result).__name__ == 'list' and len(parse_result) > 0:
                    if not os.path.exists("results/" + file_name):
                        os.mkdir("results/" + file_name)
                    g.Generer_json_file(parse_result, titres, "results/" + file_name, template_name)
                    gcf.Generate_json_file_conf2("/parse_elk/results/" + file_name + "/" + template_name + ".json",
                                                "temp", file_name + "_" + template_name, "doc", "l",file_name + "_" + template_name,file_name + "_" + template_name)
                    #exe.Execute_conf_file_using_logstash("results/" + file_name + "/" + template_name + ".conf")
    if switch_type == "cisco_nxos":
        for f in liste_fichiers:
            file_name = os.path.splitext(f)[0]
            file_name = file_name.lower()
            parse_result, titres = thk.parse_show_interface_trunk_cisco_nxos(path_repertoire + "/" + f)
            if type(parse_result).__name__ == 'list' and len(parse_result) > 0:
                if not os.path.exists("results/" + file_name):
                    os.mkdir("results/" + file_name)
                g.Generer_json_file(parse_result, titres, "results/" + file_name, "show_interfaces_thrunk")
                gcf.Generate_json_file_conf2("/parse_elk/results/" + file_name + "/show_interfaces_thrunk.json",
                                            "temp", file_name + "show_interfaces_trunk", "doc", "l",file_name + "_thrunk",file_name + "_show_interfaces_thrunk")
                #exe.Execute_conf_file_using_logstash("results/" + file_name + "/" + file_name + "show_interfaces_thrunk.conf")
            parse_result, titres = vpc.parse_vpc_status_nxos(path_repertoire + "/" + f)
            if type(parse_result).__name__ == 'list' and len(parse_result) > 0:
                if not os.path.exists("results/" + file_name):
                    os.mkdir("results/" + file_name)
                g.Generer_json_file(parse_result, titres, "results/" + file_name, "show_vpc")
                gcf.Generate_json_file_conf2("/parse_elk/results/" + file_name + "/show_vpc.json",
                            "temp", file_name + "show_vpc", "doc", "l",file_name + "_show_vpc",file_name + "_show_vpc")
                #exe.Execute_conf_file_using_logstash("results/" + file_name + "/show_vpc.conf")

    exe.Execute_conf_file_using_logstash("'temp/*.conf'")
