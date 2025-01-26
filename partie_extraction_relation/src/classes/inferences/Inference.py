import json
import os
from classes.inferences.Noeud import *


class Inference:

    dicoInferateur = None

    """classe abstraite qui permet de stocker les conversifs, les schémas,
       et deux / trois fonctions utiles
    """

    conversifs = {"r_lieu":"r_lieu-1",\
            "r_lieu-1":"r_lieu",\
            "r_carac-1":"r_carac",\
            "r_carac":"r_carac-1",\
            "r_agent":"r_agent-1",\
            "r_agent-1":"r_agent",\
            "r_has_part":"r_holo",\
            "r_holo":"r_has_part",\
            "r_patient": "r_patient-1",\
            "r_patient-1": "r_patient",\
            "r_instr": "r_instr-1",\
            "r_instr-1": "r_instr",\
            "r_syn":"r_syn",\
            "r_own": "r_own-1",\
            "r_own-1": "r_own",\
            "r_sentiment": "r_sentiment-1",\
            "r_sentiment-1": "r_sentiment",\
            "r_lieu_action": "r_action_lieu",\
            "r_action_lieu": "r_lieu_action",\
            "r_action-verbe":"r_verbe-action",\
            "r_verbe-action":"r_action-verbe",\
            "r_processus>instr": "r_processus>instr-1",\
            "r_processus>instr-1": "r_processus>instr",\
            "r_processus>patient": "r_processus>patient-1",\
            "r_processus>patient-1": "r_processus>patient",\
            "r_processus>agent":"r_processus>agent-1",\
            "r_processus>agent-1":"r_processus>agent",\
            "r_has_conseq": "r_has_causatif",\
            "r_has_causatif": "r_has_conseq"
            }
    

    with open("partie_extraction_relation/res/schema_inference.json", 'r') as fichier:
        schemas_inference = json.load(fichier)
    
    


    def __init__(self, A, rt, B, schema):

        self.A = A
        self.B = B
        self.relation = rt

        self.nombreInf = schema["nombreInf"]

        ligneInference = schema["inference"].split(";")
        self.gaucheInf = ligneInference[0]
        self.relationInf = ligneInference[1]
        self.droiteInf = ligneInference[2]

        if self.relationInf == "rt":
            self.relationInf = self.relation


        self.listeTuplesInference = []
    

    def get_terme1(self):
        return self.terme1
    
    def get_terme2(self):
        return self.terme2
    
    def get_relation(self):
        return self.relation
    

    

