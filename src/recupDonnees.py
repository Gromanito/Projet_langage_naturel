import requests
from bs4 import BeautifulSoup
import os




"""
récupère les données des fichiers json pour pouvoir les manipuler facilement



"""



def recupBaseBrut(nom, convertirEnJson=False):

	"récupère le texte et l'enregistre tel quel en txt pour pas avoir à le retélécharger"

	nom_fichier = "src/fichierBruts/"+nom+".txt"

	if os.path.exists(nom_fichier):
		print("Le fichier existe déjà.")
		return

	# URL de la page à récupérer
	url = "https://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=" + matou + "&rel="

	# Effectuer la requête HTTP pour récupérer le contenu de la page
	response = requests.get(url)

	# Vérifier si la requête a réussi (code de statut 200)
	if response.status_code == 200:
		# Parser le contenu HTML de la page
		soup = BeautifulSoup(response.text, 'html.parser')
		
		# Trouver toutes les balises <CODE>
		code_tags = soup.find('CODE')
		
		code_text = code_tag.get_text()

		
		with open(nom_fichier, 'w') as fichier:
			fichier.write(texte)
			print("fichier enregistré")

			
	else:
		print("Erreur lors de la requête HTTP:", response.status_code)



def recup


            
            

	


