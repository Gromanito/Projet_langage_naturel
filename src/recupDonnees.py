from requests_html import HTMLSession
import os
import json

import traitementJson



#je sais faut pas mettre des variables globales mais on la touchera pas et j'ai pas envie de mettre un paramètre en plus dans absolument chaque fonction donc c'est bien comme ça



# """
# récupère les données des fichiers json pour pouvoir les manipuler facilement



# """


def takeRawData(word: str, rtJSON=None, relationString=None,) -> str:
    """
        récupère le fichier du terme tel quel, en dur (pour pas avoir à le retélécharger)
    """

    
    fileName = "res/fichiersBruts/"+ word + ".txt" if relationString==None else "res/fichiersBruts/"+ word + relationString  + ".txt"
    texteBrut = None

    if not os.path.exists(fileName):
        #le mot n'a pas déjà été téléchargé, on le fait

        nombreEssai = 3

        #préparation de l'URL
        if rtJSON == None:
            with open("res/fichiersExploitables/rt.json", 'r') as fichier:
                rtJSON = json.load(fichier)

        url = 'https://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel='+word.replace(' ','+')+'&rel='\
        
        if relationString != None:
            url = url + str(rtJSON[relationString])


        while nombreEssai > 0:
            

            this_session = HTMLSession()
            response = this_session.get(url)
            

            #requête internet (ancien)
            #response = requests.get(url)

            #la requête a échoué
            if response.status_code != 200:
                #print("La requête a échoué avec le code :", response.status_code)
                nombreEssai -= 1
                if nombreEssai == 0:
                    return "EchecRequete"


            else:
                # la requête a réussie
                response.html.render(sleep=1, timeout=5)

                # affiche le texte de la page (pas le html) donc illisible)
                #texteBrut = response.html.text

                #récupère des bytes
                #texteBrut = response.html.raw_html

                #y a les accents mais tjrs pas le '>' (mettre ISO machine dans le encoding de with open)
                #texteBrut = response.html.raw_html.decode('ISO-8859-1')
                
                # c'est des bytes, pas une str
                # texteBrut = response.content

                #marche mais pas pour les accents
                # texteBrut = response.content.decode('ISO-8859-1')

                #marche juste pas 
                # texteBrut = response.content.decode('utf-8')


                #bon bah ça marche mais j'ai peur que ça fasse comme avant et que des fois on récup bien la page et des fois non (enfin on la récup mais la page est pas encore chargée quoi)
                

                
                texteBrut = response.html.raw_html.decode('utf-8')

                #on regarde si la page qu'on a reçue est bien 
                if len(texteBrut) < 6000:
                    if texteBrut.find("<CODE>MUTED_PLEASE_RESEND") > 0:
                        nombreEssai -= 1
                        texteBrut = None
                    elif texteBrut.find("n'existe pas !</div>") > 0:
                        print("le terme " + word + " semble ne pas exister")
                        return "TermeExistePas"

                    

                if texteBrut != None:
                    #on enregistre le texte brut dans un fichier
                    with open(fileName, 'w', encoding='utf-8') as fichier:
                        fichier.write(texteBrut)
                        #print("Contenu brut enregistré dans le fichier " + fileName)
                    nombreEssai = 0
        this_session.close()

    return texteBrut
        





def prepareEtRecupereLesDonneesExploitables(terme:str, dicoPrincipal:dict, relations_types=None) -> dict:

    # fonction qui récupère les données des fichiers json pour les intégrer au programme
    # (récupère les données depuis internet si besoin)
    dicoEdges = dicoPrincipal["noeuds"]
    dicoRelationsDesTermes = dicoPrincipal["relationsDesTermes"]

    nodesTerme, relationsTerme = recupExploitable(terme, relations_types)

    if nodesTerme == None or relationsTerme==None:
        #print("prblm lors de la recup des donénes")
        return False
    
    
    #on a récup les données, maintenant on les "stocke" dans notre programme
    idTerme = nodesTerme.pop("id")


    #on rajoute les noeuds
    for key, value in nodesTerme.items() :
        dicoEdges[key] = value
    
    #on rajoute les relations
    relationsTerme["id"] = str(idTerme)
    dicoRelationsDesTermes[terme] = relationsTerme

    return True






    

def recupExploitable(terme, relations_types=None):

    """
        Récupère les données exploitables (et les crée si elles n'existent pas encore)
    """
    

    filePath = "res/fichiersExploitables/"+terme+"/"


    if os.path.exists(filePath):
        #les fichiers exploitables existent déjà, on a plus qu'à les charger
        with  open(filePath + "e.json") as fichier:
            nodesTerme = json.load(fichier)
        with  open(filePath + "r.json") as fichier:
            relationsTerme = json.load(fichier)

    else:
        # les fichiers exploitables n'existent pas, on le crée
        print("préparation des données pour le terme : " + terme + "  (téléchargement, traitement ...)")

        if relations_types is None:
            with open("res/fichiersExploitables/rt.json", 'r') as fichier:
                relations_types = json.load(fichier)


        #on récup les fichiers bruts depuis internet
        chaineBruteTerme = takeRawData(terme, relations_types)
        chaineBruteHypo = takeRawData(terme, relations_types, "r_hypo")
        

        #s'il y a des problèmes lors de la récupération des données, on annule
        if chaineBruteTerme == "EchecRequete" or chaineBruteHypo == "EchecRequete":
            print("problème lors de la requête internet")
            return None, None
        
        if chaineBruteTerme == "TermeExistePas":
            print("le terme semble ne pas exister...")
            return None, None


        #on transforme le fichier brut en json
        traitementJson.enregistrer_en_json(terme, chaineBruteTerme)

        #on ajoute la relation r_hypo qui n'est pas chargé par défaut sur la page principale
        dico = traitementJson.ajouterRelationsAuJsonTraite(terme, "r_hypo")

        nodesTerme, relationsTerme = traitementJson.json_vers_exploitable(terme, dico, relations_types)
    
    return nodesTerme, relationsTerme

   



"""
def manageData(word: str, storageDir="res/fichierExploitables") :
    e_word_file = None
    r_word_file = None
        
    e_word_file = open(storageDir+'/'+word+'/e.json', 'w', encoding='utf-8')
    r_word_file = open(storageDir+'/'+word+'/r.json', 'w', encoding='utf-8') 
    
    e_word_file.write("[\n")
    r_word_file.write("[\n")





    with open(storageDir+'/'+word+'/'+word+'.txt', 'r', encoding='utf-8') as file :
        e_data = ""
        r_data = ""
        for line in file :
            data = line.split(';')
            label = label_data_json(data[0])

            if (label != None) :
                dictionnaire = {
                    label[idx]: manage_value(data[idx+1]) for idx in range(min(len(label),len(data)-1))
                }
                json_string = json.dumps(dictionnaire, ensure_ascii=False)
                if (data[0] == 'e') :
                    e_data += " "+json_string+',\n'
                elif (data[0] == 'r') :
                    r_data += " "+json_string+',\n'


        e_word_file.write(e_data[:-2]+'\n]')
        r_word_file.write(r_data[:-2]+'\n]')
"""


"""
def label_data_json(prefix_data: str) -> List[str]:
    if prefix_data == 'e' :
        return ['eid','name','type','w','formated' 'name']
    elif prefix_data == 'r' :
        return ['rid','node1','node2','type','w','w_normed','rank']  
    else : return None
"""


"""
def manage_value(value: str) -> str :
    managed_value = value.replace("'","")
    managed_value = managed_value.replace("\n","")
    try :
        managed_value = int(managed_value)
    except :
        pass
    return managed_value
"""


"""
def dispatch_RToJSON(word: str, pathToRTJSON: str, storageDir="res/fichierExploitables") -> bool:

    try :
        rt_data = None
        r_data = None
        with open(pathToRTJSON, "r", encoding="utf-8") as rt:
            rt_data = json.load(rt)
            
        rt_dico = {}
        for rt in rt_data :
            rt_dico[rt["rtid"]] = rt["trname"]

        with open(storageDir+'/'+word+'/'+'r.json', 'r', encoding='utf-8') as relations :
            r_data = json.load(relations)
            
        for rt in rt_data :
            with open(storageDir+'/'+word+'/'+rt["trname"].replace("/","_")+".json", 'w', encoding='utf-8') as f :
                f.write("[\n")
            
        for r in r_data :
            r_type = rt_dico[r["type"]]
            r_type = r_type.replace("/","_") # y a une relation qui s'appelle "r_meaning/glose". Ça fait un bug ... donc ...

            with open(storageDir+'/'+word+'/'+r_type+".json", "a") as f:
                f.writelines(" "+json.dumps(r, ensure_ascii=False)+',\n')
        
        for rt in rt_data :
            content = None
            with open(storageDir+'/'+word+'/'+rt["trname"].replace("/","_")+".json", 'r', encoding='utf-8') as f :
                content = f.read()
            
            with open(storageDir+'/'+word+'/'+rt["trname"].replace("/","_")+".json", 'w', encoding='utf-8') as f :
                f.write(content[:-2]+'\n]')

        return True 
    
    except Exception as e:
        print("Une erreur s'est produite :", e)        
        return False            
"""
    

#takeRawData("griffer")
#takeRawData("Paris")
#manageData("chien")
#dispatch_RToJSON("chien","res/fichierExploitables/rt.json")
