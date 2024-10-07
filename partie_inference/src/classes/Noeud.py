from requests_html import HTMLSession
import os
import json


from chargerDonnees import *



class Noeud:
    
    """
    classe qui représente un noeud dans jeu de mot
    donc son id, son nom et son poids, 
    ses relations
    """


    #************     variables de classe      *************************

    #référence vers l'objet principal du programme (qui stocke tout)
    dicoInferateur = None

    #**********************************************************


    def __init__(self, name ):

        self.name = name
        

        self.relations = None
        termes, self.relations = recup_exploitable(name)

        #quelque chose s'est mal passé dans la récup des données
        if termes is None or self.relations is None:
            print("impossible de créer le noeud, pour l'instant on existe")

        self.id = termes.pop("id")

        self.weight = termes[self.id]["w"]

        Noeud.dicoInferateur.add_termes(termes)
    
    def get_name(self):
        return self.name
    
    def get_string(self):
        return self.name
    
    def get_id(self):
        return self.id
    
    def get_weight(self):
        return self.weight

    
    def get_sortants(self, relation, nombre = None, poidsNegatifs=True):
        return self.get_relation(relation, sortant=True, nombre=nombre, poidsNegatifs=poidsNegatifs)
    


    def get_entrants(self, relation, nombre = None, poidsNegatifs=True):
        return self.get_relation(relation, sortant=False, nombre=nombre, poidsNegatifs=poidsNegatifs)


    
    def get_relation(self, relation, sortant=True, nombre=None, poidsNegatifs=True):
        
        
        result = {}
        cible = self.relations[relation]["sortant"] if sortant else self.relations[relation]["entrant"]

        if nombre is None:
            nombreTuple = len(cible)
        else:
            nombreTuple = nombre

    
        for idTerme, poids in cible.items():
            if poids > 0 or poidsNegatifs:
                result[idTerme] = poids
            nombreTuple -= 1

            if nombreTuple < 0:
                break

        return result




