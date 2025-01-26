
"""
ensemble des fonctions pour manipuler / traiter / charger les données de jeu de mots
"""



from requests_html import HTMLSession
import os
import json
import requests


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
                            "r_family", "r_has_conseq", "r_has_causatif",\
                            "r_pourvoyeur", "r_has_beneficiaire", "r_pos" ]


#les noeuds qui nous intéressent (pour pas trop en stocker dans le fichier traité)
idsTypesNoeudsQuonUtilise = [1, 2, 8, 9, 666, 777]


rtJSON = None
with open("res/infoNoeuds/rt.json", 'r') as fichier:
    rtJSON = json.load(fichier)




#je sais faut pas mettre des variables globales mais on la touchera pas et j'ai pas envie de mettre un paramètre en plus dans absolument chaque fonction donc c'est bien comme ça






def telecharge_fichier_brut(mot: str, relation=None) -> str:
    """
        récupère le fichier du terme tel quel, en dur (pour pas avoir à le retélécharger)
    """

    
    cheminFichier = "res/fichiersBruts/" + mot + ".txt" \
    if relation==None\
    else "res/fichiersBruts/" + mot + relation  + ".txt"
    
    texteBrut = None

    if not os.path.exists(cheminFichier):
        #le mot n'a pas déjà été téléchargé, on le fait

        nombreEssai = 3

        #préparation de l'URL
        global rtJSON
        
        url = 'https://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel='+mot.replace(' ','+')+'&rel='\
        
        if relation != None:
            url = url + str(rtJSON[relation])


        while nombreEssai > 0:
            
            this_session = HTMLSession()
            response = this_session.get(url)
            

            #la requête a échoué
            if response.status_code != 200:
                #print("La requête a échoué avec le code :", response.status_code)
                nombreEssai -= 1
                if nombreEssai == 0:
                    return "EchecRequete"


            else:
                # la requête a réussie
                response.html.render(sleep=1, timeout=5)
                
                texteBrut = response.html.raw_html.decode('utf-8')

                #on regarde si la page qu'on a reçue est bien 
                if len(texteBrut) < 6000:
                    if texteBrut.find("<CODE>MUTED_PLEASE_RESEND") > 0:
                        nombreEssai -= 1
                        texteBrut = None
                    elif texteBrut.find("n'existe pas !</div>") > 0:
                        print("le terme " + mot + " semble ne pas exister")
                        return "TermeExistePas"

                    

                if texteBrut != None:
                    #on enregistre le texte brut dans un fichier
                    with open(cheminFichier, 'w', encoding='utf-8') as fichier:
                        fichier.write(texteBrut)
                        #print("Contenu brut enregistré dans le fichier " + cheminFichier)
                    nombreEssai = 0
        this_session.close()
    
    else:
        with open(cheminFichier, 'r', encoding='utf-8') as fichier:
            texteBrut = fichier.read()

    return texteBrut






def brut_vers_json(terme, texteBrut=None, *texteBrutRelations):
    """
        Enregistre la chaine brute de la page du terme au format json 
        (pour pouvoir manipuler + facilement)
    """

    nom_fichier_json = "res/fichiersTraites/" + terme + ".json"
    dico = None
    global idsTypesNoeudsQuonUtilise

    #on fait le traitement si le fichier n'existe pas déjà
    if not os.path.exists(nom_fichier_json):
        
        #on récupère le texte brut s'il n'est pas passé en paramètre de la fonction
        if texteBrut is None:
            texteBrut = telecharge_fichier_brut(terme)
        
        #pour passer de l'identifiant d'une relation à son nom
        global rtJSON

        for texteBrutRelation in texteBrutRelations:
            texteBrut += texteBrutRelation

        # pour renseigner + tard quelles sont les relations qui existent dans ce fichier
        with open("res/infoNoeuds/relationsParTerme.json", 'r') as fichier:
            relationsParTerme = json.load(fichier)
        relationsParTerme[terme] = []


        edges={}
        relations={}
        relationsExistantes=[]



        #on récupère l'id du terme
        ligneQuiContientLid = texteBrut[texteBrut.find("(eid="):  texteBrut.find("(eid=") + 30 ]
        idTerme = ligneQuiContientLid[ligneQuiContientLid.find("(eid=") + 5 : ligneQuiContientLid.find(')')]

        #on traite chaque ligne du texte
        for ligne in texteBrut.splitlines():
            
            # si c'est un noeud
            if ligne.startswith('e;'):
                identifiant, noeud = cree_noeud_a_partir_dune_ligne(ligne)
                if noeud["nt"] in idsTypesNoeudsQuonUtilise:
                    edges[identifiant] = noeud

            #si c'est une relation
            elif ligne.startswith('r;'):
                identifiant, relation = cree_relation_a_partir_dune_ligne(ligne)

                #des fois les relations se font sur des noeuds qu'on regarde pas, il faut les filtrer
                #(on suppose que les noeuds sont remplis en premier et que donc ça produit pas d'erreurs de faire ça)
                if edges.get(relation["node1"]) is not None and edges.get(relation["node2"]) is not None:
                    relations[identifiant] = relation
            
            #on retient quelles sont les relations qui existent dans ce fichier
            elif ligne.startswith('rt;'):
                idRelationQuiExiste = ligne.split(';')[1]
                relationsExistantes.append(idRelationQuiExiste)
        

        #Parmi les relations qui existent,
        #on ne garde que les relations qui nous intéresse
        global nomsRelationsQuonUtilise

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
        with open( "res/infoNoeuds/relationsParTerme.json", 'w') as fichier:
            fichier.write(json.dumps(relationsParTerme, indent=4, ensure_ascii=False))
            #print("noeuds enregistrés")
    
    return dico





#fonction qui extrait le fichier json traité et crée les fichiers 
def json_vers_exploitable(nomTerme, dicoJson=None):

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
            if noeud["nt"] in idsTypesNoeudsQuonUtilise:
                nodes[idNoeud] = {"name" : noeud["name"], "w": noeud["w"]}
                
        
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
        global rtJSON

        #on prépare les relations qu'on doit traiter
        for nomRelation in nomsRelationsQuonUtilise:
            toutesLesRelations[nomRelation] = {"sortant":{}, "entrant":{}}
            idsRelationsATraiter.append(rtJSON[nomRelation])

        # print(idsRelationsATraiter)
        
        #on traite chaque relation
        for elementRelationJson in relations.values():
                
            #c'est une relation qui nous intéresse
            if elementRelationJson["rt"] in idsRelationsATraiter:
                # print("salut")
               
                node1 = elementRelationJson["node1"]
                node2 = elementRelationJson["node2"]
                nomRelation = rtJSON[str(elementRelationJson["rt"])]
                poids = elementRelationJson["w"]
                

                if node1  == idTerme: 
                    #c'est une relation sortante
                    toutesLesRelations[nomRelation]["sortant"][node2] = poids
                
                else:
                    #c'est une relation entrante
                    toutesLesRelations[nomRelation]["entrant"][node1] = poids
        
        #on enregistre les relations en json
        with open( directoryExploitable + "r.json", 'w') as fichier:
            fichier.write(json.dumps(toutesLesRelations, indent=4, ensure_ascii=False))
            #print("relations enregistrées")
        
    return nodes, toutesLesRelations





def recup_exploitable(terme):
    """
        fonction qui charge le terme voulu
        (le télécharge et le prépare si besoin)
    """

    cheminExploitable = "res/fichiersExploitables/" + terme + "/"
    nodesTerme = None
    relationsTerme = None


    if os.path.exists(cheminExploitable):
        #les fichiers exploitables existent déjà, on a plus qu'à les charger
        with  open(cheminExploitable + "e.json") as fichier:
            nodesTerme = json.load(fichier)
        with  open(cheminExploitable + "r.json") as fichier:
            relationsTerme = json.load(fichier)

    else:
        # les fichiers exploitables n'existent pas, on les crée
        print("préparation des données pour le terme : " + terme + "  (téléchargement, traitement ...)")



        #on récup les fichiers bruts depuis internet
        chaineBruteTerme = telecharge_fichier_brut(terme)
        chaineBruteHypo = telecharge_fichier_brut(terme, "r_hypo")
        

        #s'il y a des problèmes lors de la récupération des données, on annule
        if chaineBruteTerme == "EchecRequete" or chaineBruteHypo == "EchecRequete":
            print("problème lors de la requête internet")
            return None, None
        
        if chaineBruteTerme == "TermeExistePas":
            print("le terme semble ne pas exister...")
            return None, None


        #on transforme le fichier brut en json
        dicoTraite = brut_vers_json(terme, chaineBruteTerme, chaineBruteHypo)


        nodesTerme, relationsTerme = json_vers_exploitable(terme, dicoTraite)
    
    return nodesTerme, relationsTerme





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

    ligne = ligne.strip().replace("&gt;", ">")

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
                            "nt":type_noeud, 
                            "w":weight }
                            
            
    
            

#fonction pour créer un dictionnaire "relation" à partir d'une ligne
def cree_relation_a_partir_dune_ligne(ligne):
                
    elements = ligne.strip().split(';')

    #on récupère chaque élément de la ligne
    identifiant = elements[1]
    node1 = elements[2]
    node2 = elements[3]
    type_relation = int(elements[4])
    weight = int(elements[5])
    


    """
    encore jamais eu besoin
    #les noeuds sortants ont + d'éléments (rank et poids normé)
    if len(elements) > 6: 
        
        if elements[6] != '-':
            weight_normed =  float(elements[6])

        if elements[7].strip() != '-':
            rank =  int(elements[7])
    """ 
    
    return identifiant, { "node1":node1, 
                            "node2":node2, 
                            "rt":type_relation, 
                            "w":weight }






