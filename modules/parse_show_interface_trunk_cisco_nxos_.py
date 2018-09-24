# coding:utf8
'''
Created on 12 sept. 2018

@author: marius
'''
import os
import re
from modules import extraire_une_partie_de_liste as ext


def parse_show_interface_trunk_cisco_nxos(path_src_file):
    # path_src_file=r""+path_src_file.decode('utf8').encode('utf8')
    print(path_src_file)
    if not os.path.exists(path_src_file):
        return "Le fichier source est introuvable"
    elif not os.path.isfile(path_src_file):
        return "Le chemin indiqué ne correspond pas à celui d'un fichier !"

    # lecture du contenu du fichier
    fichier = open(path_src_file, "r")
    contenu = fichier.readlines()
    fichier.close()

    # Suppression des lignes vides et des ligne inutiles
    contenu_ = list()
    for x in contenu:
        if re.match("^\s$$", x) is None and re.match("^-", x) is None:
            contenu_.append(x)

    tab1 = ext.Extraire_une_partie_de_liste(contenu_, r"^\s{10}\s*[VLANvlan]{4}\s{10}\s*[CHANNELchannel]{7}$",
                                            r"^[PORTport]{4}\s{5}\s*[VLANSvlans]{5}\s[ALLOWEDallowed]{7}\s[ONon]{2}\s[trunkTRUNK]{5}$")
    taille = len(tab1)
    tab2 = ext.Extraire_une_partie_de_liste(contenu_,
                                            r"^[PORTport]{4}\s{5}\s*[VLANSvlans]{5}\s[ALLOWEDallowed]{7}\s[ONon]{2}\s[trunkTRUNK]{5}$",
                                            r"^Port\s*Vlans\sErr-disabled\son\sTrunk$")
    tab3 = ext.Extraire_une_partie_de_liste(contenu_, r"^Port\s*Vlans\sErr-disabled\son\sTrunk$",
                                            r"^Port\s*STP\sForwarding$")
    tab4 = ext.Extraire_une_partie_de_liste(contenu_, r"^Port\s*STP\sForwarding$",
                                            r"^Port\s*Vlans\sin\sspanning\stree\sforwarding\sstate\sand\snot\spruned$")
    tab5 = ext.Extraire_une_partie_de_liste(contenu_,
                                            r"^Port\s*Vlans\sin\sspanning\stree\sforwarding\sstate\sand\snot\spruned$",
                                            r"^Port\s*Vlans\sForwarding\son\sFabricPath$")
    tab6 = ext.Extraire_une_partie_de_liste2(contenu_, r"^Port\s*Vlans\sForwarding\son\sFabricPath$", taille)
    tab2 = Completer_tableau(tab2, taille)
    tab3 = Completer_tableau(tab3, taille)
    tab4 = Completer_tableau(tab4, taille)
    tab5 = Completer_tableau(tab5, taille)
    tab6 = Completer_tableau(tab6, taille)
    # print(tab5)

    # données du tableau 1
    port = list()
    native_vl = list()
    stat = list()
    port_channel = list()
    # données du tableau 2
    vlan_allowed2 = list()
    # données du tableau 3
    vlan_allowed3 = list()
    # données du tableau 4
    vlan_allowed4 = list()
    # données du tableau 5
    vlan_allowed5 = list()
    # données du tableau 6
    vlan_allowed6 = list()

    # remplir les listes du tableau 1
    for x in tab1:
        liste_donnees = ' '.join(x.split())
        liste_donnees = liste_donnees.split()
        port.append(liste_donnees[0])
        native_vl.append(liste_donnees[1])
        stat.append(liste_donnees[2])
        port_channel.append(liste_donnees[3])
    # remplir les listes du tableau 2
    for x in tab2:
        liste_donnees = ' '.join(x.split())
        liste_donnees = liste_donnees.split()
        vlan_allowed2.append(liste_donnees[1])

    # remplir les listes du tableau 3
    for x in tab3:
        liste_donnees = ' '.join(x.split())
        liste_donnees = liste_donnees.split()
        vlan_allowed3.append(liste_donnees[1])

    # remplir les listes du tableau 4
    for x in tab4:
        liste_donnees = ' '.join(x.split())
        liste_donnees = liste_donnees.split()
        vlan_allowed4.append(liste_donnees[1])

    # remplir les listes du tableau 5
    for x in tab5:
        liste_donnees = ' '.join(x.split())
        liste_donnees = liste_donnees.split()
        if len(liste_donnees) == 2:
            vlan_allowed5.append(liste_donnees[1])

    # remplir les listes du tableau 6
    for x in tab6:
        liste_donnees = ' '.join(x.split())
        liste_donnees = liste_donnees.split()
        vlan_allowed6.append(liste_donnees[1])

    liste_def = list()
    p = 0
    while p < len(port):
        temp = list()
        temp.append(port[p])
        temp.append(native_vl[p])
        temp.append(stat[p])
        temp.append(port_channel[p])
        temp.append(vlan_allowed2[p].split(","))
        temp.append(vlan_allowed3[p].split(","))
        temp.append(vlan_allowed4[p].split(","))
        try:
            temp.append(vlan_allowed5[p].split(","))
        except:
            pass
        try:
            temp.append(vlan_allowed6[p].split(","))
        except:
            pass
        liste_def.append(temp)
        p = p + 1

    liste_titre = ["port", "native_vlan", "status", "port_channel", "vlans_allowed_trunk", "vlans_err-disabled_trunk",
                   "stp_forwarding", "vlans_in_spanning_tree_forwarding_state_and_not_pruned",
                   "vlans_forwarding_on_fabricPath"]
    return liste_def, liste_titre


def Completer_tableau(tab, taille_normale):
    if len(tab) < taille_normale:
        d = taille_normale - len(tab)
        while d > 0:
            tab.append("port none")
            d = d - 1
    return tab





