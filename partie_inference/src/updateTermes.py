# fonction pour update les fichiers exploitables (pas avoir à manuellement effacer tous les fichiers etc)

"""
les fichiers .txt téléchargés sur jeuxDeMots n'ont pas besoin (en général) d'être re-téléchargés.
Ce fichier sert juste à retraité tous les fichiers .txt en fichiers json exploitables
(s'il y a bcp de fichiers calcul peut être long et coûteux !!!!)

"""

import chargerDonnees
import os
import json


def supprimer_contenu_repertoire_traite(repertoire):
    for element in os.listdir(repertoire):
        
        chemin_element = os.path.join(repertoire, element)
        os.remove(chemin_element)
    print("tous les fichiers sont supprimés du répertoire Traite")
            


def supprimer_contenu_repertoire_exploitable(repertoire):
    for element in os.listdir(repertoire):
        chemin_element = os.path.join(repertoire, element)
        if os.path.isdir(chemin_element):
            supprimer_contenu_repertoire_exploitable(chemin_element)
            # Supprimer le dossier vide une fois qu'il est vidé
            os.rmdir(chemin_element)
        if os.path.isfile(chemin_element):
                os.remove(chemin_element)
    
                




#on crée les répertoires "res/fichiersBruts" et "res/fichiersExploitables" prck je sais pas pk git veut pas les mettre


if not os.path.exists("res/fichiersBruts"):
    os.makedirs("res/fichiersBruts")

if not os.path.exists("res/fichiersExploitables"):
    os.makedirs("res/fichiersExploitables")

if not os.path.exists("res/fichiersTraites"):
    os.makedirs("res/fichiersTraites")

if not os.path.exists("res/infoNoeuds"):
    os.makedirs("res/infoNoeuds")


# Utilisation de la fonction pour vider un répertoire

supprimer_contenu_repertoire_traite("res/fichiersTraites")
supprimer_contenu_repertoire_exploitable("res/fichiersExploitables")
print("tous les fichiers du dossier Exploitable sont supprimés")



with open("res/infoNoeuds/relationsParTerme.json", 'w') as f:
    f.write("{}")






"""
#je recrée le fichier rt.json et nt.json exploitables
dico = rtjson_vers_rtExploitable("res/fichiersTraites/rt.json")
dicoJson = json.dumps(dico, indent=4)

with open("res/fichiersExploitables/rt.json", 'w') as fichier:
    fichier.write(dicoJson)
    print("fichier enregistré")

dico = rtjson_vers_rtExploitable("res/fichiersTraites/rt.json")
dicoJson = json.dumps(dico, indent=4)

#bon tant pis pour le nt.json mais en vrai on s'en sert pas trop donc bon
"""







#mtn qu'on a tout supprimé, on recrée tout tout tout (ça peut être lourd niveau mémoire, je verrai bien)

with open("res/infoNoeuds/rt.json", 'r') as fichier:
    relations_types = json.load(fichier)


for element in os.listdir("res/fichiersBruts"):
    if "r_hypo" not in element:
        chargerDonnees.recup_exploitable(element[0:element.find(".txt")])