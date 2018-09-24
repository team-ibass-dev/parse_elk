# -*- coding:utf-8 -*-

import os
import argparse
from modules import app
from modules import parse_show_interfaces_thrunk_cisco_ios as par

def main():

    parse = argparse.ArgumentParser("parse_elk",description="Améliorer le traitement de vos résultats")
    parse.add_argument("-d","--directory",required=True,type=str,help="Permet d'entrer le chemin à traiter ou vers le fichier a traiter",)
    parse.add_argument("-a","--action",required=True,type=str,choices=["cte","jte","pcte","pste","alte"],help="Permet d'entrer l'action que vous souhaiter éffectuée \n 'cte = csv to elk (fichiers csv vers elasticsearch) 'jte = json to elk (fichiers json vers elasticsearch) 'pcte = pcap to elk (fichiers pcap vers elasticsearch) 'pste = parse to elk (fichier à parser vers elasticsearch)")
    parse.add_argument("-s","--switch",type=str,choices=["cisco_nxos","cisco_ios"],help="entrer le type de switch donc vous souhaiter traiter les résultats" )
    parse.add_argument("-i","--index",type=str,help="Permet d'entrer le nom de l'index que vous souhaiter créer si un seul devra être créé")

    args=parse.parse_args()

    if os.path.isdir(args.directory):
        app.action(directory=args.directory,action=args.action,index=args.index,switch=args.switch,type_input="dir")
    elif os.path.isfile(args.directory):
        app.action(directory=args.directory,action=args.action,index=args.index,switch=args.switch,type_input="file")
    else:
        print("le chemin passé en argument n'existe pas")



if __name__ == '__main__':
    main()
    # res,ti=par.parse_show_interface_trunk_cisco_ios("/media/marius/Nouveau nom/example2ios/ios-3750.log")
    # for r in res:
    #     print(r)