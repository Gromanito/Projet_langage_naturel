from classes.Noeud import *

class DicoInferateur:

    """
        objet dans lequel est enregistré tous les noeuds (d'une session) nécessaires
        pour faire des inférences
    """


    def __init__(self):

        """
            les noeuds sont les objets Noeuds,
            les termes sont les dictionnaires python dont la clé est l'identifiant du terme et les valeurs sont "name" et "weight"
        """

        self.nodes = {}
        # map  string --> Noeud

        self.termes = {}
        # map id --> terme

    
    def get_node_by_string(self, nodeString):
        return self.nodes.get(nodeString)

    def get_terme_by_id(self, id):
        return self.termes.get(id)
    
    def add_termes(self, termesList):
        for id, terme in termesList.items() :
            self.termes[id] = terme


    def add_terme(self, id, terme):
        self.termes[id] = terme

    
    def add_node(self, node):
        self.nodes[node.get_name()] = node
    

    def create_node(self, nodeString):
        noeudCree = Noeud(nodeString)
        self.nodes[nodeString] = noeudCree
        return noeudCree