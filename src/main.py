"""programme pour faire des inférences, jspTrop"""


import recupDonnees



def remplirDicos(dicoDesRelations, dicoDesTermes):






def recup_input_user():

    #bon j'aime pas trop les boucles infinies mais j'ai la flemme de faire autrement
    while True:
        entree = input("Veuillez entrer trois éléments séparés par des espaces ('exit' pour quitter) : ").strip()
        
        # Vérifier si l'utilisateur veut quitter le programme
        if entree.lower() == "exit":
            print("Au revoir")
            break
        
        
        elements = entree.split()
        if len(elements) != 3:
            print("L'entrée doit contenir trois termes séparés par des espaces.")
            continue
        
        
        return elements

            

        




def jouer():

    print("Bienvenue sur Super Inferator!\n\n")


    #on récup les types de relation et de noeud
    with  open("res/fichiersExploitables/rt.json") as fichier:
        relation_types = json.load(fichier)

    with  open("res/fichiersExploitables/nt.json") as fichier:
        node_types = json.load(fichier)
    

    #boucle infinie, on peut demander autant d'inférences que l'on veut
    #le programme s'arrête quand l'utilisateur rentre "exit"
    while True:
        elements = recup_input_user()

        relation = relation_types.get(elements[1])

        terme1aEteRecup = recupDonnees.recupBaseBrut(elements[0])
        terme2aEteRecup = recupDonnees.recupBaseBrut(elements[2])
        

        ttSestBienPasse = terme1aEteRecup and 
                          terme2aEteRecup and 
                          relation is not None


        if not ttSestBienPasse:
            print("problème lors de la récupération des données.\n(Avez vous bien écrit vos termes?)")
            continue
        
        else:
            
            #on a bien les données en local, mtn on les charge et on infère




        


        










def recupFichier


