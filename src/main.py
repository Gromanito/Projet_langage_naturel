"""programme pour faire des inférences, jspTrop"""

import traitementJson
import recupDonnees
import inferences
import json
import time 
import os




def recup_input_user(rtJSON):

    #bon j'aime pas trop les boucles infinies mais j'ai la flemme de faire autrement
    while True:
        print("\n\n")
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
        
        if relation not in rtJSON:
            print("la relation \"" + relation + "\" n'existe pas")
        
        
        return elements

            


def jouer():

    global relationsTransitives

    print("Bienvenue sur un programme qui fait des inférences!\n\n")

    dicoPrincipal = {"noeuds":{}, "relationsDesTermes":{}}
    

    #on récup les types de relation et de noeud
    with  open("res/fichiersExploitables/rt.json") as fichier:
        relation_types = json.load(fichier)

    

    #boucle infinie, on peut demander autant d'inférences que l'on veut
    #le programme s'arrête quand l'utilisateur rentre "exit"
    while True:
        elements = recup_input_user(relation_types)
        terme1, terme2, typeRelation = elements[0], elements[2], elements[1]

        if dicoPrincipal["relationsDesTermes"].get(terme1) is None:
            terme1aEteRecup = recupDonnees.prepareEtRecupereLesDonneesExploitables(terme1, dicoPrincipal, relation_types)

        relation = relation_types.get(elements[1])

        if dicoPrincipal["relationsDesTermes"].get(terme2) is None:
            terme2aEteRecup = recupDonnees.prepareEtRecupereLesDonneesExploitables(terme2, dicoPrincipal, relation_types)
        

        ttSestBienPasse = terme1aEteRecup and \
                          terme2aEteRecup and \
                          relation is not None


        if not ttSestBienPasse:
            continue
        
        
        else:

            
            #on regarde déjà si la relation est connue dans la base de connaissance
            idTerme2 = dicoPrincipal["relationsDesTermes"][terme2]["id"]

            if dicoPrincipal["relationsDesTermes"][terme1][elements[1]]["sortant"].get(idTerme2) is None:
                print("\nla relation n'existe pas dans la base de connaissance\n")
            else:
                print("\nla relation existe dans la base de connaissance ! (poids: " + str(dicoPrincipal["relationsDesTermes"][terme1][elements[1]]["sortant"][idTerme2]["weight"]) + ")")



            inferences.inference_generique_triangle(terme1, typeRelation, terme2, dicoPrincipal )
            
            inferences.inference_generique_carre(terme1, typeRelation, terme2, dicoPrincipal)


            print("\n\n")
            




jouer()


        
