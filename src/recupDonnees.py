import requests
import json
from typing import List
import os
import json

import traitementJson

# """
# récupère les données des fichiers json pour pouvoir les manipuler facilement



# """



def takeRawData(word: str, enregistrerEnJson=True) -> str:
    url = 'https://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel='+word+'&rel='
    response = requests.get(url)
    
    fileName = "res/fichiersBruts/"+ word + ".txt"
    
    if os.path.exists(fileName):
        print("Ce mot est déjà enregistré")
        return True
    

    if response.status_code != 200:
        print("La requête a échoué avec le code :", response.status_code)
        return False

    else:
        # on a réussi a récup le texte brut

        with open(fileName, 'w', encoding='utf-8') as fichier:
            fichier.write(response.text)
            print("Contenu enregistré dans le fichier " + fileName)
        
        if enregistrerEnJson:
            return traitementJson.enregistrer_en_json(word, response.text)

        else:
            return True
        


    
    


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

def label_data_json(prefix_data: str) -> List[str]:
    if prefix_data == 'e' :
        return ['eid','name','type','w','formated' 'name']
    elif prefix_data == 'r' :
        return ['rid','node1','node2','type','w','w_normed','rank']  
    else : return None
    
def manage_value(value: str) -> str :
    managed_value = value.replace("'","")
    managed_value = managed_value.replace("\n","")
    try :
        managed_value = int(managed_value)
    except :
        pass
    return managed_value


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

    

takeRawData("Paris")
#manageData("chien")
#dispatch_RToJSON("chien","res/fichierExploitables/rt.json")
