"""programme pour faire des inférences, jspTrop"""

import traitementJson
import recupDonnees
import inferences
import json



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

            

        


def prepareEtRecupereLesDonneesExploitables(terme:str, dicoEdges:dict, dicoRelationsDesTermes:dict) -> dict:

    chaineBruteTerme = recupDonnees.takeRawData(terme)
    
    if chaineBruteTerme == "EchecRequete":
        print("problème lors de la requête internet (avez vous bien écrit les termes?)")
        return False

    dico = traitementJson.enregistrer_en_json(terme, chaineBruteTerme)
    traitementJson.json_vers_exploitable(terme, dico)
    
    
    dicoRelationsDesTermes[terme] = recupDonnees.recupExploitable(terme, dicoEdges)

    return True


def jouer():

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

        
        
        terme1aEteRecup = prepareEtRecupereLesDonneesExploitables(elements[0], dicoEdges, dicoRelationsDesTermes)
        relation = relation_types.get(elements[1])
        terme2aEteRecup = prepareEtRecupereLesDonneesExploitables(elements[2], dicoEdges, dicoRelationsDesTermes)
        

        ttSestBienPasse = terme1aEteRecup and \
                          terme2aEteRecup and \
                          relation is not None


        if not ttSestBienPasse:
            print("problème lors de la récupération des données.\n(Avez vous bien écrit vos termes?)")
            continue
        
        else:
            terme1, terme2, typeRelation = elements[0], elements[2], elements[1]

        
            inferences.inference_deductive(terme1, dicoRelationsDesTermes[terme1], typeRelation, terme2, dicoRelationsDesTermes[terme2], dicoEdges )
            
            if typeRelation == "r_lieu" or typeRelation == "r_has_part" or typeRelation == "r_lieu-1":
                inferences.inference_transitive(terme1, dicoRelationsDesTermes[terme1], typeRelation, terme2, dicoRelationsDesTermes[terme2], dicoEdges )

            




jouer()


        
