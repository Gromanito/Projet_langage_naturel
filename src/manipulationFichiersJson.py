""" fichier temporaire"""


"""on récupère les fichiers traites rt et nd et on les réenregistre en json de sorte 
à ce qu'on obtienne un dico

"nt":id

"""


import json

def rtjson_vers_dictionnaire_nom_rtid(nomFichier):
    # Charger le JSON
    with open(nomFichier, 'r') as fichier:
        objet_json = json.load(fichier)
    
    # Initialiser le dictionnaire résultant
    dictionnaire_nom_rtid = {}
    
    # Parcourir chaque élément de la liste JSON
    for element in objet_json:
        rtid = int(element["rtid"])
        name = element["name"]
        dictionnaire_nom_rtid[name] = rtid
    
    return dictionnaire_nom_rtid

"""
dico = rtjson_vers_dictionnaire_nom_rtid("res/fichiersTraitesJson/rt.json")
dicoJson = json.dumps(dico, indent=4)

with open("res/fichiersExploitables/rt.json", 'w') as fichier:
			fichier.write(dicoJson)
			print("fichier enregistré")
"""



def ntjson_vers_dictionnaire_nom_ntid(nomFichier):
    # Charger le JSON
    with open(nomFichier, 'r') as fichier:
        objet_json = json.load(fichier)
    
    # Initialiser le dictionnaire résultant
    dictionnaire_nom_rtid = {}
    
    # Parcourir chaque élément de la liste JSON
    for element in objet_json:
        rtid = int(element["ntid"])
        name = element["name"]
        dictionnaire_nom_rtid[name] = rtid
    
    return dictionnaire_nom_rtid


dico = ntjson_vers_dictionnaire_nom_ntid("res/fichiersTraitesJson/nt.json")
dicoJson = json.dumps(dico, indent=4)

with open("res/fichiersExploitables/nt.json", 'w') as fichier:
			fichier.write(dicoJson)
			print("fichier enregistré")