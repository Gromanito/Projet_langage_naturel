"""

 main du projet

s'occupe de récupérer les entrées utilisateurs et d'appeler les bons objets pour faire les inférences

"""


from classes.DicoInferateur import *
from classes.Inference import *
from classes.InferenceTriangle import *
from classes.Noeud import *

import json
import time 
import os



#pour savoir quelles sont les relations existantes
with open("res/infoNoeuds/rt.json", 'r') as fichier:
    rtJSON = json.load(fichier)



def recup_user_input():

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


        userInput = [terme1, relation, terme2]
        

        global rtJSON
        if relation not in rtJSON:
            print("la relation \"" + relation + "\" n'existe pas")
        
        
        return userInput

            


def jouer():
#fonction principale

    print("Bienvenue sur un programme qui fait des inférences!\n\n")
    
    dicoInferateur = DicoInferateur()
    
    Noeud.dicoInferateur = dicoInferateur
    Inference.dicoInferateur = dicoInferateur



    #boucle infinie, on peut demander autant d'inférences que l'on veut
    #le programme s'arrête quand l'utilisateur rentre "exit"
    while True:
        userInput = recup_user_input()
        terme1, rt, terme2 = userInput[0], userInput[1], userInput[2]


        #on récupère les noeuds dont on a besoin. S'ils n'existent pas, on les crée (et potentiellement télécharge sur JDM)
        noeudTerme1 = dicoInferateur.get_node_by_string(terme1)
        if dicoInferateur.get_node_by_string(terme1) is None:
            noeudTerme1 = dicoInferateur.create_node(terme1)
        
        noeudTerme2 = dicoInferateur.get_node_by_string(terme2)
        if dicoInferateur.get_node_by_string(terme2) is None:
            noeudTerme2 = dicoInferateur.create_node(terme2)
        
    

        #on a récupéré les données, mtn on fait les inférences

        print("\n\n")


        #inférence directe, on regarde si la relation existe dans JDM
        if noeudTerme2.get_id() in noeudTerme1.get_sortants(rt):
            print("la relation existe dans JDM !")
            print("\n")
            print(terme1 + " " + rt + " " + terme2 + " | " + str(noeudTerme1.get_sortants(rt)[noeudTerme2.get_id()]) )
            
        else:
            print("la relation n'existe pas dans JDM")

        print("\n\n")


        #on fait d'abord les inférences triangles

        #on récup tous les schémas d'inférence qu'on peut sur cette relation
        schemasInferences = Inference.schemas_inference["triangle"]["all"]
        if (Inference.schemas_inference["triangle"].get(rt) != None):
            schemasInferences += Inference.schemas_inference["triangle"][rt]


        #pour stocker toutes les inférences qu'on a fait, puis pour les afficher par ordre 
        listeTuplesInference = []

        for schema in schemasInferences:
            #inférence triangle qui s'occupe de tout faire (on stocke pas l'objet mais on pourrait le faire)
            listeTuplesInference += InferenceTriangle(noeudTerme1, rt, noeudTerme2, schema).get_tuples_inference_triangles()

        listeTuplesInference.sort(key=lambda x: x.get_poids_inference(), reverse=True)
        
        for inference in listeTuplesInference:
            inference.print_inference_propre()

        print("\n\n")




        #TODO: faire les inférences carrées (pas envie)





jouer()


        
