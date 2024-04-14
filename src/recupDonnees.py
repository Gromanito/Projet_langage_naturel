import requests
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


        #préparation de l'URL
        if rtJSON == None:
            with open("res/fichiersExploitables/rt.json", 'r') as fichier:
                rtJSON = json.load(fichier)

        url = 'https://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel='+word.replace(' ','+')+'&rel='\
        
        if relationString != None:
            url = url + str(rtJSON[relationString])

    
        #requête internet
        response = requests.get(url)
    
        #la requête a échoué
        if response.status_code != 200:
            print("La requête a échoué avec le code :", response.status_code)
            return "EchecRequete"


        else:
            # la requête a réussie
            texteBrut = response.text


            #on regarde si le terme entré existe
            #(s'il n'existe pas la page est petite)
            if len(texteBrut) < 6000:
                print("le terme semble ne pas exister")
                return "TermeExistePas"

            #on enregistre le texte brut dans un fichier
            with open(fileName, 'w', encoding='utf-8') as fichier:
                fichier.write(texteBrut)
                print("Contenu brut enregistré dans le fichier " + fileName)
            
    return texteBrut
        


    
#ancienne fonction pour récupérer les json et les inclure dans le programme
#(on s'en sert plus)
def recupExploitable(Terme: str, edges: dict) -> dict:

    """
        Récupère les données json utiles et les transforme en dictionnaire
    """
    
    returnedDict = {}


    filePath = "res/fichiersExploitables/"+Terme+"/"
    with open(filePath+"e.json", "r", encoding="utf-8") as e_file :
        current_term_edges = json.load(e_file)

        idTerme = current_term_edges.pop("id")

        
        for key, value in current_term_edges.items() :
            edges[key] = value
    
    r_filesName = os.listdir(filePath)
    r_filesName.remove("e.json")
    for r_fileName in r_filesName :
        with open(filePath+r_fileName, "r", encoding="utf-8") as r_file :
            key = r_fileName.split('.')[0]

            returnedDict[key] = json.load(r_file)

    returnedDict["id"] = idTerme
    return returnedDict    



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
