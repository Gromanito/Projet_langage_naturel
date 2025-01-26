def regle0(graphe, moteurRegle):
	noeuds_concernes = [n for n in graphe if graphe.nodes[n]['type_node']=='terme' or graphe.nodes[n]['type_node']=='r_lemma' ]
	nomRegle = 'regle0'
	for noeud_x in graphe.nodes:
		if 'Det:' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'Nom:' in graphe.get_r_pos_of_node(noeud_y) :
					regleDejaAppliquee = moteurRegle.regle_deja_appliquee(regle0, (('x', noeud_x), ('y', noeud_y)))
					if not regleDejaAppliquee:
						noeud_n, _ = graphe.ajoute_noeud_par_dessus('terme', *[noeud_x,noeud_y] )
						graphe.add_r_pos_to_node('GN:', noeud_n)
						graphe.add_edge(noeud_n, noeud_y, label='r_tete', w=1)
						graphe.add_edge(noeud_n, noeud_x, label='r_corps', w=1)



def regle1(graphe, moteurRegle):
	noeuds_concernes = [n for n in graphe if graphe.nodes[n]['type_node']=='terme' or graphe.nodes[n]['type_node']=='r_lemma' ]
	nomRegle = 'regle1'
	for noeud_x in graphe.nodes:
		if 'GNDET:' in graphe.get_r_pos_of_node(noeud_x) :
			regleDejaAppliquee = moteurRegle.regle_deja_appliquee(regle1, (('x', noeud_x)))
			if not regleDejaAppliquee:
				graphe.add_r_pos_to_node('GN:', noeud_n)



def regle2(graphe, moteurRegle):
	noeuds_concernes = [n for n in graphe if graphe.nodes[n]['type_node']=='terme' or graphe.nodes[n]['type_node']=='r_lemma' ]
	nomRegle = 'regle2'
	for noeud_x in graphe.nodes:
		if 'Prep:' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'GN:' in graphe.get_r_pos_of_node(noeud_y) :
					regleDejaAppliquee = moteurRegle.regle_deja_appliquee(regle2, (('x', noeud_x), ('y', noeud_y)))
					if not regleDejaAppliquee:
						noeud_n, _ = graphe.ajoute_noeud_par_dessus('terme', *[noeud_x, noeud_y] )
						graphe.add_r_pos_to_node('GNPrep:', noeud_n)
						graphe.add_edge(noeud_n, noeud_y, label='r_tete', w=1)



def regle3(graphe, moteurRegle):
	noeuds_concernes = [n for n in graphe if graphe.nodes[n]['type_node']=='terme' or graphe.nodes[n]['type_node']=='r_lemma' ]
	nomRegle = 'regle3'
	for noeud_x in graphe.nodes:
		if 'Nom:' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'GNPrep:' in graphe.get_r_pos_of_node(noeud_y) :
					regleDejaAppliquee = moteurRegle.regle_deja_appliquee(regle3, (('x', noeud_x), ('y', noeud_y)))
					if not regleDejaAppliquee:
						noeud_n, _ = graphe.ajoute_noeud_par_dessus('terme', *[noeud_x, noeud_y] )
						graphe.add_r_pos_to_node('Nom:', noeud_n)
						graphe.add_edge(noeud_n, noeud_x, label='r_tete', w=1)
						graphe.add_edge(noeud_n, noeud_y, label='r_corps', w=1)



def regle4(graphe, moteurRegle):
	noeuds_concernes = [n for n in graphe if graphe.nodes[n]['type_node']=='terme' or graphe.nodes[n]['type_node']=='r_lemma' ]
	nomRegle = 'regle4'
	for noeud_x in graphe.nodes:
		if 'GN:' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'GV:' in graphe.get_r_pos_of_node(noeud_y) :
					regleDejaAppliquee = moteurRegle.regle_deja_appliquee(regle4, (('x', noeud_x), ('y', noeud_y)))
					if not regleDejaAppliquee:
						noeud_n, _ = graphe.ajoute_noeud_par_dessus('terme', *[noeud_x, noeud_y] )
						graphe.add_r_pos_to_node('S:', noeud_n)
						graphe.add_edge(noeud_x, noeud_y, label='r_agent-1', w=1)
						graphe.add_edge(noeud_y, noeud_x, label='r_agent', w=1)



def regle5(graphe, moteurRegle):
	noeuds_concernes = [n for n in graphe if graphe.nodes[n]['type_node']=='terme' or graphe.nodes[n]['type_node']=='r_lemma' ]
	nomRegle = 'regle5'
	for noeud_x in graphe.nodes:
		if 'GV:' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'GN:' in graphe.get_r_pos_of_node(noeud_y) :
					regleDejaAppliquee = moteurRegle.regle_deja_appliquee(regle5, (('x', noeud_x), ('y', noeud_y)))
					if not regleDejaAppliquee:
						noeud_n, _ = graphe.ajoute_noeud_par_dessus('terme', *[noeud_x,noeud_y] )
						graphe.add_r_pos_to_node('GV:', noeud_n)



def regle6(graphe, moteurRegle):
	noeuds_concernes = [n for n in graphe if graphe.nodes[n]['type_node']=='terme' or graphe.nodes[n]['type_node']=='r_lemma' ]
	nomRegle = 'regle6'
	for noeud_x in graphe.nodes:
		if 'Adj:' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_predecessors_with_labelled_edge(noeud_x, 'r_succ'):
				for noeud_z in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
					regleDejaAppliquee = moteurRegle.regle_deja_appliquee(regle6, (('x', noeud_x), ('y', noeud_y), ('z', noeud_z)))
					if not regleDejaAppliquee:
						graphe.add_edge(noeud_y, noeud_z, label='r_succ', w=1)
						graphe.add_edge(noeud_y, noeud_ , label='r_pred', w=1)



def regle7(graphe, moteurRegle):
	noeuds_concernes = [n for n in graphe if graphe.nodes[n]['type_node']=='terme' or graphe.nodes[n]['type_node']=='r_lemma' ]
	nomRegle = 'regle7'
	for noeud_x in graphe.nodes:
		if 'Adj:' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'Nom:' in graphe.get_r_pos_of_node(noeud_y) :
					regleDejaAppliquee = moteurRegle.regle_deja_appliquee(regle7, (('x', noeud_x), ('y', noeud_y)))
					if not regleDejaAppliquee:
						noeud_n, _ = graphe.ajoute_noeud_par_dessus('terme', *[noeud_x,noeud_y] )
						graphe.add_r_pos_to_node('Nom:', noeud_n)
						graphe.add_edge(noeud_n, noeud_ , label='r_tete', w=1)



def regle8(graphe, moteurRegle):
	noeuds_concernes = [n for n in graphe if graphe.nodes[n]['type_node']=='terme' or graphe.nodes[n]['type_node']=='r_lemma' ]
	nomRegle = 'regle8'
	for noeud_x in graphe.nodes:
		if 'Nom:' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'Adj:' in graphe.get_r_pos_of_node(noeud_y) :
					regleDejaAppliquee = moteurRegle.regle_deja_appliquee(regle8, (('x', noeud_x), ('y', noeud_y)))
					if not regleDejaAppliquee:
						noeud_n, _ = graphe.ajoute_noeud_par_dessus('terme', *[noeud_x,noeud_y] )
						graphe.add_r_pos_to_node('Nom:', noeud_n)
						graphe.add_edge(noeud_n, noeud_ , label='r_tete', w=1)



def regle9(graphe, moteurRegle):
	noeuds_concernes = [n for n in graphe if graphe.nodes[n]['type_node']=='terme' or graphe.nodes[n]['type_node']=='r_lemma' ]
	nomRegle = 'regle9'
	for noeud_x in graphe.nodes:
		if 'Adv:' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_predecessors_with_labelled_edge(noeud_x, 'r_succ'):
				for noeud_z in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
					regleDejaAppliquee = moteurRegle.regle_deja_appliquee(regle9, (('x', noeud_x), ('y', noeud_y), ('z', noeud_z)))
					if not regleDejaAppliquee:
						graphe.add_edge(noeud_y, noeud_z, label='r_succ', w=1)
						graphe.add_edge(noeud_y, noeud_ , label='r_pred', w=1)



def regle10(graphe, moteurRegle):
	noeuds_concernes = [n for n in graphe if graphe.nodes[n]['type_node']=='terme' or graphe.nodes[n]['type_node']=='r_lemma' ]
	nomRegle = 'regle10'
	for noeud_x in graphe.nodes:
		if 'GN:' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'Pro:' in graphe.get_r_pos_of_node(noeud_y) :
					for noeud_z in graphe.get_successors_with_labelled_edge(noeud_y, 'r_succ'):
						if 'GV:' in graphe.get_r_pos_of_node(noeud_z) :
							regleDejaAppliquee = moteurRegle.regle_deja_appliquee(regle10, (('x', noeud_x), ('y', noeud_y), ('z', noeud_z)))
							if not regleDejaAppliquee:
								noeud_n, _ = graphe.ajoute_noeud_par_dessus('terme', *[noeud_x, noeud_y, noeud_z] )
								graphe.add_r_pos_to_node('S:', noeud_n)
								graphe.add_edge(noeud_x, noeud_z, label='r_agent-1', w=1)
								graphe.add_edge(noeud_z, noeud_x, label='r_agent', w=1)



def regle11(graphe, moteurRegle):
	noeuds_concernes = [n for n in graphe if graphe.nodes[n]['type_node']=='terme' or graphe.nodes[n]['type_node']=='r_lemma' ]
	nomRegle = 'regle11'
	for noeud_x in graphe.nodes:
		if être == graphe.nodes[noeud_x]['name']:
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'Ver:PPas' in graphe.get_r_pos_of_node(noeud_y) :
					regleDejaAppliquee = moteurRegle.regle_deja_appliquee(regle11, (('x', noeud_x), ('y', noeud_y)))
					if not regleDejaAppliquee:
						noeud_n, _ = graphe.ajoute_noeud_par_dessus('terme', *[noeud_x, noeud_y] )
						graphe.add_r_pos_to_node('Ver:', noeud_n)
						graphe.add_edge(noeud_n, noeud_y, label='r_tete', w=1)



def regle12(graphe, moteurRegle):
	noeuds_concernes = [n for n in graphe if graphe.nodes[n]['type_node']=='terme' or graphe.nodes[n]['type_node']=='r_lemma' ]
	nomRegle = 'regle12'
	for noeud_x in graphe.nodes:
		if avoir == graphe.nodes[noeud_x]['name']:
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'Ver:PPas' in graphe.get_r_pos_of_node(noeud_y) :
					regleDejaAppliquee = moteurRegle.regle_deja_appliquee(regle12, (('x', noeud_x), ('y', noeud_y)))
					if not regleDejaAppliquee:
						noeud_n, _ = graphe.ajoute_noeud_par_dessus('terme', *[noeud_x, noeud_y] )
						graphe.add_r_pos_to_node('Ver:', noeud_n)
						graphe.add_edge(noeud_n, noeud_y, label='r_tete', w=1)



def regle13(graphe, moteurRegle):
	noeuds_concernes = [n for n in graphe if graphe.nodes[n]['type_node']=='terme' or graphe.nodes[n]['type_node']=='r_lemma' ]
	nomRegle = 'regle13'
	for noeud_x in graphe.nodes:
		if avoir == graphe.nodes[noeud_x]['name']:
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if être == graphe.nodes[noeud_y]['name']:
					for noeud_z in graphe.get_successors_with_labelled_edge(noeud_y, 'r_succ'):
						if 'Ver:PPas' in graphe.get_r_pos_of_node(noeud_z) :
							regleDejaAppliquee = moteurRegle.regle_deja_appliquee(regle13, (('x', noeud_x), ('y', noeud_y), ('z', noeud_z)))
							if not regleDejaAppliquee:
								noeud_n, _ = graphe.ajoute_noeud_par_dessus('terme', *[noeud_x, noeud_y, noeud_z] )
								graphe.add_r_pos_to_node('Ver:', noeud_n)
								graphe.add_edge(noeud_n, noeud_z, label='r_tete', w=1)



def regle14(graphe, moteurRegle):
	noeuds_concernes = [n for n in graphe if graphe.nodes[n]['type_node']=='terme' or graphe.nodes[n]['type_node']=='r_lemma' ]
	nomRegle = 'regle14'
	for noeud_x in graphe.nodes:
		for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_tete'):
			for noeud_z in graphe.get_successors_with_labelled_edge(noeud_y, 'r_tete'):
				regleDejaAppliquee = moteurRegle.regle_deja_appliquee(regle14, (('x', noeud_x), ('y', noeud_y), ('z', noeud_z)))
				if not regleDejaAppliquee:
					graphe.add_edge(noeud_x, noeud_z, label='r_tete', w=1)



