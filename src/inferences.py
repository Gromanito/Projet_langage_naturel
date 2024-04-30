import json

#je sais faut pas mettre des variables globales mais on la touchera pas et j'ai pas envie de mettre un paramètre en plus dans absolument chaque fonction donc c'est bien comme ça
conversifs = {"r_lieu":"r_lieu-1",\
			"r_lieu-1":"r_lieu",\
			"r_agent":"r_agent-1",\
			"r_agent-1":"r_agent",\
			"r_has_part":"r_holo",\
			"r_holo":"r_has_part"}



def inference_deductive(terme1, relationsTerme1, typeRelation, terme2, relationsTerme2, edges, nombreInferences=3):
	""" trouver un générique pour lequel la réponse est vraie

	pigeon r_agent-1 voler?
	 -> oui car      pigeon r_isa oiseau      et     oiseau r_agent-1 voler
	
	intuition de l'implémentation:
	sur cet exemple
	on récupère tous les objets x tels que pigeon r_isa x  (qu'on aura récup avec le "fichier" pigeon)
	et on regarde si on a  x r_agent-1 voler 			   (qu'on aura récup avec le "fichier" voler)
	"""
	

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

	""" trouver un générique (du terme2) pour lequel la réponse est vraie

	Terre r_agent-1 tourner autour du Soleil?
	 -> oui car      tourner autour du Soleil    r_isa    	tourner autour d'une étoile      
	 	     et     Terre     					r_agent-1 	tourner autour d'une étoile
	
	intuition de l'implémentation:
	sur cet exemple
	on récupère tous les objets x tels que tourner... r_isa x  (qu'on aura récup avec le "fichier" pigeon)
	et on regarde si on a  Terre r_agent-1 x 			   (qu'on aura récup avec le "fichier" voler)
	"""

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
	""" trouver un objet z tel que terme1Rz  et zRterme2

	chat r_lieu maison?
	 -> oui car      chat r_lieu canapé      et     canapé r_lieu maison
	
	intuition de l'implémentation:
	sur cet exemple
	on récupère tous les objets x tels que chat r_lieu   x 				 (qu'on aura récup avec le "fichier" chat)
	et on regarde si on a  					x   r_lieu maison 			   (qu'on aura récup avec le "fichier" maison)



	marche que pour les relations transitives, donc r_lieu et r_has_part (ptre d'autres?)
	"""

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
	""" trouver un spécifique pour lequel la réponse est vraie

	oiseau r_agent-1 voler?
	 -> oui car      pigeon r_isa oiseau      et     pigeon r_agent-1 voler
	
	intuition de l'implémentation:
	sur cet exemple
	on récupère tous les objets x tels que x r_isa oiseau  (qu'on aura récup avec le "fichier" oiseau)
	et on regarde si on a  x r_agent-1 voler 			   (qu'on aura récup avec le "fichier" voler)



	(en vrai c'est exactement comme l'inférence déductive mais on regarde plus les génériques, que les spécifiques)
	"""


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






def inference_generique_triangle(terme1, relationsTerme1, typeRelation, terme2, relationsTerme2, edges, nombreInferences=3):
	"""
	inférence qu'on a "trouvé"
	"""

	with open("src/schema_inference.json", 'r') as fichier:
        dico = json.load(fichier)
	
	inferences = dico["triangle"]["all"]
	inferenecs.append(dico["triangle"][typeRelation])