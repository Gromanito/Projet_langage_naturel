import requests
from bs4 import BeautifulSoup
import os
import json

import traitementJson

"""
récupère les données des fichiers json pour pouvoir les manipuler facilement


"""



def recupBaseBrut(nom, convertirEnJson=False):

	"""récupère le texte depuis Jeuxdemots et l'enregistre tel quel en txt
	 pour pas avoir à le retélécharger
	 
	 renvoie True si le texte a bien été récupéré
	 """


	nom_fichier_brut = "res/fichiersBruts/"+nom+".txt"

	if os.path.exists(nom_fichier_brut):
		print("Le fichier existe déjà.")
		return True

	
	url = "https://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=" + nom + "&rel="
	response = requests.get(url)
	
	
	if response.status_code == 200:
		# Parse le contenu HTML de la page
		soup = BeautifulSoup(response.text, 'html.parser')
		
		code_tags = soup.find('code')
		
		code_text = code_tags.get_text()

		print(code_text)
		
		with open(nom_fichier_brut, 'w', encoding='utf-8') as fichier:
			fichier.write(code_text)
			print("fichier brut enregistré")


		#enregistre le fichier sous format json
		if convertirEnJson:
			traitementJson.enregistrer_en_json(nom, code_text)
			
		return True
	
	else:
		print("Erreur lors de la requête HTTP:", response.status_code)
		return False



"""
#recupBaseBrut("hibiscus")


with open("res/fichiersBruts/hibiscus.txt", 'r', encoding='utf-8') as fichier:
	chaine = fichier.read()
	enregistrer_en_json("hibiscus", chaine)
"""     



	





