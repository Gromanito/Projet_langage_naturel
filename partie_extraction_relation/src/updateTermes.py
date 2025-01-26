# fonction pour update les fichiers exploitables (pas avoir à manuellement effacer tous les fichiers etc)

"""
les fichiers .txt téléchargés sur jeuxDeMots n'ont pas besoin (en général) d'être re-téléchargés.
Ce fichier sert juste à retraité tous les fichiers .txt en fichiers json exploitables
(s'il y a bcp de fichiers calcul peut être long et coûteux !!!!)

"""

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
    
                






# Utilisation de la fonction pour vider un répertoire

supprimer_contenu_repertoire_traite("noeudsJDM/fichiersTraites")
supprimer_contenu_repertoire_exploitable("noeudsJDM/fichiersExploitables")











