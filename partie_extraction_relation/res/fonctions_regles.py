def regle0(graphe, moteurRegle):
	nomRegle = 'regle0'
	for noeud_x in graphe.nodes:
		if 'Det:' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'GN:' in graphe.get_r_pos_of_node(noeud_y) :
					regleDejaAppliquee = moteurRegle.regle_deja_appliquee(regle0, (('x', noeud_x), ('y', noeud_y)))
					if not regleDejaAppliquee:
						noeud_n, _ = graphe.ajoute_noeud_par_dessus('terme', *[noeud_x,noeud_y] )
						graphe.add_r_pos_to_node('GNDET:', noeud_n)



def regle1(graphe, moteurRegle):
	nomRegle = 'regle1'
	for noeud_x in graphe.nodes:
		if 'GN:' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'Prep:' in graphe.get_r_pos_of_node(noeud_y) :
					for noeud_z in graphe.get_successors_with_labelled_edge(noeud_y, 'r_succ'):
						if 'GN:' in graphe.get_r_pos_of_node(noeud_z) :
							regleDejaAppliquee = moteurRegle.regle_deja_appliquee(regle1, (('x', noeud_x), ('y', noeud_y), ('z', noeud_z)))
							if not regleDejaAppliquee:
								noeud_n, _ = graphe.ajoute_noeud_par_dessus('terme', *[noeud_x, noeud_y, noeud_z] )
								graphe.add_r_pos_to_node('GN:', noeud_n)



def regle2(graphe, moteurRegle):
	nomRegle = 'regle2'
	for noeud_x in graphe.nodes:
		if 'GN:' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'GV:' in graphe.get_r_pos_of_node(noeud_y) :
					regleDejaAppliquee = moteurRegle.regle_deja_appliquee(regle2, (('x', noeud_x), ('y', noeud_y)))
					if not regleDejaAppliquee:
						graphe.add_edge(noeud_x, noeud_y, label='r_agent-1', w=1)
						graphe.add_edge(noeud_y, noeud_x, label='r_agent', w=1)



