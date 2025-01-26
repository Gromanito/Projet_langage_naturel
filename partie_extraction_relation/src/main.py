from classes.Graphe import *
from classes.NoeudArbrePrefixeDesMots import *
from classes.MoteurRegle import *



import regles_compilees
import os
import subprocess



#compile les règles si jamais elles ont été modifiées
def execute_if_needed(program_a, file_t, file_b):
    """
    Exécute le programme A si le fichier B est plus ancien que le fichier T.

    :param program_a: str, chemin ou commande du programme A
    :param file_t: str, chemin vers le fichier d'entrée T
    :param file_b: str, chemin vers le fichier de sortie B
    """
    try:
        # Vérifier si les fichiers existent
        if not os.path.exists(file_t):
            raise FileNotFoundError(f"Le fichier d'entrée {file_t} n'existe pas.")
        
        if not os.path.exists(file_b):
            subprocess.run([program_a, file_t], check=True)
            return
        
        # Obtenir les dates de modification
        time_t = os.path.getmtime(file_t)
        time_b = os.path.getmtime(file_b)
        
        # Comparer les dates et exécuter si nécessaire
        if time_t > time_b:
            print("Compilation des règles")
            subprocess.run(["python3", program_a], check=True)

    except Exception as e:
        print(f"Erreur : {e}")






#on peut construire l'arbre préfixe des mots, 
# mais sur mon ordi ça prend 10secondes + 20% de ma RAM


# print("construction de l'abre préfixe des mots...")
# arbrePrefixeDesMots = construire_arbre_prefixe("noeudsJDM/LEXICALNET-JEUXDEMOTS-ENTRIES-MWE.txt")


print("\n\n")

programme = "partie_extraction_relation/src/compile_regles_en_fonction.py"
fichierRegle = "partie_extraction_relation/res/regles.txt"
fichierRegleCompilees = "partie_extraction_relation/src/regles_compilees.py"


#compile les règles si besoin
execute_if_needed(programme,fichierRegle, fichierRegleCompilees)

print("\n")

#boucle principale



user_input = input("\n\nEntrez une phrase! (il faut qu'elle termine par un . )  (ou 'exit' pour quitter) : ")



print("création du graphe linéaire de la phrase")
graphe_phrase = Graphe(user_input.replace("n'", "ne "), None)



#Le moteur de règle
moteurRegle = MoteurRegle(graphe_phrase, regles_compilees)

print("application des règles")
moteurRegle.application_des_regles()


graphe_phrase.extraire_relations()



        

    


