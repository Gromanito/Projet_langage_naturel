import networkx as nx
from telechargeDonneesApi import *
from classes.NoeudArbrePrefixeDesMots import *
from classes.Desambiguiseur import *

import json
import uuid
import re

class Graphe(nx.MultiDiGraph):


    with open( "noeudsJDM/infoNoeuds/rt.json", 'r') as fichier:
        rtJSON = json.load(fichier)
        del(rtJSON['r_succ'])
        del(rtJSON['r_pos'])




    def __init__(self, phrase, arbrePrefixeDesMots):
        """
        Transforme une phrase en un graphe où chaque mot et signe de ponctuation
        est un nœud, et les relations entre les mots (ordre dans la phrase) sont des arêtes.

        :param phrase: str, la phrase à transformer en graphe
        """
        super().__init__()

        


        #on remplace les apostrophes prck elles sont relou
        self.phrase = phrase.replace("'", ' ')


        self.desambiguiseur = Desambiguiseur(self)

        # Séparation des mots et des signes de ponctuation
        tokens = re.findall(r"\w+|[',.\"!?:;]", phrase)
        
        print(tokens)


        self.indiceDebutPhrase = 0
        self.indiceFinPhrase = len(tokens)-1


        


        # Ajout des nœuds et des arêtes
        for i, token in enumerate(tokens):
            #on récupère le r_pos du token
            
            self.add_node(i, name=token, type_node='terme', w=1)


            if i > 0:
                self.add_edge(i-1, i, label='r_succ', w=1)
                self.add_edge(i, i-1, label='r_pred', w=1)
        

        #on ajoute les noeuds "début" et "fin", qui sont des noeuds à part
        self.add_node('start', name='start', type_node='meta', w=1)
        self.add_node('end', name='end', type_node='meta', w=1)

        self.add_edge('start', self.indiceDebutPhrase, label = 'r_succ', w=1)
        self.add_edge(self.indiceDebutPhrase, 'start', label = 'r_pred', w=1)
        self.add_edge('end', self.indiceFinPhrase, label = 'r_pred', w=1)
        self.add_edge(self.indiceFinPhrase, 'end', label = 'r_succ', w=1)


        #on ajoute d'abord les r_lemma utile pour les verbes
        self.ajout_noeuds_r_lemma()

        #on essaie maintenant de "combiner" des noeuds qui sont des termes composés
        #ne pas voir "pied" "de" "biche" comme 3 noeuds différents, il s'agit du même terme
        
        # self.ajout_termes_composes(arbrePrefixeDesMots)
        
        #on ajoute maintenant tous les r_pos
        self.ajout_noeuds_r_pos_dupliques()


        #on "met à jour" le désambiguiseur pour qu'il puisse récupérer tous les noeuds du graphe   

        for noeud in self.nodes:
            if self.nodes[noeud]['type_node'] in ['terme', 'r_lemma']:
                self.desambiguiseur.ajouter_noeud(noeud)




        


        


    

    """
    méthodes d'initialisation
    """


    #ajoute des noeuds r_lemma pour chaque mot de la phrase d'origine
    #(exécuté une seule fois au début)
    def ajout_noeuds_r_lemma(self):

        for i in range(self.indiceDebutPhrase, self.indiceFinPhrase+1):

            noeud_courant = self.nodes[i]
            mot = noeud_courant['name']

            if mot != '.':

                telecharge_exploitable(mot) #on en profite pour télécharger le mot au passage
                tous_les_r_lemma = get_node_relations_by_name(mot)["r_lemma"]["sortant"]
                
                tous_les_r_pos = get_node_relations_by_name(mot)["r_pos"]["sortant"]

                if "Ver:" in tous_les_r_pos or "Abr:" in tous_les_r_pos:

                    #on crée tous les noeuds r_lemma pour les verbes
                    for r_lemma, poids in tous_les_r_lemma.items():
                        #pour tous les r_lemma positifs
                            if poids > 0 and r_lemma != mot:

                                telecharge_exploitable(r_lemma) 
                                #c'est un mot dont on va avoir besoin, on le télécharge
                                
                                #on crée un nouveau noeud r_lemma
                                id_nouveau_noeud_r_lemma = uuid.uuid4() 
                                self.add_node(id_nouveau_noeud_r_lemma, name=r_lemma, type_node='r_lemma', w=1 )

                                #on le relie aux bons predecesseurs et aux bons successeurs
                                self.relie_noeud_pred_succ(id_nouveau_noeud_r_lemma, i, i)




    #ajoute des noeuds r_pos pour chaque mot (r_lemma ou non)
    #exécuté une fois, juste après l'ajout des r_lemma
    def ajout_noeuds_r_pos(self):
        
        #une fois qu'on a créé tous les noeuds, on ajoute les noeuds r_pos
        #on crée un nouveau noeud pour chaque r_pos qui existe

        #on va mettre un noeud r_pos pour chaque noeud terme ou r_lemma
        noeuds_concernes = self.get_all_nodes_terme()

        
        for id_noeud in noeuds_concernes:
            noeud_courant = self.nodes[id_noeud]
            mot = noeud_courant['name']

            if mot == '.':
                id_nouveau_noeud_r_pos = uuid.uuid4()
                self.add_node(id_nouveau_noeud_r_pos, name = 'Punct:', type_node='pos', w=1)
                self.add_edge(id_noeud, id_nouveau_noeud_r_pos, label = 'r_pos', w=1)
            
            else:
                tous_les_r_pos = get_node_relations_by_name(mot)["r_pos"]["sortant"]
                

                #on crée tous les noeuds r_pos et tous les noeuds 
                for r_pos, poids in tous_les_r_pos.items():
                    #pour tous les r_pos positifs, qui sont de la forme "Truc:"  (on veut pas les Nom:Gen:Mas)
                        if poids > 0:
                            id_nouveau_noeud_r_pos = uuid.uuid4()
                            self.add_node(id_nouveau_noeud_r_pos, name = r_pos, type_node='pos', w=1)
                            self.add_edge(id_noeud, id_nouveau_noeud_r_pos, label = 'r_pos', w=1)
        
        


#on crée des nouveauds noeux pour CHAQUE r_pos du noeud
    def ajout_noeuds_r_pos_dupliques(self):

        noeuds_concernes = self.get_all_nodes_terme()

        
        for id_noeud in noeuds_concernes:
            noeud_courant = self.nodes[id_noeud]
            mot = noeud_courant['name']

            if mot == '.':
                id_nouveau_noeud_r_pos = uuid.uuid4()
                self.add_node(id_nouveau_noeud_r_pos, name = 'Punct:', type_node='pos' , w=1)
                self.add_edge(id_noeud, id_nouveau_noeud_r_pos, label = 'r_pos', w=1)
            

            else:
                tous_les_r_pos = get_node_relations_by_name(mot)["r_pos"]["sortant"]

                #on crée tous les noeuds r_pos et tous les noeuds 
                for r_pos, poids in tous_les_r_pos.items():
                    #pour tous les r_pos positifs, qui sont de la forme "Truc:"  (on veut pas les Nom:Gen:Mas)
                        if poids > 0:
                            id_nouveau_noeud = uuid.uuid4()
                            id_nouveau_noeud_r_pos = uuid.uuid4()
                            
                            self.add_node(id_nouveau_noeud, name = mot, type_node='terme', w=1)
                            self.add_node(id_nouveau_noeud_r_pos, name = r_pos, type_node='pos', w=1)
                            
                            self.relie_noeud_pred_succ(id_nouveau_noeud, id_noeud, id_noeud)

                            self.add_edge(id_nouveau_noeud, id_nouveau_noeud_r_pos, label = 'r_pos', w=1)
        
    



    #on calcule tous les termes composés possibles de la phrase
    def ajout_termes_composes(self, arbrePrefixeDesMots):

        noeuds_concernes = [n for n in self if self.nodes[n]['type_node'] in ['terme', 'r_lemma']  ]

        #pour chaque noeud "terme" du graphe
        for id_noeud in noeuds_concernes:

            noeud_courant = id_noeud
            terme_courant = self.nodes[noeud_courant]["name"]

            if terme_courant in arbrePrefixeDesMots.enfants:
                liste_noeuds_parcourus = [id_noeud]

                #parcours récursif de l'abre pour chaque terme 
                self.parcours_arbre_prefixe(noeud_courant, liste_noeuds_parcourus, arbrePrefixeDesMots.enfants[terme_courant])


           



    def parcours_arbre_prefixe(self, noeud_courant, liste_noeuds_parcourus, arbre_courant):


        #on est arrivé sur un arbre avec un certain terme et une certaine liste de noeuds parcourus
        #on regarde si jamais il s'agit bien d'un mot composé

        if arbre_courant.fin:
            _, nouveau_mot = self.ajoute_noeud_par_dessus("terme_composé", *liste_noeuds_parcourus)
            telecharge_exploitable(nouveau_mot)
        
        #on entame une étape du parcours
        tous_les_succ = self.get_successors_with_labelled_edge(noeud_courant, 'r_succ')

        for succ in tous_les_succ:

            noeud_suivant = succ
            terme_suivant = self.nodes[noeud_suivant]["name"]

            if terme_suivant in arbre_courant.enfants:
                liste_noeuds_parcourus.append(noeud_suivant)
                self.parcours_arbre_prefixe(noeud_suivant, liste_noeuds_parcourus, arbre_courant.enfants[terme_suivant])
                liste_noeuds_parcourus.pop()
            




    """fonctions appelées lors de l'application des règles"""

    def creer_noeud_regle(self, type_node, *noeuds_couverts):
        
        id_nouveau_noeud, _ = self.ajoute_noeud_par_dessus(type_node, *noeuds_couverts )
        self.desambiguiseur.ajouter_noeud(id_nouveau_noeud)

        return id_nouveau_noeud


    """
    fonctions utilisées pour l'extraction des relations
    """

    #dans l'analyse, on pourrait avoir "Le chat" r_agent-1 boire,
    #mais on a pu "oublier" "chat" r_agent-1 boire, il faut propager les relations JDM avec le r_chef
    def propage_relations(self):
        for noeud in self.get_all_nodes_terme():
            for r_chef in self.get_successors_with_labelled_edge(noeud, "r_chef"):

                for successor in self.successors(noeud):
                    for arete in self[noeud][successor].values():
                        if successor != r_chef and arete["label"] in Graphe.rtJSON:
                            self.add_edge(r_chef, successor, label=arete["label"], w=1)

                for predecessor in self.predecessors(noeud):
                    for arete in self[predecessor][noeud].values():
                        if predecessor != r_chef and arete["label"] in Graphe.rtJSON:
                            self.add_edge(predecessor, r_chef, label=arete["label"], w=1)



    #écrit toutes les relations extraites
    def extraire_relations(self):
        
        #je coupe tous les noeuds qui n'apparaissent pas dans la structure syntaxique de la phrase
        self.desambiguiseur.desambiguiser()


        #on propage les relations sémantiques jusqu'au r_chef
        self.propage_relations()


        #on enlève les noeuds qu'on a fabriqués mais qui n'apparaissent dans aucune phrase
        self.desambiguiseur.couper_noeud_non_phrases()

        relations_extraites = set()

        

        for noeud in self.get_all_nodes_terme():
            #print("noeud Gauche : ", self.nodes[noeud]["name"], self.get_r_pos_of_node(noeud))
            if "Nom:" in self.get_r_pos_of_node(noeud) or "Ver:" in self.get_r_pos_of_node(noeud):
                for successor in self.successors(noeud):
                    if self.nodes[successor]['w'] > 0:
                        #print("noeud Droite : ", self.nodes[successor]["name"], self.get_r_pos_of_node(successor))
                        if "Nom:" in self.get_r_pos_of_node(successor) or "GV:" in self.get_r_pos_of_node(successor) or "GV:Passive:" in self.get_r_pos_of_node(successor):
                            for arete in self[noeud][successor].values():   
                                if arete["label"] in Graphe.rtJSON and arete['w'] > 0:
                                    relations_extraites.add( self.nodes[noeud]["name"] + '   ' + arete["label"] + '   ' + self.nodes[successor]["name"] )


        relations_extraites = list(relations_extraites)
        relations_extraites.sort()
        for relation in relations_extraites:
            print(relation)

    """
    fonctions utilitaires pour la classe
    """


    def ajoute_noeud_par_dessus(self, type_node, *noeuds_couverts):
        #méthode qui prend un certains nombre de noeuds, et ajoute un seul noeud
        #couvrant tous les noeuds passés en paramètres (en liant les prédécesseurs et les successeurs)

        id_nouveau_noeud = uuid.uuid4()

        mot_nouveau_noeud = ' '.join(self.nodes[noeud]['name'] for noeud in noeuds_couverts)

        self.add_node(id_nouveau_noeud, type_node = type_node, name=mot_nouveau_noeud, w=1)


        self.relie_noeud_pred_succ(id_nouveau_noeud, noeuds_couverts[0], noeuds_couverts[-1])
        
        return id_nouveau_noeud, mot_nouveau_noeud
        

    # Fonction pour obtenir les successeurs avec un label spécifique
    def get_successors_with_labelled_edge(self, node, label):
        # Parcourir les successeurs et filtrer par le label de l'arête

        successors = []

        for succ in self.successors(node):
            for arete in self[node][succ].values():
                if arete["label"] == label and arete['w'] > 0:
                    successors.append(succ)
        
        return successors


    
    # Fonction pour obtenir les predecesseurs avec un label spécifique
    def get_predecessors_with_labelled_edge(self, node, label):
        # Parcourir les predecesseurs et filtrer par le label de l'arête
        predecessors = []

        for pred in self.predecessors(node):
            for arete in self[pred][node].values():
                if arete["label"] == label and arete['w'] > 0:
                    predecessors.append(pred)
        
        return predecessors



    def get_r_pos_of_node(self, node):
        return [self.nodes[node]['name'] for node in self.get_successors_with_labelled_edge(node, 'r_pos') ]
    


    def get_sub_nodes_of_node(self, node):
        #retourne la "décomposition" d'un noeud

        result = {}

        for succ in self.successors(node):
            for arete in self[node][succ].values():
                if arete["label"].startswith("r_sub_node:"):
                    result[arete["label"][11:]] = succ

        return result
    

    def get_all_nodes_terme(self):
        return [n for n in self if self.nodes[n]['type_node'] in ['terme_composé', 'r_lemma', 'terme'] and self.nodes[n]['w']>0]

    
    def add_r_pos_to_node(self, pos, node):

        id_nouveau_noeud = uuid.uuid4()

        self.add_node(id_nouveau_noeud, type_node='pos', name=pos, w=1)
        self.add_edge(node, id_nouveau_noeud, label='r_pos', w=1)
    


    #relier un nouveau noeud couvrant d'autres noeuds
    #les prédecesseurs seront les prédécesseurs du noeud couvert le plus à gauche
    #les successeurs seront les successeurs du noeud couvert le plus à droite
    def relie_noeud_pred_succ(self, nouveau_noeud, noeud_gauche, noeud_droite):

        tous_les_pred = self.get_successors_with_labelled_edge(noeud_gauche, 'r_pred')
        tous_les_succ = self.get_successors_with_labelled_edge(noeud_droite, 'r_succ')

        #on lie avec tous les noeuds précédents et les noeuds suivants
        for pred in tous_les_pred:
            self.add_edge(pred, nouveau_noeud, label='r_succ', w=1)
            self.add_edge(nouveau_noeud, pred, label='r_pred', w=1)

        for succ in tous_les_succ:
            self.add_edge(nouveau_noeud, succ, label='r_succ', w=1)
            self.add_edge(succ, nouveau_noeud, label='r_pred', w=1)



    #met toutes les arêtes sortantes et entrantes à -1 (coupe "virtuellement" le noeud)
    def couper_noeud(self, noeud):
        preds = self.get_predecessors_with_labelled_edge(noeud, 'r_pred')
        succs = self.get_successors_with_labelled_edge(noeud, 'r_succ')

        self.nodes[noeud]['w'] = -1

        for pred in preds:
            for arete in self[pred][noeud].values():
                arete['w'] = -1
        for succ in succs:
            for arete in self[noeud][succ].values():
                arete['w'] = -1
        
            
    
    

    
