""" fichier temporaire"""


""" suite de fonctions qui traitent les fichiers traites json 
et les transforme en fichier json directement utilisable pour les inférences


"""

import json
import os



#fonction qui extrait le fichier json traité et crée les fichiers 
def json_vers_exploitable(nomTerme):

    """
    extrait le fichier json traité et crée des fichiers exploitables par
    le programme principal
    
    """

    directoryExploitable = "res/fichiersExploitables/" + nomTerme + "/"

    with open("res/fichiersTraites/" + nomTerme + ".json", 'r') as fichier:
        objet_json = json.load(fichier)
    
    #le fichier contient les noeuds et les relations

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
    

    if not os.path.exists(directoryExploitable + "e.json"):
        # on génère le fichier e.json (sans les noeuds relations )
        nodes = {}
        nodes["id"] = idTerme

        for elementJson in edges:

            #y a que les noeuds "terme" qui nous intéressent (pour l'instant)
            if elementJson["node_type"] != 10:
                nodeName = elementJson["name"] if elementJson["formated_name"] is None else elementJson["formated_name"]
                nodes[elementJson["id"]] = {"name" : elementJson["name"], "weight": elementJson["weight"]}

    if not os.path.exists(directoryExploitable + "r_isa.json"):

        # on génère les fichiers r_isa.json, r_agent-1, r_haspart... etc
        r_isa = {"superClasse":{}, "sousClasse":{}}
        r_has_part = {"contient":{}, "estContenuDans":{}}
        r_agent = {"agents":{}, "actions":{}}
        r_agent_1 = {"agents":{}, "actions":{}}
        r_lieu = {"estInclusDans":{}, "inclus":{}}
        #r_syn = {}
         # on en ajoutera d'autres + tard si besoin (j'ai vu processus agent-1,  id 137, il peut être pas mal)


        toutesLesRelations = {"r_isa" : r_isa, "r_has_part": r_has_part, "r_agent": r_agent, "r_agent-1": r_agent_1, "r_lieu" : r_lieu }

        for elementJson in relations:
            match elementJson["type"]:

                case 6: #r_isa
                    if elementJson["node1"] == idTerme:
                        r_isa["superClasse"][elementJson["node2"]] = {"weight" : elementJson["weight"],  "weight_normed" : elementJson["weight_normed"]}
                    else:
                        r_isa["sousClasse"][elementJson["node1"]] = {"weight" : elementJson["weight"],  "weight_normed" : elementJson["weight_normed"]}

                case 9: #has_part
                    if elementJson["node1"] == idTerme:
                        r_has_part["contient"][elementJson["node2"]] = {"weight" : elementJson["weight"],  "weight_normed" : elementJson["weight_normed"]}
                    else:
                        r_has_part["estContenuDans"][elementJson["node1"]] = {"weight" : elementJson["weight"],  "weight_normed" : elementJson["weight_normed"]}

                case 13: #r_agent (manger r_agent chat) , "<action> a pour agent <terme>"
                    if elementJson["node1"] == idTerme:
                        r_agent["agents"][elementJson["node2"]] = {"weight" : elementJson["weight"],  "weight_normed" : elementJson["weight_normed"]}
                    else:
                        r_agent["actions"][elementJson["node1"]] = {"weight" : elementJson["weight"],  "weight_normed" : elementJson["weight_normed"]}

                case 24: #r_agent-1 (chat r_agent-1 manger) ,  "<terme> est l'agent de <action>"
                    if elementJson["node1"] == idTerme:
                        r_agent_1["actions"][elementJson["node2"]] = {"weight" : elementJson["weight"],  "weight_normed" : elementJson["weight_normed"]}
                    else:
                        r_agent_1["agents"][elementJson["node1"]] = {"weight" : elementJson["weight"],  "weight_normed" : elementJson["weight_normed"]}


                #on fera les autres + tards


        objet_json = json.dumps(nodes, indent=4, ensure_ascii=False)
        with open( directoryExploitable + "e.json", 'w') as fichier:
            fichier.write(objet_json)
            print("noeuds enregistrés")

        for nomRelation, dico in toutesLesRelations.items():
            with open(directoryExploitable + nomRelation + ".json", 'w') as fichier:
                fichier.write(json.dumps(dico, indent=4, ensure_ascii=False))
                print( nomRelation + " enregistrée")


json_vers_exploitable("matou")



def enregistrer_en_json(nomFichier, texteBrut):
	"""Enregistre la chaine brute de la page du terme au format json 
	   pour pouvoir manipuler + facilement
	"""

	edges=[]
	relations=[]

	#on recherche l'id de ce qu'on cherche (première ligne du texte, 
	#au lieu de regarde chaque noeud et faire des if)
	#(le code est horrible tkt)
	
	ligneQuiContientLid = texteBrut[texteBrut.find("(eid="):  texteBrut.find("(eid=") + 30 ]
	idTerme = int(ligneQuiContientLid[ligneQuiContientLid.find("(eid=") + 5 : ligneQuiContientLid.find(')')])

	for ligne in texteBrut.splitlines():
		if ligne.startswith('e;'):
			elements = ligne.strip().split(';')
			identifiant = int(elements[1])
			nom = elements[2][1:-1]  # Supprimer les guillemets autour du nom
			type_noeud = int(elements[3])
			weight = int(elements[4])
			formated_name = None
			if len(elements) == 6:
				formated_name =  elements[5][1:-1]
			
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

	nom_fichier_json = "res/fichiersTraites/"+nomFichier+".json"
	with open(nom_fichier_json, 'w') as fichier:
		fichier.write(objet_json)
		print("fichier json enregistré")



"""
on s'en sert une fois pour toutes les relations mais maintenant on s'en fout

def rtjson_vers_dictionnaire_nom_rtid(nomTerme):
    # Charger le JSON
    with open(nomTerme, 'r') as fichier:
        objet_json = json.load(fichier)
    
    # Initialiser le dictionnaire résultant
    dictionnaire_nom_rtid = {}
    
    # Parcourir chaque élément de la liste JSON
    for element in objet_json:
        rtid = int(element["rtid"])
        name = element["name"]
        dictionnaire_nom_rtid[name] = rtid
    
    return dictionnaire_nom_rtid


dico = rtjson_vers_dictionnaire_nom_rtid("res/fichiersTraitesJson/rt.json")
dicoJson = json.dumps(dico, indent=4)

with open("res/fichiersExploitables/rt.json", 'w') as fichier:
			fichier.write(dicoJson)
			print("fichier enregistré")




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