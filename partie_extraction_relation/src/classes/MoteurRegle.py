import inspect



#le fichier fonction_regles contient toutes les règles compilées qui modifieront le graphe

#le packetage inspect permet d'obtenir tous les objets "fonctions" d'un module (un fichier importé quoi)

class MoteurRegle:
    """
        classe qui servira à gérer l'application des règles
        (vérification de si elles ont déjà été appliquées,
        refaire une itération de règle si le graphe a changé, etc)
    """

    def __init__(self, graphe, module):

        self.stockageReglesAppliquees = {}
        #dictionnaire de set
        # {règle0 : set(),   règle1: set() ...}


        self.graphe = graphe
        self.grapheModifie = False

        self.regles = []

        #module est un objet "fichier" qui contient des objets "fonctions"
        for nom, fonction in inspect.getmembers(module, inspect.isfunction):
            #on enregistre ces fonctions (exécutables) dans une liste
            self.regles.append(fonction)

        
        


    def application_des_regles(self):
        
        #sera modifié par self.regle_deja_appliquee si on n'a jamais applique une règle
        self.grapheModifie = True

        while self.grapheModifie:
            self.grapheModifie = False
        
            #l'objet "regle" est une fonction qui prend 2 arguments en paramètres
            for regle in self.regles:
                regle(self.graphe, self)
            
           

            
            


    def regle_deja_appliquee(self, regle, substitution):
        #on regarde si la regle a déjà été appliquée
        #si c'est le cas, on dit juste que ça a déjà été appliquée,
        #sinon on dit que ça a pas encore été appliqué et on enregistre pour plus tard
        
        regleDejaAppliquee = True
        
        if regle not in self.stockageReglesAppliquees:
            regleDejaAppliquee = False
            self.stockageReglesAppliquees[regle] = set()
            self.stockageReglesAppliquees[regle].add(substitution)

        
        else:
    
            if substitution not in self.stockageReglesAppliquees[regle]:
            
                regleDejaAppliquee = False
                self.stockageReglesAppliquees[regle].add(substitution)

        #si une regle va être appliquée, on modifie le graphe
        if not regleDejaAppliquee:
            self.grapheModifie = True

        return regleDejaAppliquee