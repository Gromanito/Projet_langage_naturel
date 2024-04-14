"""programme pour faire des inférences, jspTrop"""

import traitementJson
import recupDonnees
import inferences
import json
import time 
import os


relationsTransitives = ["r_has_part", "r_holo", "r_syn", "r_lieu", "r_lieu-1"]

# UTILISATION : mettre @timing comme annotation d'une fonction
def timing(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        print("Durée d'exécution : {:1.3}s".format(end_time - start_time))
    return wrapper



def recup_input_user():

    #bon j'aime pas trop les boucles infinies mais j'ai la flemme de faire autrement
    while True:
        entree = input("Veuillez entrer trois éléments séparés par des espaces ('exit' pour quitter) : ").strip()
        
        # Vérifier si l'utilisateur veut quitter le programme
        if entree.lower() == "exit":
            print("Au revoir")
            exit()
        
        
        indiceRelation = entree.find("r_")

        if indiceRelation < 0:
            print("Veuillez indiquer une relation correcte")
            continue
            
        terme1 = entree[ 0 :indiceRelation-1]
        relation = entree[indiceRelation:].split()[0]
        terme2 = entree[indiceRelation + len(relation)+1:]


        elements = [terme1, relation, terme2]
        
        
        
        return elements

            

        


def prepareEtRecupereLesDonneesExploitables(terme:str, dicoEdges:dict, dicoRelationsDesTermes:dict, relation_types=None) -> dict:

    # fonction qui récupère les données des fichiers json pour les intégrer au programme
    # (récupère les données depuis internet si besoin)


    filePath = "res/fichiersExploitables/"+terme+"/"


    if os.path.exists(filePath):
        #les fichiers exploitables existent déjà, on a plus qu'à les charger
        with  open(filePath + "e.json") as fichier:
            nodesTerme = json.load(fichier)
        with  open(filePath + "r.json") as fichier:
            relationsTerme = json.load(fichier)

    else:
        # les fichiers exploitables n'existent pas, on le crée

        if relation_types == None:
            with open("res/fichiersExploitables/rt.json", 'r') as fichier:
                relation_types = json.load(fichier)


        #on récup les fichiers bruts depuis internet
        chaineBruteTerme = recupDonnees.takeRawData(terme, relation_types)
        chaineBruteHypo = recupDonnees.takeRawData(terme, relation_types, "r_hypo")
        

        #s'il y a des problèmes lors de la récupération des données, on annule
        if chaineBruteTerme == "EchecRequete" or chaineBruteHypo == "EchecRequete":
            print("problème lors de la requête internet")
            return False
        
        if chaineBruteTerme == "TermeExistePas":
            return False


        #on transforme le fichier brut en json
        traitementJson.enregistrer_en_json(terme, chaineBruteTerme)

        #on ajoute la relation r_hypo qui n'est pas chargé par défaut sur la page principale
        dico = traitementJson.ajouterRelationsAuJsonTraite(terme, "r_hypo")

        nodesTerme, relationsTerme = traitementJson.json_vers_exploitable(terme, dico, relation_types)
        
    
    
    #on a récup les données, maintenant on les "stocke" dans notre programme
    idTerme = nodesTerme.pop("id")


    #on rajoute les noeuds
    for key, value in nodesTerme.items() :
        dicoEdges[key] = value
    
    #on rajoute les relations
    relationsTerme["id"] = idTerme
    dicoRelationsDesTermes[terme] = relationsTerme

    return True
    


def jouer():

    global relationsTransitives

    print("Bienvenue sur Super Inferator!\n\n")

    dicoEdges = {}
    dicoRelationsDesTermes = {}

    #on récup les types de relation et de noeud
    with  open("res/fichiersExploitables/rt.json") as fichier:
        relation_types = json.load(fichier)

    

    #boucle infinie, on peut demander autant d'inférences que l'on veut
    #le programme s'arrête quand l'utilisateur rentre "exit"
    while True:
        elements = recup_input_user()
        terme1, terme2, typeRelation = elements[0], elements[2], elements[1]

        if dicoRelationsDesTermes.get(terme1) is None:
            terme1aEteRecup = prepareEtRecupereLesDonneesExploitables(elements[0], dicoEdges, dicoRelationsDesTermes, relation_types)

        relation = relation_types.get(elements[1])

        if dicoRelationsDesTermes.get(terme2) is None:
            terme2aEteRecup = prepareEtRecupereLesDonneesExploitables(elements[2], dicoEdges, dicoRelationsDesTermes, relation_types)
        

        ttSestBienPasse = terme1aEteRecup and \
                          terme2aEteRecup and \
                          relation is not None


        if not ttSestBienPasse:
            continue
        
        
        else:
            inferences.inference_deductive(terme1, dicoRelationsDesTermes[terme1], typeRelation, terme2, dicoRelationsDesTermes[terme2], dicoEdges )
            inferences.inference_deductive_inversee(terme1, dicoRelationsDesTermes[terme1], typeRelation, terme2, dicoRelationsDesTermes[terme2], dicoEdges )
            inferences.inference_inductive(terme1, dicoRelationsDesTermes[terme1], typeRelation, terme2, dicoRelationsDesTermes[terme2], dicoEdges )
            

            if typeRelation in relationsTransitives:
                inferences.inference_transitive(terme1, dicoRelationsDesTermes[terme1], typeRelation, terme2, dicoRelationsDesTermes[terme2], dicoEdges )


            print("\n\n")
            




jouer()


        
