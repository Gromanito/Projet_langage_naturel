""" fichier temporaire"""


""" suite de fonctions qui traitent les fichiers traites json 
et les transforme en fichier json directement utilisable pour les inférences


"""

import json
import os



#les relations qu'on utilise pour les inférences
nomsRelationsQuonUtilise = ["r_isa", "r_hypo",  "r_agent", "r_agent-1",\
                            "r_lieu_action", "r_action_lieu", "r_lieu", "r_lieu-1",\
                            "r_processus>agent", "r_processus>agent-1",\
                            "r_action-verbe", "r_verbe-action",\
                            "r_holo", "r_has_part", "r_syn", "r_lemma", \
                            "r_verb_real", "r_own", "r_own-1", "r_instr", "r_instr-1",\
                            "r_processus>instr", "r_processus>instr-1",\
                            "r_der_morpho", "r_patient", "r_patient-1",\
                            "r_carac", "r_carac-1", "r_sentiment", "r_sentiment-1",\
                            "r_processus>patient", "r_processus>patient-1",\
                            "r_family", "r_has_conseq", "r_has_causatif" ]

#les noeuds qui nous intéressent (pour pas trop en stocker dans le fichier traité)
idsTypesNoeudsQuonUtilise = [1, 2, 8, 9, 666, 777]

#fonction qui extrait le fichier json traité et crée les fichiers 
def json_vers_exploitable(nomTerme, dicoJson, rtJSON=None):

    """
    extrait le fichier json traité et crée des fichiers json 
    exploitables par le programme principal
    
    """


    #le dossier contient les noeuds et les relations
    directoryExploitable = "res/fichiersExploitables/" + nomTerme + "/"

    
    #on récupère le fichier traité json
    if dicoJson == None:
        with open("res/fichiersTraites/" + nomTerme + ".json", 'r') as fichier:
            objet_json = json.load(fichier)
    else:
        objet_json = dicoJson
    


    # on créé le dossier s'il n'existe pas déjà
    try:  
        os.mkdir(directoryExploitable)
    except FileExistsError:
        pass 
    except OSError as error:  
        print(error)
        return False


    # on prépare les structures pour pouvoir itérer sur les noeuds et les traiter 
    edges = objet_json["e"]
    relations = objet_json["r"]
    idTerme = objet_json["id"]

    nodes = None
    toutesLesRelations = None


    # les noeuds (les termes) n'ont pas encore été créés
    if not os.path.exists(directoryExploitable + "e.json"):
        
        global idsTypesNoeudsQuonUtilise
        nodes = {}
        nodes["id"] = idTerme

        #on traite chaque noeud
        for idNoeud, noeud in edges.items():
            #y a que les noeuds "terme" qui nous intéressent
            if noeud["node_type"] in idsTypesNoeudsQuonUtilise:
                nodeName = noeud["name"] if noeud["formated_name"] is None else noeud["formated_name"]
                nodes[idNoeud] = {"name" : nodeName, "weight": noeud["weight"]}
                
        
        #on enregistre les noeuds en json
        objet_json = json.dumps(nodes, indent=4, ensure_ascii=False)
        with open( directoryExploitable + "e.json", 'w') as fichier:
            fichier.write(objet_json)
            #print("noeuds enregistrés")
    

    #les relations n'ont pas encore été créées
    if not os.path.exists(directoryExploitable + "r.json"):

        toutesLesRelations = {}
        idsRelationsATraiter = []
        
        global nomsRelationsQuonUtilise
        

        if rtJSON == None:
            with open("res/fichiersExploitables/rt.json", 'r') as fichier:
                rtJSON = json.load(fichier)


        #on prépare les relations qu'on doit traiter
        for nomRelation in nomsRelationsQuonUtilise:
            toutesLesRelations[nomRelation] = {"sortant":{}, "entrant":{}}
            idsRelationsATraiter.append(rtJSON[nomRelation])

        
        #on traite chaque relation
        for elementRelationJson in relations.values():
            
            #c'est une relation qui nous intéresse
            if elementRelationJson["type"] in idsRelationsATraiter:
                node1 = elementRelationJson["node1"]
                node2 = elementRelationJson["node2"]
                nomRelation = rtJSON[str(elementRelationJson["type"])]
                poids = elementRelationJson["weight"]
                poids_norme = elementRelationJson["weight_normed"]

                if node1  == idTerme: 
                    #c'est une relation sortante
                    toutesLesRelations[nomRelation]["sortant"][str(node2)] = {"weight" : poids,  "weight_normed" : poids_norme}
                
                else:
                    #c'est une relation entrante
                    toutesLesRelations[nomRelation]["entrant"][str(node1)] = {"weight" : poids,  "weight_normed" : poids_norme}
        
        #on enregistre les relations en json
        with open( directoryExploitable + "r.json", 'w') as fichier:
            fichier.write(json.dumps(toutesLesRelations, indent=4, ensure_ascii=False))
            #print("relations enregistrées")
        
    
    return nodes, toutesLesRelations








def enregistrer_en_json(terme, texteBrut=None, rtJSON = None ):
    """
    Enregistre la chaine brute de la page du terme au format json 
       pour pouvoir manipuler + facilement
    """

    nom_fichier_json = "res/fichiersTraites/"+terme+".json"
    dico = None
    global idsTypesNoeudsQuonUtilise

    #on fait le traitement si le fichier n'existe pas déjà
    if not os.path.exists(nom_fichier_json):
        
        #on récupère le texte brut s'il n'est pas passé en paramètre de la fonction
        if texteBrut == None:
            with open("res/fichiersBruts/"+terme+".txt") as fichier:
                texteBrut = fichier.read()
        
        #pour passer de l'identifiant d'une relation à son nom
        if rtJSON == None:
            with open("res/fichiersExploitables/rt.json", 'r') as fichier:
                rtJSON = json.load(fichier)

        # pour renseigner + tard quelles sont les relations qui existent dans ce fichier
        with open("res/fichiersTraites/relationsParTerme.json", 'r') as fichier:
            relationsParTerme = json.load(fichier)
        relationsParTerme[terme] = []


        edges={}
        relations={}
        relationsExistantes=[]



        #on récupère l'id du terme
        ligneQuiContientLid = texteBrut[texteBrut.find("(eid="):  texteBrut.find("(eid=") + 30 ]
        idTerme = int(ligneQuiContientLid[ligneQuiContientLid.find("(eid=") + 5 : ligneQuiContientLid.find(')')])

        #on traite chaque ligne du texte
        for ligne in texteBrut.splitlines():
            
            # si c'est c'est un noeud
            if ligne.startswith('e;'):
                identifiant, noeud = cree_noeud_a_partir_dune_ligne(ligne)
                if noeud["node_type"] in idsTypesNoeudsQuonUtilise:
                    edges[identifiant] = noeud

            #si c'est une relation
            elif ligne.startswith('r;'):
                identifiant, relation = cree_relation_a_partir_dune_ligne(ligne)

                #des fois les relations se font sur des noeuds qu'on regarde pas, il faut les filtrer
                #(on suppose que les noeuds sont remplis en premier et que donc ça produit pas d'erreurs de faire ça)
                if edges.get(str(relation["node1"])) is not None and edges.get(str(relation["node2"])) is not None:
                    relations[identifiant] = relation
            
            #on retient quelles sont les relations qui existent dans ce fichier
            elif ligne.startswith('rt;'):
                idRelationQuiExiste = ligne.split(';')[1]
                relationsExistantes.append(idRelationQuiExiste)
        

        #Parmi les relations qui existent,
        #on ne garde que les relations qui nous intéresse
        for relation in nomsRelationsQuonUtilise:
            if str(rtJSON[relation]) in relationsExistantes:
                relationsParTerme[terme].append(relation) 
        

        #j'ai traité toutes les lignes
        #j'enregistre le fichier json
        dico = { "id":idTerme, "r":relations, "e":edges}
        objet_json = json.dumps(dico, indent=4, ensure_ascii=False)

        with open(nom_fichier_json, 'w') as fichier:
            fichier.write(objet_json)
            #print("fichier traité json enregistré")
        

        #on renseigne les relations qui existent dans le fichier relationsParTerme
        with open( "res/fichiersTraites/relationsParTerme.json", 'w') as fichier:
            fichier.write(json.dumps(relationsParTerme, indent=4, ensure_ascii=False))
            #print("noeuds enregistrés")
        
    return dico





#fonction pour récupérer le nom d'un noeud
#(le nom d'un noeud peut contenir des ' , donc pas évident en vrai)
def renvoieNameApartirDuneLigne(ligne):
    indexDebut = ligne.find(";'")
    indexFin = ligne.find("';")
    name = ligne[indexDebut+2 : indexFin]
    nouvelleLigne = ligne[0 : indexDebut] + ligne[indexFin+1 :]
    return name, nouvelleLigne





#fonction pour créer un dictionnaire "noeud" à partir d'une ligne
def cree_noeud_a_partir_dune_ligne(ligne):

    ligne = ligne.strip()

    #on récupère le nom du terme
    nom, ligne = renvoieNameApartirDuneLigne(ligne)
    
    #si ça finit par ' c'est qu'à la fin c'est un formated name
    formated_name = None
    
    if ligne.endswith("'"):
        ligneFormatee = ligne + ";"
        formated_name, ligne = renvoieNameApartirDuneLigne(ligneFormatee)

    #une fois qu'on a récupéré le nom et le nom formatté,
    #on sépare les éléments de la ligne
    elements = ligne.split(';') 

    identifiant = elements[1]
    type_noeud = int(elements[2])
    weight = int(elements[3])
    
    return identifiant, {  "name":nom, 
                            "node_type":type_noeud, 
                            "weight":weight, 
                            "formated_name":formated_name }
                            
            
    
            

#fonction pour créer un dictionnaire "relation" à partir d'une ligne
def cree_relation_a_partir_dune_ligne(ligne):
                
    elements = ligne.strip().split(';')

    #on récupère chaque élément de la ligne
    identifiant = elements[1]
    node1 = int(elements[2])
    node2 = int(elements[3])
    type_relation = int(elements[4])
    weight = int(elements[5])
    weight_normed = None
    rank = None

    #les noeuds sortants ont + d'éléments (rank et poids normé)
    if len(elements) > 6: 
        
        if elements[6] != '-':
            weight_normed =  float(elements[6])

        if elements[7].strip() != '-':
            rank =  int(elements[7])

    
    return identifiant, { "node1":node1, 
                            "node2":node2, 
                            "type":type_relation, 
                            "weight":weight,
                            "weight_normed": weight_normed,
                            "rank": rank }








def ajouterRelationsAuJsonTraite(nomTerme, relationString):
    """
        le fichier traité existe déjà, mais on ajoute 
        le fichier txt de la relation au fichier json traité
    """

    nom_fichier_json = "res/fichiersTraites/" + nomTerme + ".json"
    global idsTypesNoeudsQuonUtilise

    #on récupère le json traité
    with open(nom_fichier_json, 'r') as fichier:
        dico = json.load(fichier)



    #on regarde si la relation a déjà été cherchée auparavant
    #pour pas refaire un truc inutile
    with open("res/fichiersTraites/relationsParTerme.json", 'r') as fichier:
        relationsParTerme = json.load(fichier)

    
    #la relation n'existe pas dans le fichier traité, on l'ajoute
    if relationString not in relationsParTerme[nomTerme]:
        
        #on récupère le texte brut du terme avec que la relation indiquée
        with open("res/fichiersBruts/" + nomTerme + relationString + ".txt") as fichier:
            texteBrut = fichier.read()


        #on fait le traitement habituel
        for ligne in texteBrut.splitlines():

            if ligne.startswith('e;'):
                identifiant, noeud = cree_noeud_a_partir_dune_ligne(ligne)
                if noeud["node_type"] in idsTypesNoeudsQuonUtilise:
                    dico["e"][identifiant] = noeud
                
                
            elif ligne.startswith('r;'):
                identifiant, relation = cree_relation_a_partir_dune_ligne(ligne)

                if dico["e"].get(str(relation["node1"])) is not None and dico["e"].get(str(relation["node2"])) is not None:
                    dico["r"][identifiant] = relation
                


        #on enregistre le nouveau fichier json augmenté avec la relation
        objet_json = json.dumps(dico, indent=4, ensure_ascii=False)

        with open(nom_fichier_json, 'w') as fichier:
            fichier.write(objet_json)
            #print("fichier traité json enregistré (avec nouvelle relation)")


        #on renseigne que cette relation existe maintenant bien dans le fichier traité
        relationsParTerme[nomTerme].append(relationString)
        with open("res/fichiersTraites/relationsParTerme.json", 'w') as fichier:
            fichier.write(json.dumps(relationsParTerme, indent=4, ensure_ascii=False))

    
    return dico




            




















#ancien json_vers_exploitable qui créait un fichier par relation 
#(ça faisait bcp de fichier alors qu'en pratique on récupère tout d'un coup)
"""

#fonction qui extrait le fichier json traité et crée les fichiers 
def json_vers_exploitable(nomTerme, dicoJson):

    
    extrait le fichier json traité et crée des fichiers exploitables par
    le programme principal
    
    


    #le fichier contient les noeuds et les relations
    directoryExploitable = "res/fichiersExploitables/" + nomTerme + "/"

    
    if dicoJson == None:
        with open("res/fichiersTraites/" + nomTerme + ".json", 'r') as fichier:
            objet_json = json.load(fichier)
    
    else:
        objet_json = dicoJson
    

    edges = objet_json["e"]
    relations = objet_json["r"]
    idTerme = objet_json["id"]

    try:  
        os.mkdir(directoryExploitable)
    except FileExistsError:
        pass 
    except OSError as error:  
        print(error)
        return False

    nodes = None
    toutesLesRelations = None

    if not os.path.exists(directoryExploitable + "e.json"):
        # on génère le fichier e.json (sans les noeuds relations )
        nodes = {}
        nodes["id"] = idTerme

        for idNoeud, noeud in edges.items():

            #y a que les noeuds "terme" qui nous intéressent (pour l'instant)
            if noeud["node_type"] != 10:
                nodeName = noeud["name"] if noeud["formated_name"] is None else noeud["formated_name"]
                nodes[idNoeud] = {"name" : nodeName, "weight": noeud["weight"]}
        
        objet_json = json.dumps(nodes, indent=4, ensure_ascii=False)
    
        with open( directoryExploitable + "e.json", 'w') as fichier:
            fichier.write(objet_json)
            print("noeuds enregistrés")
    
    toutesLesRelations = {}
    typesDesFichiersDejaCrees =[]
    # on génère les fichiers r_isa.json, r_agent-1, r_haspart... etc (que s'ils n'existent pas)
    with open("res/fichiersExploitables/rt.json", 'r') as fichier:
        rtJSON = json.load(fichier)


    relationsQuonADeja = [nomFichier.split('.')[0] for nomFichier in os.listdir("res/fichiersExploitables/"+nomTerme)]
    idsRelationsATraiter = []
    #on peut en ajouter + tard pour d'autres inférences
    nomsRelationsQuonUtilise = ["r_isa", "r_has_part", "r_agent", "r_agent-1", "r_lieu", "r_lieu-1", "r_processus>agent", "r_processus>agent-1", "r_hypo"]
    
    #on filtre les relations qu'on doit traiter
    #(soit parce qu'on a déjà le fichier, soit prck c'est pas une relation qui nous intéresse)
    for nomRelation in nomsRelationsQuonUtilise:
        if nomRelation not in relationsQuonADeja:
            toutesLesRelations[nomRelation] = {"sortant":{}, "entrant":{}}
            idsRelationsATraiter.append(rtJSON[nomRelation])


    #le dico contient que les trucs UTILES
    
    #on traite chaque relation
    for elementRelationJson in relations.values():
        
        #c'est une relation qui nous intéresse
        if elementRelationJson["type"] in idsRelationsATraiter:
            node1 = elementRelationJson["node1"]
            node2 = elementRelationJson["node2"]
            nomRelation = rtJSON[str(elementRelationJson["type"])]
            poids = elementRelationJson["weight"]
            poids_norme = elementRelationJson["weight_normed"]

            if node1  == idTerme: 
                #c'est une relation sortante
                toutesLesRelations[nomRelation]["sortant"][node2] = {"weight" : poids,  "weight_normed" : poids_norme}
            
            else:
                #c'est une relation entrante
                toutesLesRelations[nomRelation]["entrant"][node1] = {"weight" : poids,  "weight_normed" : poids_norme}
        

    

    for nomRelation, dico in toutesLesRelations.items():
        with open(directoryExploitable + nomRelation + ".json", 'w') as fichier:
            fichier.write(json.dumps(dico, indent=4, ensure_ascii=False))
            print( nomRelation + " enregistrée")


"""















# ça c'était pour le rt.json et le nt.json, je les garde au cas où j'efface les fichiers sans faire exprès
"""
#on s'en sert une fois pour toutes les relations mais maintenant on s'en fout
#
def rtjson_vers_rtExploitable(nomTerme):
    # Charger le JSON
    with open(nomTerme, 'r') as fichier:
        objet_json = json.load(fichier)
    
    # Initialiser le dictionnaire résultant
    dictionnaireRT = {}
    
    # Parcourir chaque élément de la liste JSON
    for element in objet_json:
        rtid = int(element["rtid"])
        name = element["name"]
        dictionnaireRT[name] = rtid
        dictionnaireRT[rtid] = name
    
    return dictionnaireRT


dico = rtjson_vers_rtExploitable("res/fichiersTraites/rt.json")
dicoJson = json.dumps(dico, indent=4)

with open("res/fichiersExploitables/rt.json", 'w') as fichier:
            fichier.write(dicoJson)
            print("fichier enregistré")
"""


"""
def ntjson_vers_dictionnaire_nom_ntid(nomTerme):
    # Charger le JSON
    with open(nomTerme, 'r') as fichier:
        objet_json = json.load(fichier)
    
    # Initialiser le dictionnaire résultant
    dictionnaire_nom_rtid = {}
    
    # Parcourir chaque élément de la liste JSON
    for element in objet_json:
        rtid = int(element["ntid"])
        name = element["name"]
        dictionnaire_nom_rtid[name] = rtid
    
    return dictionnaire_nom_rtid


"""

