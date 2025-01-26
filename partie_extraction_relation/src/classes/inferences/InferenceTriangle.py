from classes.inferences.Inference import *
from classes.inferences.TupleInferenceTriangle import *

class InferenceTriangle(Inference):



    def __init__(self, A, rt, B, schema):

        #récupère le nombre d'inf, tout ce que concerne l'inférence, et d'autres trucs sympathique tkt
        Inference.__init__(self, A, rt, B, schema)


        ligneC = schema["C"].split(';')
        self.sourceIntermediaire = A if ligneC[0] == 'A' else B
        self.relationInt = ligneC[1]
        if self.relationInt == "rt":
            self.relationInt = self.relation

        
        self.intermediairesC = self.sourceIntermediaire.get_sortants(self.relationInt, poidsNegatifs=False)
        
        ligneScore = schema["score"].split(";")
        self.metaPoidsRelationIntermediaire = float(ligneScore[0])
        self.metaPoidsRelationInference = float(ligneScore[1])

        


        #on calcul les inférences
        self.calcul_inf()


        #on les affiche
        #self.print_inferences()
    



    def calcul_inf(self):

        #bon attention à ces lignes là, normalement ça marche mais si à gauche y a "C",  gaucheTerme=B (alors que non)
        elements_inference = {}
        gaucheTerme = self.A if self.gaucheInf == "A" else self.B
        droiteTerme = self.A if self.droiteInf == "A" else self.B
        relationInferenceFonction = self.relationInf


        #si on a eu des intermédiaires (y a matière à faire des inférences)
        if self.intermediairesC is not None:


            
            
            yAunConversif = Inference.conversifs.get(self.relationInf) is not None

            # le cas simple est le cas où on a  A rt C, prck on a qu'à prendre les sortants de A
            
            # mais si on a   C rt A,   il faut prendre les sortants de C (chiant prck il faut télécharger)
            # ou alors on prend les entrants de A,  ou les sortants de A par le conversif, 
            # (et donc ça revient à faire A rt-1 C),  cas qu'on traitera + tard


            #cas pas simple
            #on cherche des chemins de C vers le truc à droite
            #on regarde d'abord les entrants sur le truc à droite (pour pas avoir à télécharger des trucs depuis C)
            if self.gaucheInf == 'C':

                elements_inference.update(droiteTerme.get_entrants(self.relationInf))
                #on teste les sortants mais sur le conversif
                if yAunConversif:
                    relationInferenceFonction = Inference.conversifs[relationInferenceFonction]
                    gaucheTerme, droiteTerme = droiteTerme, gaucheTerme

                    elements_inference.update(gaucheTerme.get_sortants(relationInferenceFonction))


                # cas chiant où on a rien depuis A ou B, il faut envisager de télécharger tous les intermédiaires et de voir si y aura pas plus d'info
                else:
                    #pour l'instant je return juste, je verrai plus tard si je les télécharge vraiment ou si juste je dis que ça a rien trouvé
                    return

                    #TODO : télécharger (efficacement...) les noeuds intermédiaires et générer les tuples à partir d'eux
            
            
            else:
                elements_inference.update(gaucheTerme.get_sortants(relationInferenceFonction))




        # print(elements_inference)
            

        
        #on a les termes qui seraient bien pour les inférences, on regarde si ce sont aussi des intermédiaires
        
        #on regarde d'abord si on a trouvé de quoi faire des inférences
        if elements_inference:
            tousLesIntermediaires = self.intermediairesC.keys()

            #pour l'affichage on prend direct les string, pas les objets
            if self.gaucheInf == "A":
                gauche = self.A.get_string()
            elif self.gaucheInf == "B":
                gauche = self.B.get_string()

            if self.droiteInf == "A":
                droite = self.A.get_string()
            elif self.droiteInf == "B":
                droite = self.B.get_string()

           
            #pour chaque terme pour lequel l'inférence est possible, on regarde s'il est bien un intermédiaire
            for termeIdInference, poids in elements_inference.items():
                if termeIdInference in tousLesIntermediaires:

                    
                    #pour l'affichage on prend direct les string, pas les objets
                    if self.gaucheInf == "C":
                        gauche = Inference.dicoInferateur.get_terme_by_id(termeIdInference)["n"]
                    if self.droiteInf == "C":
                        droite = Inference.dicoInferateur.get_terme_by_id(termeIdInference)["n"]

                    


                    #on stocke tous les tuples inférences (pour pouvoir les comparer entre eux + tard)
                    self.listeTuplesInference.append(TupleInferenceTriangle(sourceIntermediaire = self.sourceIntermediaire.get_string() , 
                                                            rtInt = self.relationInt,
                                                            intermediaire = Inference.dicoInferateur.get_terme_by_id(termeIdInference)["n"],
                                                            gaucheInf = gauche,
                                                            rtInf = self.relationInf,
                                                            droiteInf = droite,
                                                            poidsInt = self.intermediairesC.get(termeIdInference) ,
                                                            poidsInf = elements_inference.get(termeIdInference),
                                                            importanceInt = self.metaPoidsRelationIntermediaire ,
                                                            importanceInf = self.metaPoidsRelationInference
                                                            )
                                                    )

                                                        
            #on a nos inférences, on les trie par poids croissant
            self.listeTuplesInference.sort(key=lambda x: x.get_poids_inference(), reverse=True)
            nbrDePoidsNegatif = 0

            resultat=[]

            nbrTuples = min(self.nombreInf, len(self.listeTuplesInference))

            for i in range(nbrTuples):
                #si on a des inférences négatives, on les privilégie
                if self.listeTuplesInference[-i-1].get_poids_inference() < 0:
                    resultat.append(self.listeTuplesInference[-1-i])
                    nbrDePoidsNegatif += 1
                else:
                    resultat.append(self.listeTuplesInference[i+nbrDePoidsNegatif])
            
            self.listeTuplesInference = resultat

    


    def print_inferences(self):
        for tupleInference in self.listeTuplesInference:
            tupleInference.print_inference_propre()

    def get_tuples_inference_triangles(self):
        return self.listeTuplesInference






        
    

    
