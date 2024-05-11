import json
import recupDonnees

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
			"r_processus>agent-1":"r_processus>agent"
			}



# UTILISATION : mettre @timing comme annotation d'une fonction
def timing(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        print("Durée d'exécution : {:1.3}s".format(end_time - start_time))
    return wrapper



def recup_elements(source, termeId, relation, entrant=False, nombreLimite=-1 ):
	elements = {}
	sens = "entrant" if entrant else "sortant"
	termeId=str(termeId)
	try:
		for noeud, poids in source[relation][sens].items():
			
			if noeud != termeId:
				
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

	nouveauPoidsIntermediaire = poidsIntermediaire * (importancePoidsIntermediaire * float(scores[0])) 
	nouveauPoidsInference =poidsInference * (importancePoidsInference * float(scores[1]))


	return nouveauPoidsIntermediaire * nouveauPoidsInference








def inference_triangle(inferenceJSON, intermediaires, elements_inference, terme1, relation, terme2, relationsTerme1, relationsTerme2, edges, besoinTelechargement ):
	
	
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

		#on doit télécharger chaque terme intermédiaire (relou)
		for intermediaire, poids_intermediaireJSON in intermediaires.items():
			nodesIntermediaire, relationsIntermediaire = recupDonnees.recupExploitable(edges[intermediaire]["name"])
			
			#on a l'exploitable, on récup ce qu'on a à récup
			sortantsIntermediaire = recup_elements(relationsIntermediaire, nodesIntermediaire["id"], ligneInference[1], nombreLimite = 5)

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
	
	resultat = [[inferenceJSON, terme1, relation, terme2, inf[0], inf[1]] for inf in listeInference[0:nbrInfAMontrer]]

	return resultat












def inference_generique_triangle(terme1, relationsTerme1, typeRelation, terme2, relationsTerme2, edges, nombreInferences=3):
	"""
	inférences qu'on a "trouvées"
	"""

	with open("src/schema_inference.json", 'r') as fichier:
		dico = json.load(fichier)
	
	inferences = dico["triangle"]["all"]
	if (dico["triangle"].get(typeRelation) != None):
		inferences += dico["triangle"][typeRelation]
		

	listeInference = []
	#pour chaque inférence possible sur cette relation
	for inferenceJSON in inferences:

		A = terme1
		B = terme2

		#on s'occupe de récupérer les éléments "intermédiaires"
		ligneC = inferenceJSON["C"].split(";")
		
		source, relation = ligneC[0], ligneC[1]

		if relation=='rt':
			relation = typeRelation

		
		if source == "A":
			C = recup_elements( relationsTerme1, relationsTerme1["id"], relation, nombreLimite=20)
		else:
			C = recup_elements( relationsTerme2, relationsTerme2["id"], relation, nombreLimite=20)


		if C is not None:
			#une fois qu'on les a, on regarde quels intermédiaires sont liés avec le terme en question
			ligneInference = inferenceJSON["inference"].split(";")
			gauche, relationInf, droite = ligneInference[0], ligneInference[1], ligneInference[2]

			if relationInf=='rt':
				relationInf = typeRelation

			# au lieu de prendre les sortants de C (nécessite de télécharger chaque terme) 
			# on regarde plutôt les entrants de B (ou A) avec le conversif

			if conversifs.get(relationInf) is None:
				# dans le cas où on est obligé de télécharger (pire des cas mais tant pis)
				listeInference += inference_triangle(inferenceJSON, C, None, A, typeRelation, B, relationsTerme1, relationsTerme2, edges, True )

			else:
				if gauche == 'C':
					relationInf = conversifs[relationInf]
					gauche, droite = droite, gauche
			
				#on a le C à droite, on regarde quel trucs récup avec quelles relations
				if gauche == 'A':
					elements_inference = recup_elements(relationsTerme1, relationsTerme1["id"], relationInf)
				else:
					elements_inference = recup_elements(relationsTerme2, relationsTerme2["id"], relationInf)
				
				#si y a aucun noeud pour cette relation (soit y en pas dans jeux de mot, soit je l'ai mal téléchargé (jsp pk))
				if elements_inference is not None:
					#on a récupéré les éléments qu'il nous faut, maintenant on affiche l'inférence
					listeInference += inference_triangle(inferenceJSON, C, elements_inference, A, typeRelation, B, relationsTerme1, relationsTerme2, edges, False )


	#on a fait toutes nos inférences, mtn on les affiche dans l'ordre
	
	listeInference.sort(key=lambda x:x[5], reverse=True)
	
	if len(listeInference) > 0:

		print("\n\n\n\n\n")
		#y a au moins une inférence (ouf)
		maxScore = listeInference[0][5]
		for inf in listeInference:
			if inf[5] > 0.05 * maxScore:
				#on garde pas les inférences trop nulles
				print_inference_triangle(inf)
	





























		

			
#inférence en dur à la main, on gère maintenant avec des formats json



"""
def inference_deductive(terme1, relationsTerme1, typeRelation, terme2, relationsTerme2, edges, nombreInferences=3):
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
	conversifDeLaRelation = conversifs.get(typeRelation)
	
	if conversifDeLaRelation is None:
		lesEntrantsDeTerme2 = [entrants for entrants in relationsTerme2[typeRelation]["entrant"].keys()]
	else:
		lesEntrantsDeTerme2 = [sortant for sortant in relationsTerme2[conversifDeLaRelation]["sortant"].keys()]
	
	
	print("\ninférence déductive : ")
	for generique in lesMeilleuresGeneriquesDeTerme1:
		if generique in lesEntrantsDeTerme2:

			#générique est un identifiant, on récupère le nom associé
			print("\toui car      " + terme1 +  " r_isa " + edges[generique]["name"] + "     et     "   + edges[generique]["name"] + " " + typeRelation + " " + terme2)
	

	






def inference_deductive_inversee(terme1, relationsTerme1, typeRelation, terme2, relationsTerme2, edges, nombreInferences=3):

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
	

	lesSortantsDeTerme1 = [sortant for sortant in relationsTerme1[typeRelation]["sortant"].keys()]

	print("\ninférence déductive inversée : ")
	for generiqueTerme2 in lesGeneriquesDeTerme2:
		if generiqueTerme2 in lesSortantsDeTerme1:
			print("\toui car      " + terme2 +  " r_isa " + edges[generiqueTerme2]["name"] + "     et     "   + terme1 + " " + typeRelation + " " + edges[generiqueTerme2]["name"] )
	
	print("\n")




def inference_transitive(terme1, relationsTerme1, typeRelation, terme2, relationsTerme2, edges, nombreInferences=3):
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
	for trucTransitif, poids in relationsTerme1[typeRelation]["sortant"].items():
		lesMeilleursTrucsTransitifs.append(trucTransitif)

		if len(lesMeilleursTrucsTransitifs) >= nombreInferences:
			break


	#si la relation a un inverse, on le prend (on préfère celui là que les entrants de terme2)
	global conversifs
	conversifDeLaRelation = conversifs.get(typeRelation)
	
	if conversifDeLaRelation is None:
		lesEntrantsDeTerme2 = [entrants for entrants in relationsTerme2[typeRelation]["entrant"].keys()]
	else:
		lesEntrantsDeTerme2 = [sortant for sortant in relationsTerme2[conversifDeLaRelation]["sortant"].keys()]


	print("\ninférence transitive")
	
	for trucTransitif in lesMeilleursTrucsTransitifs:
		if trucTransitif in lesEntrantsDeTerme2:
			#trucTransitif est un identifiant, on récupère le nom associé
			print("\t" + "oui car      " + terme1 +  " " + typeRelation + " " + edges[trucTransitif]["name"] + "     et     "   + edges[trucTransitif]["name"] + " " + typeRelation + " " + terme2)
	print("\n")









	
def inference_inductive(terme1, relationsTerme1, typeRelation, terme2, relationsTerme2, edges, nombreInferences=3):
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
	conversifDeLaRelation = conversifs.get(typeRelation)
	
	if conversifDeLaRelation is None:
		lesEntrantsDeTerme2 = [entrants for entrants in relationsTerme2[typeRelation]["entrant"].keys()]
	else:
		lesEntrantsDeTerme2 = [sortant for sortant in relationsTerme2[conversifDeLaRelation]["sortant"].keys()]
	


	print("\ninférence inductive : ")
	for specifique in lesMeilleursSpecifiques:
		if specifique in lesEntrantsDeTerme2:

			#specifique est un identifiant, on récupère le nom associé
			print("\t" + "oui car      " + terme1 +  " r_hypo " + edges[specifique]["name"] + "     et     "   + edges[specifique]["name"] + " " + typeRelation + " " + terme2)
	print("\n")

"""
