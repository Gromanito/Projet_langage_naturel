import json
import recupDonnees
import time

#je sais faut pas mettre des variables globales mais on la touchera pas et j'ai pas envie de mettre un paramètre en plus dans absolument chaque fonction donc c'est bien comme ça
conversifs = {"r_lieu":"r_lieu-1",\
			"r_lieu-1":"r_lieu",\
			"r_carac-1":"r_carac",\
			"r_carac":"r_carac-1",\
			"r_agent":"r_agent-1",\
			"r_agent-1":"r_agent",\
			"r_has_part":"r_holo",\
			"r_holo":"r_has_part",\
			"r_patient": "r_patient-1",\
			"r_patient-1": "r_patient",\
			"r_instr": "r_instr-1",\
			"r_instr-1": "r_instr",\
			"r_syn":"r_syn",\
			"r_own": "r_own-1",\
			"r_own-1": "r_own",\
			"r_sentiment": "r_sentiment-1",\
			"r_sentiment-1": "r_sentiment",\
			"r_lieu_action": "r_action_lieu",\
			"r_action_lieu": "r_lieu_action",\
			"r_action-verbe":"r_verbe-action",\
			"r_verbe-action":"r_action-verbe",\
			"r_processus>instr": "r_processus>instr-1",\
			"r_processus>instr-1": "r_processus>instr",\
			"r_processus>patient": "r_processus>patient-1",\
			"r_processus>patient-1": "r_processus>patient",\
			"r_processus>agent":"r_processus>agent-1",\
			"r_processus>agent-1":"r_processus>agent",\
			"r_has_conseq": "r_has_causatif",\
			"r_has_causatif": "r_has_conseq"
			}



# UTILISATION : mettre @timing comme annotation d'une fonction
def timing_inference(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        print("\nDurée d'exécution : {:1.3}s\n\n".format(end_time - start_time))
    return wrapper



def recup_elements(source, termeId, relation, entrant=False, prendrePoidsNegatifs=True, nombreLimite=-1 ):
	elements = {}
	sens = "entrant" if entrant else "sortant"
	termeId=str(termeId)
	try:
		for noeud, poids in source[relation][sens].items():
			
			if noeud != termeId:
				
				if poids["weight"] > 0 or prendrePoidsNegatifs:
					elements[noeud]= poids
				
				if nombreLimite > 0 and len(elements) > nombreLimite:
					break
	
		return elements	
	
	except KeyError:
		return None
		

def print_inference_triangle(inference ):
	# (inferenceJSON, terme1, relation, terme2, intermediaire, score)
	inferenceJSON = inference[0]
	A = inference[1]
	B = inference[3]
	C = inference[4]
	score = inference[5]


	ligneC = inferenceJSON["C"].split(";")
	ligneInference = inferenceJSON["inference"].split(";")
	

	if ligneInference[1] == "rt":
		ligneInference[1] = inference[2]

	
	if ligneC[0] == 'A':
		chaineJustification = A
	else:
		chaineJustification = B

	if score < 0:
		reponse = "non"
	else:
		reponse = "oui"
	
	chaineJustification += ' ' + ligneC[1] + " " + C + " & "

	if ligneInference[0] == 'A':
		chaineJustification += A
	elif ligneInference[0] == 'B':
		chaineJustification += B
	elif ligneInference[0] == 'C':
		chaineJustification += C

	chaineJustification += ' ' + ligneInference[1] + ' '
	
	if ligneInference[2] == 'A':
		chaineJustification += A
	elif ligneInference[2] == 'B':
		chaineJustification += B
	elif ligneInference[2] == 'C':
		chaineJustification += C
	
	print("|".join([reponse,chaineJustification,str(score)]))




def calcul_score_triangle(inferenceJSON, poids_intermediaireJSON, poids_inferenceJSON):
	# calcul des scores (un peu bizarre mais ça marche pas trop mal)
	#l'idée : on met des poids sur les poids 
	# par exemple pour chat r_agent-1 griffer :   dans cette inférence, c'est quoi le + important? 
	# que       chat r_isa x    ou que      x r_agent-1 griffer    ?
	
	scores = inferenceJSON["score"].split(";")
	poidsIntermediaire = poids_intermediaireJSON["weight"]
	poidsInference = poids_inferenceJSON["weight"]


	#si y a un poids négatif, on s'arrête là (peur de faire une div par zéro ou quoi)
	if poidsIntermediaire < 0 or poidsInference < 0:
		return min(poidsIntermediaire, poidsInference)


	importancePoidsIntermediaire = poidsIntermediaire / (poidsIntermediaire + poidsInference) 
	importancePoidsInference =         poidsInference / (poidsIntermediaire + poidsInference) 

	nouvelleImportancePoidsIntermediaire = importancePoidsIntermediaire * float(scores[0])
	nouvelleImportancePoidsInference = importancePoidsInference * float(scores[1])
	
	
	nouveauPoidsIntermediaire = nouvelleImportancePoidsIntermediaire * poidsIntermediaire
	nouveauPoidsInference = nouvelleImportancePoidsInference * poidsInference


	return round(nouveauPoidsIntermediaire * nouveauPoidsInference)








def inference_triangle(inferenceJSON, intermediaires, elements_inference, terme1, relation, terme2, dicoPrincipal, besoinTelechargement ):
	
	relationsTerme1 = dicoPrincipal["relationsDesTermes"][terme1]
	relationsTerme2 = dicoPrincipal["relationsDesTermes"][terme2]
	edges = dicoPrincipal["noeuds"]
	scores = inferenceJSON["score"].split(";")
	ligneInference = inferenceJSON["inference"].split(";")
	
	if ligneInference[1] == "rt":
		ligneInference[1] = relation
	
	listeInference=[]

	if not besoinTelechargement:
		#on a pas besoin de télécharger les termes intermédiaires (ouf)
		for intermediaire, poids_intermediaireJSON in intermediaires.items():
			if intermediaire in elements_inference.keys():

				#intermediaire est un identifiant, on récupère le nom associé
				C = edges[intermediaire]["name"]
				score_inference = calcul_score_triangle(inferenceJSON, poids_intermediaireJSON, elements_inference[intermediaire] )

				listeInference.append([C, score_inference ])


	else:

		compteur = 0 #c'est moche je sais

		#on doit télécharger chaque terme intermédiaire (relou)
		for intermediaire, poids_intermediaireJSON in intermediaires.items():

			
			#c'est pour pas qu'on télécharge trop non plus t'as capté
			compteur += 1
			if compteur > 3:
				break

			nodesIntermediaire, relationsIntermediaire = recupDonnees.recupExploitable(edges[intermediaire]["name"])
			
			#on a l'exploitable, on récup ce qu'on a à récup
			sortantsIntermediaire = recup_elements(relationsIntermediaire, nodesIntermediaire["id"], ligneInference[1])

			if sortantsIntermediaire is not None:
				for sortantIntermediaire, poids_sortant_intermediaire in sortantsIntermediaire.items():

					terme = terme1 if ligneInference[2]=='A' else terme2
					if sortantIntermediaire == terme:
						#on a trouvé une inférence
						
						#intermediaire est un identifiant, on récupère le nom associé
						C = nodesIntermediaire[intermediaire]["name"]

						score_inference = calcul_score_triangle(inferenceJSON, poids_intermediaireJSON, poids_sortant_intermediaire )
						
						listeInference.append([C, score_inference ])


	# on a fabriqué nos inférences, on choisit les meilleures
	
	nbrInfAMontrer = inferenceJSON["nombreInf"]
	
	resultat = [[inferenceJSON, terme1, relation, terme2, inf[0], inf[1]] for inf in listeInference]


	if resultat:	
		resultat.sort(key=lambda x:x[5], reverse=True)
		
		
		#si le pire score est négatif, on le retourne
		if resultat[-1][5] < 0:
			return [resultat[-1]]
		else:
			return resultat[0:nbrInfAMontrer]

	else:
		return []











@timing_inference
def inference_generique_triangle(terme1, rt, terme2, dicoPrincipal):
	"""
	inférences qu'on a "trouvées"
	"""

	print("\n\n\nInférences triangles\n")

	
	edges = dicoPrincipal["noeuds"]
	relationsTerme1 = dicoPrincipal["relationsDesTermes"][terme1]
	relationsTerme2 = dicoPrincipal["relationsDesTermes"][terme2]

	with open("src/schema_inference.json", 'r') as fichier:
		dico = json.load(fichier)
	
	inferences = dico["triangle"]["all"]
	if (dico["triangle"].get(rt) != None):
		inferences += dico["triangle"][rt]
		

	listeInference = []
	#pour chaque inférence possible sur cette relation
	for inferenceJSON in inferences:
		#print(inferenceJSON)
		A = terme1
		B = terme2

		#on s'occupe de récupérer les éléments "intermédiaires"
		ligneC = inferenceJSON["C"].split(";")
		
		source, relation = ligneC[0], ligneC[1]

		if relation=='rt':
			relation = rt

		
		if source == "A":
			C = recup_elements( relationsTerme1, relationsTerme1["id"], relation, prendrePoidsNegatifs=False, nombreLimite=20)
		else:
			C = recup_elements( relationsTerme2, relationsTerme2["id"], relation, prendrePoidsNegatifs=False, nombreLimite=20)

		#print(C)
		if C is not None:
			#une fois qu'on les a, on regarde quels intermédiaires sont liés avec le terme en question
			ligneInference = inferenceJSON["inference"].split(";")
			gauche, relationInf, droite = ligneInference[0], ligneInference[1], ligneInference[2]

			if relationInf=='rt':
				relationInf = rt

			# au lieu de prendre les sortants de C (nécessite de télécharger chaque terme) 
			# on regarde plutôt les entrants de B (ou A) avec le conversif
			global conversifs
			yAunConversif = conversifs.get(relationInf) is not None
							
			if gauche == 'C':
				#on regarde d'abord les entrants vers B
				if droite == 'A':
					elements_inference = recup_elements(relationsTerme1, relationsTerme1["id"], relationInf, entrant=True)
				else:
					elements_inference = recup_elements(relationsTerme2, relationsTerme2["id"], relationInf, entrant=True)

				if elements_inference:
					listeInference += inference_triangle(inferenceJSON, C, elements_inference, A, rt, B, dicoPrincipal, False )
					continue


				#si y a pas, on teste les sortants sur le conversifs
				if yAunConversif:
					relationInf = conversifs[relationInf]
					gauche, droite = droite, gauche
				else:
					listeInference += inference_triangle(inferenceJSON, C, None, A, rt, B, dicoPrincipal, True )
					continue 
					#on a fini avec cette inférence, faut pas qu'on passe dans l'autre truc
		
			#on a le C à droite, on regarde quel trucs récup avec quelles relations
			if gauche == 'A':
				elements_inference = recup_elements(relationsTerme1, relationsTerme1["id"], relationInf)
			else:
				elements_inference = recup_elements(relationsTerme2, relationsTerme2["id"], relationInf)
			
			#si y a aucun noeud pour cette relation (soit y en pas dans jeux de mot, soit je l'ai mal téléchargé (jsp pk))
			if elements_inference is not None:
				#on a récupéré les éléments qu'il nous faut, maintenant on affiche l'inférence
				listeInference += inference_triangle(inferenceJSON, C, elements_inference, A, rt, B, dicoPrincipal, False )


	#on a fait toutes nos inférences, mtn on les affiche dans l'ordre
	
	listeInference.sort(key=lambda x:x[5], reverse=True)
	#print(listeInference)

	if len(listeInference) > 0:

		#y a au moins une inférence (ouf)
		maxScore = listeInference[0][5]
		for inf in listeInference:
			if inf[5] > 0.05 * maxScore or inf[5] < 0:
				#on garde pas les inférences trop nulles
				print_inference_triangle(inf)
	
	else:
		print("Aucune inférence trouvée")
	















def print_inference_carre(inferenceJSON, terme1, rt, terme2, C, D, score):

	ligneC = inferenceJSON["C"].split(";")
	ligneD = inferenceJSON["D"].split(";")
	ligneInference = inferenceJSON["inference"].split(";")
	
	A = terme1
	B = terme2

	if ligneInference[1] == "rt":
		ligneInference[1] = rt
	if ligneC[1] == "rt":
		ligneC[1] = rt
	if ligneD[1] == "rt":
		ligneD[1] = rt


	if score < 0:
		reponse = "non"
	else:
		reponse = "oui"

	

	if ligneC[0] == 'A':
		chaineJustification = A
	else:
		chaineJustification = B

	
	chaineJustification += ' ' + ligneC[1] + " " + C + " & "


	if ligneD[0] == 'A':
		chaineJustification += A
	elif ligneD[0] == 'B':
		chaineJustification += B
	else:
		chaineJustification += C

	chaineJustification += ' ' + ligneD[1] + " " + D + " & "


	if ligneInference[0] == 'A':
		chaineJustification += A
	elif ligneInference[0] == 'B':
		chaineJustification += B
	elif ligneInference[0] == 'C':
		chaineJustification += C
	elif ligneInference[0] == 'D':
		chaineJustification += D

	chaineJustification += ' ' + ligneInference[1] + ' '
	
	if ligneInference[2] == 'A':
		chaineJustification += A
	elif ligneInference[2] == 'B':
		chaineJustification += B
	elif ligneInference[2] == 'C':
		chaineJustification += C
	elif ligneInference[2] == 'D':
		chaineJustification += D
	
	print("|".join([reponse,chaineJustification,str(score)]))





def calcul_score_carre(inferenceJSON, poidsCjson, poidsDjson, poids_inference):
	
	# calcul des scores (un peu bizarre mais ça marche pas trop mal)
	#l'idée : on met des poids sur les poids 
	# par exemple pour chat r_agent-1 griffer :   dans cette inférence, c'est quoi le + important? 
	# que       chat r_isa x    ou que      x r_agent-1 griffer    ?
	
	scores = inferenceJSON["score"].split(";")
	poidsC = poidsCjson["weight"]
	poidsD = poidsDjson["weight"]
	poidsInf = poids_inference["weight"]


	#si y a un poids négatif, on s'arrête là (peur de faire une div par zéro ou quoi)
	if poidsC < 0 or poidsD < 0 or poidsInf < 0:
		return min(min(poidsC, poidsD), poidsInf)


	importancePoidsC = poidsC / (poidsC + poidsD + poidsInf) 
	importancePoidsD = poidsD / (poidsC + poidsD + poidsInf) 
	importancePoidsInf = poidsInf / (poidsC + poidsD + poidsInf) 

	nouvelleImportancePoidsC = importancePoidsC * float(scores[0])
	nouvelleImportancePoidsD = importancePoidsD * float(scores[1])
	nouvelleImportancePoidsInf = importancePoidsInf * float(scores[2])

	nouveauPoidsC = nouvelleImportancePoidsC * poidsC
	nouveauPoidsD = nouvelleImportancePoidsD * poidsD
	nouveauPoidsInf = nouvelleImportancePoidsInf * poidsInf
	
	return round( nouveauPoidsC * nouveauPoidsD * nouveauPoidsInf )









def map_C_vers_D(noeudsC, relationD, dicoPrincipal, entrant=False, nombreLimite=3 ):
	# (pour l'inférence carré) dans le cas où on récupère D depuis C, faut télécharger + gérer les poids ...
	sens = "entrant" if entrant else "sortant"
	dico = {}
	edges = dicoPrincipal["noeuds"]

	for noeud, poids in noeudsC.items():
		noeudTermeC, relationTermeC = recupDonnees.recupExploitable(edges[noeud]["name"])

		#à faire : quand je récupère les D ce sont des identifiants, comment faire pour avoir leurs noms? vu qu'on les a pas stocké dans les edges
		dico[noeud] = {	"edgesC":noeudTermeC,\
						"poidsC":poids,\
						"noeudD":recup_elements(relationTermeC, edges[noeud], relationD, prendrePoidsNegatifs=False,)}

		if len(dico)>nombreLimite:
			break
	
	return dico




def inference_carre_chiantos(terme1, rt, terme2, C, inferenceJSON, dicoPrincipal):

	# D contient une "liste chaînée" avec les éléments atteints pour chaque C
	# on regarde, à partir de chaque C, si y a en D tel que D rt B

	ligneD = inferenceJSON["D"].split(";")
	ligneInference = inferenceJSON["inference"].split(";")
	nbrInfAMontrer = inferenceJSON["nombreInf"]

	relationsTerme1 = dicoPrincipal["relationsDesTermes"][terme1]
	relationsTerme2 = dicoPrincipal["relationsDesTermes"][terme2]
	
	
	CversD = map_C_vers_D(C, ligneD[1], dicoPrincipal)

	listeInference = []

	if len(CversD) > 0:
		
		#j'ai récupéré C puis j'ai récupéré D, je fais l'inférence
		global conversifs
		gauche, relationInf, droite = ligneInference[0], ligneInference[1], ligneInference[2]

		if relationInf=='rt':
			relationInf = rt
		yAunConversif = conversifs.get(relationInf) is not None


		if gauche=='D':
			if yAunConversif:
				relationInf = conversifs[relationInf]
				gauche, droite = droite, gauche
			else:
				#si faut retélécharger tous les termes qu'on a depuis C, c'est bcp trop long donc on fait pas
				#(peut invalider certaines inférences dans le fichier schema_inference.json)
				return []
		

		#normalement ça peut pas être A mais bon...
		if gauche == 'A':
			elements_inference = recup_elements(relationsTerme1, relationsTerme1["id"], relationInf)
		else:
			elements_inference = recup_elements(relationsTerme2, relationsTerme2["id"], relationInf)
		
		#si y a aucun noeud pour cette relation (soit y en pas dans jeux de mot, soit je l'ai mal téléchargé (jsp pk))
		if elements_inference is not None:
			for idNoeudC, infoC  in CversD.items():
				for noeudD, poidsD in infoC["noeudD"].items():
					if noeudD in elements_inference.keys():
						edgesC = infoC["edgesC"]
						C = edgesC[str(edgesC["id"])]["name"]
						D = edgesC[noeudD]["name"]

						scoreInf = calcul_score_carre(inferenceJSON, infoC["poidsC"], poidsD, elements_inference[noeudD])
						#je viens de trouver 2 intermédiaires qui vont bien, on fait l'inférence

						listeInference.append( [inferenceJSON, terme1, rt, terme2, C, D, scoreInf] )


	if listeInference:
		listeInference.sort(key=lambda x:x[6], reverse=True)
	
		#si le pire score est négatif, on le retourne
		if listeInference[-1][6] < 0:
			return [listeInference[-1]]
		else:
			return listeInference[0:nbrInfAMontrer]
	else:
		return []

			




	
	








#inférences carrées maintenant (même principe mais + chiant quand même)



@timing_inference
def inference_generique_carre(terme1, rt, terme2, dicoPrincipal):
	"""
	inférences qu'on a "trouvées"
	"""
	
	print("\n\nInférences carrés\n")

	edges = dicoPrincipal["noeuds"]
	relationsTerme1 = dicoPrincipal["relationsDesTermes"][terme1]
	relationsTerme2 = dicoPrincipal["relationsDesTermes"][terme2]

	with open("src/schema_inference.json", 'r') as fichier:
		dico = json.load(fichier)
	
	inferences = dico["carre"]["all"]
	if (dico["carre"].get(rt) != None):
		inferences += dico["carre"][rt]
		

	listeInference = []

	#pour chaque inférence possible sur cette relation
	for inferenceJSON in inferences:

		A = terme1
		B = terme2

		#on s'occupe de récupérer les éléments "intermédiaires"
		ligneC = inferenceJSON["C"].split(";")
		ligneD = inferenceJSON["D"].split(";")
		
		sourceC, relationC = ligneC[0], ligneC[1]
		sourceD, relationD = ligneD[0], ligneD[1]

		nbrInfAMontrer = inferenceJSON["nombreInf"]


		if relationC=='rt':
			relationC = rt
		if relationD=='rt':
			relationD = rt

		
		if sourceC == "A":
			C = recup_elements( relationsTerme1, relationsTerme1["id"], relationC, prendrePoidsNegatifs=False, nombreLimite=20)
			
		else:
			C = recup_elements( relationsTerme2, relationsTerme2["id"], relationC, prendrePoidsNegatifs=False, nombreLimite=20)

		if sourceD == "A":
			D = recup_elements( relationsTerme1, relationsTerme1["id"], relationD, prendrePoidsNegatifs=False, nombreLimite=20)

		elif sourceD == "B":
			D = recup_elements( relationsTerme2, relationsTerme2["id"], relationD, prendrePoidsNegatifs=False, nombreLimite=20)
		
		#cas chiantos où on doit télécharger chaque noeud....
		else:
			listeInference +=  inference_carre_chiantos(A, rt, B, C, inferenceJSON, dicoPrincipal ) 
			continue


		if C is not None and D is not None:
			listeInfSympa = []
			#une fois qu'on les a, on regarde comment se fait l'inférence
			ligneInference = inferenceJSON["inference"].split(";")
			gaucheInf, relationInf, droiteInf = ligneInference[0], ligneInference[1], ligneInference[2]

			if relationInf=='rt':
				relationInf = rt


			# puisque c'est une inférence carré, il va falloir télécharger des termes
			# je vais tt le temps télécharger les termes de gauche

			if gaucheInf == 'C':
				gauche = C 
				droite = D
			else: 
				gauche = D
				droite = C

			compteur = 0 	#c'est moche mais flemme
			for noeudGaucheID, poidsGaucheID in gauche.items():

				# c'est juste pour pas télécharger trop de truc
				compteur += 1
				if compteur > 3:
					break
				

				edgesGauche, relationsGauche = recupDonnees.recupExploitable(edges[noeudGaucheID]["name"])

				noeudsGauche = recup_elements(relationsGauche, noeudGaucheID, relationInf)

				if noeudsGauche is not None:
					for noeudGauche, poidsGauche in noeudsGauche.items():
						if noeudGauche in droite.keys():

							#on a trouvé une inférence (ouf)
							
							#je viens de trouver 2 intermédiaires qui vont bien, on fait l'inférence

							if ligneInference[0] == 'C':
								scoreInf = calcul_score_carre(inferenceJSON, gauche[noeudGaucheID], droite[noeudGauche], poidsGauche)
								termeC = edges[noeudGaucheID]["name"]
								termeD = edges[noeudGauche]["name"]
							
							else:
								scoreInf = calcul_score_carre(inferenceJSON, droite[noeudGauche], gauche[noeudGaucheID], poidsGauche)
								termeC = edges[noeudGaucheID]["name"]
								termeD = edges[noeudGauche]["name"]

							listeInfSympa.append([inferenceJSON, terme1, rt, terme2, termeC, termeD, scoreInf])
		
			#on a nos inférences carrés sur cette inférence JSON, on les garde les meilleures / les négatives
			if listeInfSympa:
				listeInfSympa.sort(key=lambda x:x[6], reverse=True)
			
			
				#si le pire score est négatif, on le retourne
				if listeInfSympa[-1][6] < 0:
					listeInference += [listeInfSympa[-1]]
				else:
					listeInference += listeInfSympa[0:nbrInfAMontrer]

	#on a fait toutes nos inférences, mtn on les affiche dans l'ordre
	
	listeInference.sort(key=lambda x:x[6], reverse=True)
	
	if listeInference:

		#y a au moins une inférence (ouf)
		maxScore = listeInference[0][6]
		for inf in listeInference:
			if inf[6] > 0.05 * maxScore or inf[6] < 0:
				#on garde pas les inférences trop nulles
				
				print_inference_carre(inf[0], inf[1], inf[2], inf[3], inf[4], inf[5], inf[6])
	
	else:
		print("aucune inférence trouvée")
	
	










		

			
#inférence en dur à la main, on gère maintenant avec des formats json



"""
def inference_deductive(terme1, relationsTerme1, rt, terme2, relationsTerme2, edges, nombreInferences=3):
	 trouver un générique pour lequel la réponse est vraie

	pigeon r_agent-1 voler?
	 -> oui car      pigeon r_isa oiseau      et     oiseau r_agent-1 voler
	
	intuition de l'implémentation:
	sur cet exemple
	on récupère tous les objets x tels que pigeon r_isa x  (qu'on aura récup avec le "fichier" pigeon)
	et on regarde si on a  x r_agent-1 voler 			   (qu'on aura récup avec le "fichier" voler)
	
	

	#on récupère les génériques du terme 1
	lesMeilleuresGeneriquesDeTerme1 = []
	for generique, poids in relationsTerme1["r_isa"]["sortant"].items():
		lesMeilleuresGeneriquesDeTerme1.append(generique)

		if len(lesMeilleuresGeneriquesDeTerme1) >= nombreInferences:
			break




	#si la relation a un conversif, on le prend (on préfère celui là que les entrants du terme 2)
	global conversifs
	conversifDeLaRelation = conversifs.get(rt)
	
	if conversifDeLaRelation is None:
		lesEntrantsDeTerme2 = [entrants for entrants in relationsTerme2[rt]["entrant"].keys()]
	else:
		lesEntrantsDeTerme2 = [sortant for sortant in relationsTerme2[conversifDeLaRelation]["sortant"].keys()]
	
	
	print("\ninférence déductive : ")
	for generique in lesMeilleuresGeneriquesDeTerme1:
		if generique in lesEntrantsDeTerme2:

			#générique est un identifiant, on récupère le nom associé
			print("\toui car      " + terme1 +  " r_isa " + edges[generique]["name"] + "     et     "   + edges[generique]["name"] + " " + rt + " " + terme2)
	

	






def inference_deductive_inversee(terme1, relationsTerme1, rt, terme2, relationsTerme2, edges, nombreInferences=3):

	 trouver un générique (du terme2) pour lequel la réponse est vraie

	Terre r_agent-1 tourner autour du Soleil?
	 -> oui car      tourner autour du Soleil    r_isa    	tourner autour d'une étoile      
	 	     et     Terre     					r_agent-1 	tourner autour d'une étoile
	
	intuition de l'implémentation:
	sur cet exemple
	on récupère tous les objets x tels que tourner... r_isa x  (qu'on aura récup avec le "fichier" pigeon)
	et on regarde si on a  Terre r_agent-1 x 			   (qu'on aura récup avec le "fichier" voler)
	

	#on récupère les génériques du terme2
	lesGeneriquesDeTerme2 = []
	for generique, poids in relationsTerme2["r_isa"]["sortant"].items():
		lesGeneriquesDeTerme2.append(generique)
	

	lesSortantsDeTerme1 = [sortant for sortant in relationsTerme1[rt]["sortant"].keys()]

	print("\ninférence déductive inversée : ")
	for generiqueTerme2 in lesGeneriquesDeTerme2:
		if generiqueTerme2 in lesSortantsDeTerme1:
			print("\toui car      " + terme2 +  " r_isa " + edges[generiqueTerme2]["name"] + "     et     "   + terme1 + " " + rt + " " + edges[generiqueTerme2]["name"] )
	
	print("\n")




def inference_transitive(terme1, relationsTerme1, rt, terme2, relationsTerme2, edges, nombreInferences=3):
	 trouver un objet z tel que terme1Rz  et zRterme2

	chat r_lieu maison?
	 -> oui car      chat r_lieu canapé      et     canapé r_lieu maison
	
	intuition de l'implémentation:
	sur cet exemple
	on récupère tous les objets x tels que chat r_lieu   x 				 (qu'on aura récup avec le "fichier" chat)
	et on regarde si on a  					x   r_lieu maison 			   (qu'on aura récup avec le "fichier" maison)



	marche que pour les relations transitives, donc r_lieu et r_has_part (ptre d'autres?)
	

	# on récupère les sortants de terme1
	lesMeilleursTrucsTransitifs = []
	for trucTransitif, poids in relationsTerme1[rt]["sortant"].items():
		lesMeilleursTrucsTransitifs.append(trucTransitif)

		if len(lesMeilleursTrucsTransitifs) >= nombreInferences:
			break


	#si la relation a un inverse, on le prend (on préfère celui là que les entrants de terme2)
	global conversifs
	conversifDeLaRelation = conversifs.get(rt)
	
	if conversifDeLaRelation is None:
		lesEntrantsDeTerme2 = [entrants for entrants in relationsTerme2[rt]["entrant"].keys()]
	else:
		lesEntrantsDeTerme2 = [sortant for sortant in relationsTerme2[conversifDeLaRelation]["sortant"].keys()]


	print("\ninférence transitive")
	
	for trucTransitif in lesMeilleursTrucsTransitifs:
		if trucTransitif in lesEntrantsDeTerme2:
			#trucTransitif est un identifiant, on récupère le nom associé
			print("\t" + "oui car      " + terme1 +  " " + rt + " " + edges[trucTransitif]["name"] + "     et     "   + edges[trucTransitif]["name"] + " " + rt + " " + terme2)
	print("\n")









	
def inference_inductive(terme1, relationsTerme1, rt, terme2, relationsTerme2, edges, nombreInferences=3):
	 trouver un spécifique pour lequel la réponse est vraie

	oiseau r_agent-1 voler?
	 -> oui car      pigeon r_isa oiseau      et     pigeon r_agent-1 voler
	
	intuition de l'implémentation:
	sur cet exemple
	on récupère tous les objets x tels que x r_isa oiseau  (qu'on aura récup avec le "fichier" oiseau)
	et on regarde si on a  x r_agent-1 voler 			   (qu'on aura récup avec le "fichier" voler)



	(en vrai c'est exactement comme l'inférence déductive mais on regarde plus les génériques, que les spécifiques)
	


	lesMeilleursSpecifiques = []
	for specifique, poids in relationsTerme1["r_hypo"]["sortant"].items():
		lesMeilleursSpecifiques.append(specifique)

		if len(lesMeilleursSpecifiques) >= nombreInferences:
			break

	
	global conversifs
	conversifDeLaRelation = conversifs.get(rt)
	
	if conversifDeLaRelation is None:
		lesEntrantsDeTerme2 = [entrants for entrants in relationsTerme2[rt]["entrant"].keys()]
	else:
		lesEntrantsDeTerme2 = [sortant for sortant in relationsTerme2[conversifDeLaRelation]["sortant"].keys()]
	


	print("\ninférence inductive : ")
	for specifique in lesMeilleursSpecifiques:
		if specifique in lesEntrantsDeTerme2:

			#specifique est un identifiant, on récupère le nom associé
			print("\t" + "oui car      " + terme1 +  " r_hypo " + edges[specifique]["name"] + "     et     "   + edges[specifique]["name"] + " " + rt + " " + terme2)
	print("\n")

"""
