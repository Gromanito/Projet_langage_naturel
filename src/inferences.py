import json

#je sais faut pas mettre des variables globales mais on la touchera pas et j'ai pas envie de mettre un paramètre en plus dans absolument chaque fonction donc c'est bien comme ça
coercifs = {"r_lieu":"r_lieu-1",\
			"r_lieu-1":"r_lieu",\
			"r_agent":"r_agent-1",\
			"r_agent-1":"r_agent"}

def inference_deductive(terme1, relationsTerme1, typeRelation, terme2, relationsTerme2, edges, nombreInferences=5):
	""" trouver un générique pour lequel la réponse est vraie

	pigeon r_agent-1 voler?
	 -> oui car pigeon r_isa oiseau      et     oiseau r_agent-1 voler
	
	intuition de l'implémentation:
	sur cet exemple
	on récupère tous les objets x tels que pigeon r_isa x  (qu'on aura récup avec le "fichier" pigeon)
	et on regarde si on a  x r_agent-1 voler 			   (qu'on aura récup avec le "fichier" voler)
	"""
	
	lesMeilleuresGeneriques = []
	for generique, poids in relationsTerme1["r_isa"]["sortant"].items():
		if poids["weight_normed"]>0.5:
			lesMeilleuresGeneriques.append(generique)

		if len(lesMeilleuresGeneriques) >= nombreInferences:
			break



	#si la relation a un inverse, on le prend (on préfère celui là que les entrants )
	global coercifs
	coercifDeLaRelation = coercifs.get(typeRelation)
	
	if coercifDeLaRelation is None:
		lesEntrantsDeTerme2 = [entrants for entrants in relationsTerme2[typeRelation]["entrant"].keys()]
	else:
		lesEntrantsDeTerme2 = [sortant for sortant in relationsTerme2[coercifDeLaRelation]["sortant"].keys()]


	print("\ninférence déductive : ")
	for generique in lesMeilleuresGeneriques:
		if generique in lesEntrantsDeTerme2:

			#générique est un identifiant, on récupère le nom associé
			print("\toui car " + terme1 +  " " + "r_isa" + " " + edges[generique]["name"] + " et " + edges[generique]["name"] + " " + typeRelation + " " + terme2)
	print("\n")










def inference_transitive(terme1, relationsTerme1, typeRelation, terme2, relationsTerme2, edges, nombreInferences=5):
	""" trouver un objet z tel que terme1Rz  et zRterme2

	chat r_lieu maison?
	 -> oui car chat r_lieu canapé      et     canapé r_lieu maison
	
	intuition de l'implémentation:
	sur cet exemple
	on récupère tous les objets x tels que chat r_lieu   x 				 (qu'on aura récup avec le "fichier" chat)
	et on regarde si on a  					x   r_lieu maison 			   (qu'on aura récup avec le "fichier" maison)



	marche que pour les relations transitives, donc r_lieu et r_has_part (ptre d'autres?)
	"""

	lesMeilleursTrucsTransitifs = []
	for trucTransitif, poids in relationsTerme1[typeRelation]["sortant"].items():
		if poids["weight_normed"]>0.5:
			lesMeilleursTrucsTransitifs.append(trucTransitif)

		if len(lesMeilleursTrucsTransitifs) >= nombreInferences:
			break


	#si la relation a un inverse, on le prend (on préfère celui là que les entrants )
	global coercifs
	coercifDeLaRelation = coercifs.get(typeRelation)
	
	if coercifDeLaRelation is None:
		lesEntrantsDeTerme2 = [entrants for entrants in relationsTerme2[typeRelation]["entrant"].keys()]
	else:
		lesEntrantsDeTerme2 = [sortant for sortant in relationsTerme2[coercifDeLaRelation]["sortant"].keys()]


	print("\ninférence transitive")
	for trucTransitif in lesMeilleursTrucsTransitifs:
		if trucTransitif in lesEntrantsDeTerme2:
			#générique est un identifiant, on récupère le nom associé
			print("\t" + "oui car " + terme1 +  " " + typeRelation + " " + edges[trucTransitif]["name"] + " et " + edges[trucTransitif]["name"] + " " + typeRelation + " " + terme2)
	print("\n")























	#pour l'instant on peut pas la faire à cause de "r_hypo" on demandera
def inference_inductive(terme1, relationsTerme1, typeRelation, terme2, relationsTerme2, edges, nombreInferences=5):
	""" trouver un spécifique pour lequel la réponse est vraie

	oiseau r_agent-1 voler?
	 -> oui car pigeon r_isa oiseau      et     pigeon r_agent-1 voler
	
	intuition de l'implémentation:
	sur cet exemple
	on récupère tous les objets x tels que x r_isa oiseau  (qu'on aura récup avec le "fichier" oiseau)
	et on regarde si on a  x r_agent-1 voler 			   (qu'on aura récup avec le "fichier" voler)



	(en vrai c'est exactement comme l'inférence déductive mais on regarde plus les génériques, que les spécifiques)
	"""



	lesMeilleuresGeneriques = []
	for generique, poids in relationsTerme1["r_hypo"]["entrant"].items():
		if poids["weight_normed"]>0.5:
			lesMeilleuresGeneriques.append(generique)

		if len(lesMeilleuresGeneriques) >= nombreInferences:
			break

	
	lesAgentsDeTerme2 = [agents for agents in relationsTerme2[typeRelation]["entrant"].keys()]

	print("\ninférence déductive : ")
	for generique in lesMeilleuresGeneriques:
		if generique in lesAgentsDeTerme2:

			#générique est un identifiant, on récupère le nom associé
			print("\t" + edges[generique]["name"] + " " + typeRelation + " " + terme2)
	print("\n")