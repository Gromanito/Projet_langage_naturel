import json
def inference_deductive(terme1, relationsTerme1, terme2, relationsTerme2, edges, nombreInferences=5):
	""" trouver un générique pour lequel la réponse est vraie

	pigeon r_agent-1 voler?
	 -> oui car pigeon r_isa oiseau      et     oiseau r_agent-1 voler
	
	intuition de l'implémentation:
	sur cet exemple
	on récupère tous les objets x tels que pigeon r_isa x  (qu'on aura récup avec le "fichier" pigeon)
	et on regarde si on a  x r_agent-1 voler 			   (qu'on aura récup avec le "fichier" voler)
	"""

	lesMeilleuresGeneriques = []
	for generique, poids in relationsTerme1["r_isa"]["superClasse"].items():
		if poids["weight_normed"]>0.5:
			lesMeilleuresGeneriques.append(generique)

	#ça peut ne pas être r_agent-1, faudra faire les autres etc blabla
	lesAgentsDeTerme2 = [agents for agents in relationsTerme2["r_agent"]["agents"].keys()]


	for generique in lesMeilleuresGeneriques:
		if generique in lesAgentsDeTerme2:
			print(generique + " r_agent-1 griffer")
	


with open ("res/fichiersExploitables/matou/r_isa.json") as fichier:
	r_isaMatou = json.load(fichier)

with open ("res/fichiersExploitables/griffer/r_agent.json") as fichier:
	r_agentGriffer = json.load(fichier)

dicoMatou = {"r_isa" : r_isaMatou}
dicoGriffer = {"r_agent" : r_agentGriffer}


inference_deductive("matou", dicoMatou, "griffer", dicoGriffer, None)