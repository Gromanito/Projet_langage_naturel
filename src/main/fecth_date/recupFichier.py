"""
fonctions pour récupérer les fichiers, les traiter, etc

"""
import requests
from bs4 import BeautifulSoup





def recupFichierTxt( nom :str):
    urlFichier = "https://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=" + nom + "&rel="


    # Envoyer une requête GET pour récupérer le contenu de la page
    response = requests.get(urlFichier)

    # Vérifier si la requête s'est bien déroulée
    if response.status_code == 200:
        # Parser le contenu HTML avec BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Trouver la balise spécifique que vous souhaitez extraire
        balise_texte = soup.find('CODE')

        # Vérifier si la balise a été trouvée
        if balise_texte:
            # Extraire le texte de la balise
            texte = balise_texte.get_text()
            
            with open( "src/res/fichiersBruts/" + nom+ '.txt', 'w', encoding='utf-8') as f:
                f.write(texte)


        else:
            print("La balise spécifiée n'a pas été trouvée.")
    else:
        print("Échec de la requête pour récupérer la page.")



def traduireTextVersJson()
