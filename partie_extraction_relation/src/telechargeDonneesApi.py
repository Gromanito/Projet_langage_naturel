"""
fichier contenant des ptites fonctions pour télécharger 
les noeuds/relations depuis l'api jdm avec requests (et non plus avec html_session)

"""

import requests
import json
import os


idsTypesNoeudsQuonUtilise = [1, 2, 4, 8, 9, 14, 666, 777]




def telecharger_noeud_by_name(nodeName):
    fileName = "noeudsJDM/fichiersTraites/{nodeName}.json"

    api_url = "https://jdm-api.demo.lirmm.fr/v0/relations/from/{node_name}".format(node_name = nodeName) 
    nodeByNameUrl = "https://jdm-api.demo.lirmm.fr/v0/node_by_name/{node_name}".format(node_name = nodeName)
    
    
    reponse = requests.get(api_url)
    reponseNode = requests.get(nodeByNameUrl)

    if reponse.status_code != 200 or reponseNode.status_code != 200:
        print ("erreur lors du téléchargement de : {nodeName}".format(nodeName = nodeName))
        return None
    
    else:
        resultatJson = reponse.json()
        resultatJson["id"] = reponseNode.json()["id"]

        # print(resultatJson)

        with open(fileName.format(nodeName = nodeName), 'w') as file:
            json.dump(resultatJson, file, indent=4, ensure_ascii=False)


        return resultatJson



def json_traite_vers_exploitable(nodeName, nodeJSON=None):
    
    fichierTraite = "/noeudsJDM/fichiersTraites/{nodeName}.json".format(nodeName = nodeName)
    directoryExploitable = "noeudsJDM/fichiersExploitables/" + nodeName + "/"

    if nodeJSON is None: #si on a pas le fichier json de l'API
        if os.path.exists(os.getcwd() + fichierTraite):
            with open (fichierTraite, 'r') as fichierTraite:
                jsonTraite = json.load(fichierTraite)
        else:
            jsonTraite = telecharger_noeud_by_name(nodeName)

    else:
        jsonTraite = nodeJSON

    
    

    # on créé le dossier Exploitable s'il n'existe pas déjà
    try:  
        os.mkdir(directoryExploitable)
    except FileExistsError:
        pass 
    except OSError as error:  
        print(error)
        return False


    edgesTraites = jsonTraite["nodes"]
    relationsTraites = jsonTraite["relations"]
    idTerme = jsonTraite["id"]

    nodes={'id': idTerme}

    #on traite chaque noeud
    for noeud in edgesTraites:
        #y a que les noeuds "terme" qui nous intéressent
        if noeud["type"] in idsTypesNoeudsQuonUtilise:
            nodes[noeud['id']] = {"n" : noeud["name"], "w": noeud["w"]}
        
        
            
    
    #on enregistre les noeuds en json
    objet_json = json.dumps(nodes, indent=4, ensure_ascii=False)
    with open( directoryExploitable + "e.json", 'w') as fichier:
        fichier.write(objet_json)
        #print("noeuds enregistrés")
    

    r_pos = {}
    r_lemma = {}
    r_raff_sem = {}
    relationsExploitables = {}

    with open( "noeudsJDM/infoNoeuds/rt.json", 'r') as fichier:
        rtJSON = json.load(fichier)
    
    for relation in rtJSON.keys():
        if not relation.isdigit():
            relationsExploitables[relation] = {"sortant": {}, "entrant": {}}


    #on traite chaque relation
    for relation in relationsTraites:
               
        node1 = relation["node1"]
        node2 = relation["node2"]
        nomRelation = rtJSON[str(relation["type"])]
        poids = relation["w"]
        

        if node1  == idTerme: 
            #c'est une relation sortante
            relationsExploitables[nomRelation]["sortant"][node2] = poids
        
        else:
            #c'est une relation entrante
            relationsExploitables[nomRelation]["entrant"][node1] = poids
        
        if nomRelation == "r_pos":
            r_pos[nodes[node2]['n']] = poids
        
        if nomRelation == "r_lemma":
            r_lemma[nodes[node2]['n']] = poids

        if nomRelation == "r_raff_sem":
            r_raff_sem[nodes[node2]['n']] = poids
    

    relationsExploitables["r_pos"]["sortant"] = r_pos
    relationsExploitables["r_lemma"]["sortant"] = r_lemma
        
    #on enregistre les relations en json
    objet_json = json.dumps(relationsExploitables, indent=4, ensure_ascii=False)
    with open( directoryExploitable + "r.json", 'w') as fichier:
        fichier.write(objet_json)
    

    #on traite le cas des r_pos
    #on veut un fichier à part avec, pour chaque 



def get_node_relations_by_name(node_name):
    with open( "noeudsJDM/fichiersExploitables/{node_name}/r.json".format(node_name = node_name), 'r') as fichier:
        objet_json = json.load(fichier)
    return objet_json

    
def get_node_by_name(node_name):
    with open( "noeudsJDM/fichiersExploitables/{node_name}/e.json".format(node_name = node_name), 'r') as fichier:
        objet_json = json.load(fichier)
    return objet_json







def telecharge_exploitable(terme):
    """
        fonction qui charge le terme voulu
        (le télécharge et le prépare si besoin)
    """

    cheminExploitable = "noeudsJDM/fichiersExploitables/" + terme + "/"
    nodesTerme = None
    relationsTerme = None



    if os.path.exists(cheminExploitable):
        return

    else:
        # les fichiers exploitables n'existent pas, on les crée
        print("préparation des données pour le terme : " + terme + "  (téléchargement, traitement ...)")

        nodeJSON = telecharger_noeud_by_name(terme)

        
        
        """
        #s'il y a des problèmes lors de la récupération des données, on annule
        if chaineBruteTerme == "EchecRequete" or chaineBruteHypo == "EchecRequete":
            print("problème lors de la requête internet")
            return None, None
        
        if chaineBruteTerme == "TermeExistePas":
            print("le terme semble ne pas exister...")
            return None, None
        """


        #on transforme le fichier brut en json
        json_traite_vers_exploitable(terme, nodeJSON)



def recup_exploitable(terme):

    cheminExploitable = "noeudsJDM/fichiersExploitables/" + terme + "/"
    

    with  open(cheminExploitable + "e.json") as fichier:
        nodesTerme = json.load(fichier)
    with  open(cheminExploitable + "r.json") as fichier:
        relationsTerme = json.load(fichier)

    
    return nodesTerme, relationsTerme



# telecharge_exploitable('animaux')
# print(get_node_relations_by_name('animaux')["r_pos"]["sortant"])