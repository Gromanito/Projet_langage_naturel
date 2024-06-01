# fonction pour update les fichiers exploitables (pas avoir à manuellement effacer tous les fichiers etc)

"""
les fichiers .txt téléchargés sur jeuxDeMots n'ont pas besoin (en général) d'être re-téléchargés.
Ce fichier sert juste à retraité tous les fichiers .txt en fichiers json exploitables
(s'il y a bcp de fichiers calcul peut être long et coûteux !!!!)

"""

import recupDonnees
import os
import json


def supprimer_contenu_repertoire_traite(repertoire):
    for element in os.listdir(repertoire):
        
        if element != "rt.json" and element != "nt.json":

            chemin_element = os.path.join(repertoire, element)
            # Si c'est un fichier, le supprimer

            if os.path.isfile(chemin_element):
                os.remove(chemin_element)
                print(f"Fichier supprimé : {chemin_element}")
            


def supprimer_contenu_repertoire_exploitable(repertoire):
    for element in os.listdir(repertoire):
        chemin_element = os.path.join(repertoire, element)
        if os.path.isdir(chemin_element):
            supprimer_contenu_repertoire_exploitable(chemin_element)
            # Supprimer le dossier vide une fois qu'il est vidé
            os.rmdir(chemin_element)
            print(f"Dossier supprimé : {chemin_element}")
        if os.path.isfile(chemin_element):
                os.remove(chemin_element)
                print(f"Fichier supprimé : {chemin_element}")





def rtjson_vers_rtExploitable(nomFichier):
    # Charger le JSON traité
    with open(nomFichier, 'r') as fichier:
        objet_json = json.load(fichier)
    
    # Initialiser le dictionnaire résultant
    dictionnaireRT = {}
    
    # Parcourir chaque élément de la liste JSON
    for element in objet_json:
        rtid = int(element["rtid"])
        name = element["name"]
        dictionnaireRT[name] = rtid
        dictionnaireRT[rtid] = name
    
    return dictionnaireRT





# Utilisation de la fonction pour vider un répertoire

supprimer_contenu_repertoire_traite("res/fichiersTraites")
supprimer_contenu_repertoire_exploitable("res/fichiersExploitables")



with open("res/fichiersTraites/relationsParTerme.json", 'w') as f:
    f.write("{}")







#je recrée le fichier rt.json et nt.json exploitables
dico = rtjson_vers_rtExploitable("res/fichiersTraites/rt.json")
dicoJson = json.dumps(dico, indent=4)

with open("res/fichiersExploitables/rt.json", 'w') as fichier:
    fichier.write(dicoJson)
    print("fichier enregistré")

dico = rtjson_vers_rtExploitable("res/fichiersTraites/rt.json")
dicoJson = json.dumps(dico, indent=4)

#bon tant pis pour le nt.json mais en vrai on s'en sert pas trop donc bon








#mtn qu'on a tout supprimé, on recrée tout tout tout (ça peut être lourd niveau mémoire, je verrai bien)

with open("res/fichiersExploitables/rt.json", 'r') as fichier:
    relations_types = json.load(fichier)


for element in os.listdir("res/fichiersBruts"):
    if "r_hypo" not in element:
        recupDonnees.recupExploitable(element[0:element.find(".txt")], relations_types)