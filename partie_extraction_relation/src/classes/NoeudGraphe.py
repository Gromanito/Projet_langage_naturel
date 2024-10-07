

class NoeudGraphe:

    graphe = None


    """
        classe qui représente un noeud dans le graphe (avec le poids, l'id etc etc)
    """

    def __init__(self, id, nodeJDM):
        
        self.id = id
        self.weight = 1
        self.label = None
        self.nodeJDM = nodeJDM
        
        
