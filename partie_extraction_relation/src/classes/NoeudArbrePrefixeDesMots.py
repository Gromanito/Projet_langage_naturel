import re


class NoeudArbrePrefixeDesMots:
    """
    Classe représentant un nœud dans l'arbre préfixe.
    
    Attributs:
        mot (str): Le mot ou fragment de mot représenté par ce nœud.
        fin (bool): Indique si ce nœud correspond à la fin d'un mot composé.
        enfants (list): Liste des nœuds enfants.
    """
    def __init__(self, mot):
        self.mot = mot
        self.fin = False
        self.enfants = {}

    def ajouter_enfant(self, mot):
        
        """
        Ajoute un enfant à ce nœud ou retourne un enfant existant avec le même mot.

        :param mot: str, le mot de l'enfant à ajouter ou chercher
        :return: NoeudArbrePrefixeDesMots, le nœud enfant correspondant
        """

        #si le sous arbre connexe comportant le mot existe déjà, on le retourne juste
        if mot in self.enfants:
            return self.enfants[mot]
        
        #si dans mes enfants j'ai pas le sous arbre connexe, on le crée
        else:
            nouvel_enfant = NoeudArbrePrefixeDesMots(mot)
            self.enfants[mot]=nouvel_enfant
            return nouvel_enfant


def construire_arbre_prefixe(fichier):
    """
    Construit un arbre préfixe (trie) à partir d'un fichier contenant des mots composés.

    :param fichier: str, chemin vers le fichier contenant les mots composés
    :return: NoeudArbrePrefixeDesMots, la racine de l'arbre préfixe
    """
    # Racine de l'arbre
    racine = NoeudArbrePrefixeDesMots("")

    # Lecture du fichier
    with open(fichier, 'r', encoding='raw_unicode_escape') as f:

        commencer_parsage = False
        for ligne in f:

            # Ignorer les lignes jusqu'à trouver une ligne commençant par un chiffre
            if not commencer_parsage:
                if re.match(r"^\d+", ligne):
                    commencer_parsage = True
                else:
                    continue
        
        
            # Extraction du mot composé après le point-virgule

            if ';"' in ligne:

            
                mot_compose = ligne.split(';"')[1].split('";')[0]

                # Insertion dans l'arbre
                noeud_courant = racine
                for mot in mot_compose.split():
                    noeud_courant = noeud_courant.ajouter_enfant(mot)

                # Marque la fin d'un mot composé
                noeud_courant.fin = True

    return racine