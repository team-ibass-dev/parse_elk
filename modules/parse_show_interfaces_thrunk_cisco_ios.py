import os
import re
from modules import extraire_une_partie_de_liste as ext


def parse_show_interface_trunk_cisco_ios(path_src_file):
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

    tab1 = ext.Extraire_une_partie_de_liste(contenu_,r"^Port[ ]+Mode[ ]+Encapsulation[ ]+Status[ ]+Native[ ]{1}vlan$",r"Port[ ]+Vlans[ ]{1}allowed[ ]{1}on[ ]{1}trunk$")
    taille = len(tab1)
    tab2 = ext.Extraire_une_partie_de_liste(contenu_,r"^Port[ ]+[Vv]{1}lans[ ]{1}allowed[ ]{1}on[ ]{1}trunk$",r"^Port[ ]+[Vv]{1}lans[ ]{1}allowed[ ]{1}on[ ]{1}trunk$")
    tab3 = ext.Extraire_une_partie_de_liste(contenu_,r"^[Pp]{1}ort[ ]+[Vv]{1}lans[ ]{1}allowed and active in management domain",r"^[Pp]{1}ort[ ]+[Vv]{1}lans in spanning tree forwarding state and not pruned")
    tab4 = ext.Extraire_une_partie_de_liste2(contenu_,r"^[Pp]{1}ort[ ]+[Vv]{1}lans in spanning tree forwarding state and not pruned",taille)

    tab2 = Completer_tableau(tab2, taille)
    tab3 = Completer_tableau(tab3, taille)
    tab4 = Completer_tableau(tab4, taille)

    # données du tableau 1
    port = list()
    mode = list()
    Encapsulation = list()
    Status = list()
    native_vlan = list()
    # données du tableau 2
    vlan_allowed2 = list()
    # données du tableau 3
    vlan_allowed3 = list()
    # données du tableau 4
    vlan_allowed4 = list()

    # remplir les listes du tableau 1
    for x in tab1:
        liste_donnees = ' '.join(x.split())
        liste_donnees = liste_donnees.split()

        port.append(liste_donnees[0])
        mode.append(liste_donnees[1])
        Encapsulation.append(liste_donnees[2])
        Status.append(liste_donnees[3])
        native_vlan.append(liste_donnees[4])

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

    liste_def = list()
    p = 0
    while p < len(port):
        temp = list()
        temp.append(port[p])
        temp.append(mode[p])
        temp.append(Encapsulation[p])
        temp.append(Status[p])
        temp.append(native_vlan[p])
        temp.append(vlan_allowed2[p].split(","))
        temp.append(vlan_allowed3[p].split(","))
        temp.append(vlan_allowed4[p].split(","))
        liste_def.append(temp)
        p = p + 1
    liste_titre = ["port", "mode", "Encapsulation", "Status", "Native_vlan", "Vlans_allowed_on_trunk",
                   "Vlans_allowed_active_management_domain", "Vlans_in_spanning_tree_forwarding_state_not_pruned"]
    return liste_def, liste_titre


def Completer_tableau(tab, taille_normale):
    if len(tab) < taille_normale:
        d = taille_normale - len(tab)
        while d > 0:
            tab.append("port none")
            d = d - 1
    return tab