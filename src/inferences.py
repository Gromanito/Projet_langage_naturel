
def inference_deductive(identifiant1, relation, identifiant2, noeuds):
	""" trouver un générique pour lequel la réponse est vraie

	pigeon r_agent-1 voler?
	 -> oui car pigeon r_isa oiseau      et     oiseau r_agent-1 voler
	
	intuition de l'implémentation:
	sur cet exemple
	on récupère tous les objets x tels que pigeon r_isa x  (qu'on aura récup avec le "fichier" pigeon)
	et on regarde si on a  x r_agent-1 voler 			   (qu'on aura récup avec le "fichier" voler)
	"""
