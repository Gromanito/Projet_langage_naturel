""" fichier temporaire"""


""" suite de fonctions qui traitent les fichiers traites json 
et les transforme en fichier json directement utilisable pour les inférences


"""

import json
import os



#fonction qui extrait le fichier json traité et crée les fichiers 
def json_vers_exploitable(nomTerme, dicoJson):

    """
    extrait le fichier json traité et crée des fichiers exploitables par
    le programme principal
    
    """


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

        for elementNoeudJson in edges:

            #y a que les noeuds "terme" qui nous intéressent (pour l'instant)
            if elementNoeudJson["node_type"] != 10:
                nodeName = elementNoeudJson["name"] if elementNoeudJson["formated_name"] is None else elementNoeudJson["formated_name"]
                nodes[elementNoeudJson["id"]] = {"name" : nodeName, "weight": elementNoeudJson["weight"]}
        
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
    for elementRelationJson in relations:
        
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
                toutesLesRelations[nomRelation]["entrant"][node2] = {"weight" : poids,  "weight_normed" : poids_norme}
        

    

    for nomRelation, dico in toutesLesRelations.items():
        with open(directoryExploitable + nomRelation + ".json", 'w') as fichier:
            fichier.write(json.dumps(dico, indent=4, ensure_ascii=False))
            print( nomRelation + " enregistrée")








def enregistrer_en_json(terme, texteBrut):
    """Enregistre la chaine brute de la page du terme au format json 
       pour pouvoir manipuler + facilement
    """

    nom_fichier_json = "res/fichiersTraites/"+terme+".json"
    dico = None


    #si le fichier n'existe pas, je fais le traitement, s'il existe déjà je fais rien
    if not os.path.exists(nom_fichier_json):
        
        if texteBrut == None:
            with open("res/fichiersBruts/"+terme+".txt") as fichier:
                texteBrut = fichier.read()


        edges=[]
        relations=[]

        #on recherche l'id de ce qu'on cherche (première ligne du texte, 
        #au lieu de regarde chaque noeud et faire des if)
        #(le code est horrible tkt)
        
        ligneQuiContientLid = texteBrut[texteBrut.find("(eid="):  texteBrut.find("(eid=") + 30 ]
        idTerme = int(ligneQuiContientLid[ligneQuiContientLid.find("(eid=") + 5 : ligneQuiContientLid.find(')')])

        for ligne in texteBrut.splitlines():
            if ligne.startswith('e;'):
                ligne = ligne.strip()
                
                nom, ligne = renvoieNameApartirDuneLigne(ligne)

                formated_name = None
                #si ça finit par ' c'est qu'à la fin c'est un formated name
                if ligne.endswith("'"):
                    ligneFormatee = ligne + ";"
                    formated_name, ligne = renvoieNameApartirDuneLigne(ligneFormatee)

                elements = ligne.split(';') 
                identifiant = int(elements[1])

                type_noeud = int(elements[2])
                weight = int(elements[3])
                
                
                edges.append({"id":identifiant, 
                                "name":nom, 
                                "node_type":type_noeud, 
                                "weight":weight, 
                                "formated_name":formated_name })
            
            elif ligne.startswith('r;'):
                
                elements = ligne.strip().split(';')
                identifiant = int(elements[1])
                node1 = int(elements[2])
                node2 = int(elements[3])
                type_relation = int(elements[4])
                weight = int(elements[5])
                weight_normed = None
                rank = None

                if len(elements) > 6: #cas où c'est les noeuds sortants
                    
                    if elements[6] != '-':
                        weight_normed =  float(elements[6])

                    if elements[7].strip() != '-':
                        rank =  int(elements[7])

                
                relations.append({  "id":identifiant, 
                                    "node1":node1, 
                                    "node2":node2, 
                                    "type":type_relation, 
                                    "weight":weight,
                                    "weight_normed": weight_normed,
                                    "rank": rank })
        
        #après la boucle for
        dico = { "id":idTerme, "r":relations, "e":edges}
        objet_json = json.dumps(dico, indent=4, ensure_ascii=False)

        
        with open(nom_fichier_json, 'w') as fichier:
            fichier.write(objet_json)
            print("fichier json enregistré")
        
    return dico



def renvoieNameApartirDuneLigne(ligne):
    indexDebut = ligne.find(";'")
    indexFin = ligne.find("';")
    name = ligne[indexDebut+2 : indexFin]
    nouvelleLigne = ligne[0 : indexDebut] + ligne[indexFin+1 :]
    return name, nouvelleLigne


"""
with open("res/fichiersBruts/chien.txt", 'r') as fichier:
            enregistrer_en_json("chien", fichier.read())
            print("pitié")
"""




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

