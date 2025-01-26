from classes.inferences.DicoInferateur import *
from classes.inferences.InferenceTriangle import *
from classes.inferences.Noeud import *


class Inferateur:

    def __init__(self):


        self.dicoInferateur = DicoInferateur()
    
        Noeud.dicoInferateur = self.dicoInferateur
        Inference.dicoInferateur = self.dicoInferateur

    

    def inference(self, terme1, relation, terme2):

        noeudTerme1 = self.dicoInferateur.get_node_by_string(terme1)
        if self.dicoInferateur.get_node_by_string(terme1) is None:
            noeudTerme1 = self.dicoInferateur.create_node(terme1)
        
        noeudTerme2 = self.dicoInferateur.get_node_by_string(terme2)
        if self.dicoInferateur.get_node_by_string(terme2) is None:
            noeudTerme2 = self.dicoInferateur.create_node(terme2)
    

        #si la relation existe déjà dans JDM:
        if noeudTerme2.get_id() in noeudTerme1.get_sortants(relation):
            
            return noeudTerme1.get_sortants(relation)[noeudTerme2.get_id()]
            
        
        else:
            #on récup tous les schémas d'inférence qu'on peut sur cette relation
            schemasInferences = Inference.schemas_inference["triangle"]["all"]
            if (Inference.schemas_inference["triangle"].get(relation) != None):
                schemasInferences += Inference.schemas_inference["triangle"][relation]


            #pour stocker toutes les inférences qu'on a fait, puis pour les afficher par ordre 
            listeTuplesInference = []

            for schema in schemasInferences:
                #inférence triangle qui s'occupe de tout faire (on stocke pas l'objet mais on pourrait le faire)
                listeTuplesInference += InferenceTriangle(noeudTerme1, relation, noeudTerme2, schema).get_tuples_inference_triangles()


            if listeTuplesInference:

                listeTuplesInference.sort(key=lambda x: x.get_poids_inference(), reverse=True)
                
                scoreOui = 0
                scoreNon = 0
                compteurTotal = 0
                compteurOui = 0

                for inference in listeTuplesInference:
                    compteurTotal += 1

                    if inference.get_poids_inference()>0:
                        compteurOui += 1
                        scoreOui += inference.get_poids_inference()

                    else:
                        scoreNon += inference.get_poids_inference()
                

                if compteurOui / compteurTotal > 0.55:
                    return scoreOui
                elif compteurOui / compteurTotal < 0.45:
                    return scoreNon
                
                #incertain
                else:
                    return 0
            
            #y a pas eu d'inférence, c'est incertain
            else: 
                return 0