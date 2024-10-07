class TupleInferenceTriangle:

    def __init__(self, sourceIntermediaire, rtInt, intermediaire, gaucheInf, rtInf, droiteInf, poidsInt, poidsInf, importanceInt, importanceInf):
        """
            Classe qui va contenir toutes les informations d'une seule inférence
            (quel est le poids de cette inférence? avec quel chemin? quels termes utilisés?)

            tous les attributs (sauf les poids) sont des strings
        """

        self.sourceIntermediaire = sourceIntermediaire
        self.rtInt = rtInt
        self.intermediaire = intermediaire
        self.gaucheInf = gaucheInf
        self.rtInf = rtInf
        self.droiteInf = droiteInf
        
        self.poidsInference = None
        
        #on calcule le poids de l'inférence

        #si y a un poids négatif, on s'arrête là (peur de faire une div par zéro ou quoi)
        if poidsInf < 0:
            self.poidsInference = poidsInf

        #sinon on calcule le poids selon une formule de mon invention (voir le README)
        else:
            importancePoidsIntermediaire = poidsInt / (poidsInt + poidsInf) 
            importancePoidsInference =     poidsInf / (poidsInt + poidsInf) 

            nouvelleImportancePoidsIntermediaire = importancePoidsIntermediaire * float(importanceInt)
            nouvelleImportancePoidsInference = importancePoidsInference * float(importanceInf)
            
            
            nouveauPoidsIntermediaire = nouvelleImportancePoidsIntermediaire * poidsInt
            nouveauPoidsInference = nouvelleImportancePoidsInference * poidsInt

            self.poidsInference = nouveauPoidsInference
    

    def get_poids_inference(self):
        return self.poidsInference


    def print_inference_propre(self):

        chaineReponse = ""

        if self.poidsInference > 0:
            chaineReponse += "oui car   "
        else:
            chaineReponse += "non car   "
        
        chaineReponse += self.sourceIntermediaire + '  ' + self.rtInt+ '  ' + self.intermediaire + '     &     ' + self.gaucheInf + '  ' + self.rtInf + '  ' + self.droiteInf + ' | ' + str(self.poidsInference)

        print(chaineReponse)
    



    def get_inference_parsable(self):
        chaineReponse = ""

        if self.poidsInference > 0:
            chaineReponse += "oui|"
        else:
            chaineReponse += "non|"

        chaineReponse += self.sourceIntermediaire + ' ' + self.rtInt+ ' ' + self.intermediaire + ' & ' + self.gaucheInf + ' ' + self.rtInf + ' ' + self.droiteInf + '|' + str(self.poidsInference)

        return chaineReponse