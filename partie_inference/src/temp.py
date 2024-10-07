import chargerDonnees
import os
import json

def supprimer_contenu_repertoire_exploitable(repertoire):
    for element in os.listdir(repertoire):
        chemin_element = os.path.join(repertoire, element)
        if os.path.isdir(chemin_element):
            supprimer_contenu_repertoire_exploitable(chemin_element)
            # Supprimer le dossier vide une fois qu'il est vidé
            os.rmdir(chemin_element)
        if os.path.isfile(chemin_element):
                os.remove(chemin_element)


supprimer_contenu_repertoire_exploitable("res/fichiersExploitables")




with open("res/infoNoeuds/relationsParTerme.json", 'w') as f:
    f.write("{}")

chargerDonnees.recup_exploitable("mijoter")



