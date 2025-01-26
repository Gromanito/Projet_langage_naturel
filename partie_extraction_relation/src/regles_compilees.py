def regle0(graphe, moteurRegle):
	nomRegle = 'regle0'
	for noeud_x in graphe.get_all_nodes_terme():
		if 'Det:' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'Nom:' in graphe.get_r_pos_of_node(noeud_y) :
					regleDejaAppliquee = moteurRegle.regle_deja_appliquee('regle0', (('x', noeud_x), ('y', noeud_y)))
					if not regleDejaAppliquee:
						noeud_n = graphe.creer_noeud_regle('terme', *[noeud_x, noeud_y] )
						graphe.add_r_pos_to_node('GN:', noeud_n)
						graphe.add_edge(noeud_n, noeud_y, label='r_chef', w=1)
						graphe.add_edge(noeud_n, noeud_x, label='r_sub_node:Det:', w=1)
						graphe.add_edge(noeud_n, noeud_y, label='r_sub_node:Nom:', w=1)



def regle1(graphe, moteurRegle):
	nomRegle = 'regle1'
	for noeud_x in graphe.get_all_nodes_terme():
		if 'GNDET:' in graphe.get_r_pos_of_node(noeud_x) :
			regleDejaAppliquee = moteurRegle.regle_deja_appliquee('regle1', (('x', noeud_x)))
			if not regleDejaAppliquee:
				graphe.add_r_pos_to_node('GN:', noeud_x)



def regle2(graphe, moteurRegle):
	nomRegle = 'regle2'
	for noeud_x in graphe.get_all_nodes_terme():
		if 'Pre:' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'GN:' in graphe.get_r_pos_of_node(noeud_y) :
					regleDejaAppliquee = moteurRegle.regle_deja_appliquee('regle2', (('x', noeud_x), ('y', noeud_y)))
					if not regleDejaAppliquee:
						noeud_n = graphe.creer_noeud_regle('terme', *[noeud_x, noeud_y] )
						graphe.add_r_pos_to_node('GNPre:', noeud_n)
						graphe.add_edge(noeud_n, noeud_y, label='r_chef', w=1)
						graphe.add_edge(noeud_n, noeud_x, label='r_sub_node:Pre:', w=1)
						graphe.add_edge(noeud_n, noeud_y, label='r_sub_node:GN:', w=1)



def regle3(graphe, moteurRegle):
	nomRegle = 'regle3'
	for noeud_x in graphe.get_all_nodes_terme():
		if 'Pre:' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'Nom:' in graphe.get_r_pos_of_node(noeud_y) :
					regleDejaAppliquee = moteurRegle.regle_deja_appliquee('regle3', (('x', noeud_x), ('y', noeud_y)))
					if not regleDejaAppliquee:
						noeud_n = graphe.creer_noeud_regle('terme', *[noeud_x, noeud_y] )
						graphe.add_r_pos_to_node('GNPre:', noeud_n)
						graphe.add_edge(noeud_n, noeud_y, label='r_chef', w=1)
						graphe.add_edge(noeud_n, noeud_x, label='r_sub_node:Pre:', w=1)
						graphe.add_edge(noeud_n, noeud_y, label='r_sub_node:Nom:', w=1)



def regle4(graphe, moteurRegle):
	nomRegle = 'regle4'
	for noeud_x in graphe.get_all_nodes_terme():
		if 'Nom:' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'GNPre:' in graphe.get_r_pos_of_node(noeud_y) :
					regleDejaAppliquee = moteurRegle.regle_deja_appliquee('regle4', (('x', noeud_x), ('y', noeud_y)))
					if not regleDejaAppliquee:
						noeud_n = graphe.creer_noeud_regle('terme', *[noeud_x, noeud_y] )
						graphe.add_r_pos_to_node('Nom:', noeud_n)
						graphe.add_edge(noeud_n, noeud_x, label='r_chef', w=1)
						graphe.add_edge(noeud_n, noeud_x, label='r_sub_node:Nom:', w=1)
						graphe.add_edge(noeud_n, noeud_y, label='r_sub_node:CDN:', w=1)



def regle5(graphe, moteurRegle):
	nomRegle = 'regle5'
	for noeud_x in graphe.get_all_nodes_terme():
		if 'GN:' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'GV:' in graphe.get_r_pos_of_node(noeud_y) :
					for noeud_z in graphe.get_successors_with_labelled_edge(noeud_y, 'r_succ'):
						if '.' == graphe.nodes[noeud_z]['name']:
							regleDejaAppliquee = moteurRegle.regle_deja_appliquee('regle5', (('x', noeud_x), ('y', noeud_y), ('z', noeud_z)))
							if not regleDejaAppliquee:
								noeud_n = graphe.creer_noeud_regle('terme', *[noeud_x, noeud_y] )
								graphe.add_r_pos_to_node('S:', noeud_n)
								graphe.add_edge(noeud_n, noeud_x, label='r_chef', w=1)
								graphe.add_edge(noeud_n, noeud_x, label='r_sub_node:GN:', w=1)
								graphe.add_edge(noeud_n, noeud_y, label='r_sub_node:GV:', w=1)



def regle6(graphe, moteurRegle):
	nomRegle = 'regle6'
	for noeud_x in graphe.get_all_nodes_terme():
		if 'Pro:Pers' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'GV:' in graphe.get_r_pos_of_node(noeud_y) :
					regleDejaAppliquee = moteurRegle.regle_deja_appliquee('regle6', (('x', noeud_x), ('y', noeud_y)))
					if not regleDejaAppliquee:
						noeud_n = graphe.creer_noeud_regle('terme', *[noeud_x, noeud_y] )
						graphe.add_r_pos_to_node('S:', noeud_n)
						graphe.add_edge(noeud_n, noeud_x, label='r_chef', w=1)
						graphe.add_edge(noeud_n, noeud_x, label='r_sub_node:Pro:Pers', w=1)
						graphe.add_edge(noeud_n, noeud_y, label='r_sub_node:GV:', w=1)



def regle7(graphe, moteurRegle):
	nomRegle = 'regle7'
	for noeud_x in graphe.get_all_nodes_terme():
		if 'GV:' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'GN:' in graphe.get_r_pos_of_node(noeud_y) :
					regleDejaAppliquee = moteurRegle.regle_deja_appliquee('regle7', (('x', noeud_x), ('y', noeud_y)))
					if not regleDejaAppliquee:
						noeud_n = graphe.creer_noeud_regle('terme', *[noeud_x,noeud_y] )
						graphe.add_r_pos_to_node('GV:', noeud_n)
						graphe.add_edge(noeud_n, noeud_x, label='r_chef', w=1)
						graphe.add_edge(noeud_n, noeud_x, label='r_sub_node:GV:', w=1)
						graphe.add_edge(noeud_n, noeud_y, label='r_sub_node:COD:', w=1)



def regle8(graphe, moteurRegle):
	nomRegle = 'regle8'
	for noeud_x in graphe.get_all_nodes_terme():
		if 'GV:' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'de' == graphe.nodes[noeud_y]['name']:
					for noeud_z in graphe.get_successors_with_labelled_edge(noeud_y, 'r_succ'):
						if 'GN:' in graphe.get_r_pos_of_node(noeud_z) :
							regleDejaAppliquee = moteurRegle.regle_deja_appliquee('regle8', (('x', noeud_x), ('y', noeud_y), ('z', noeud_z)))
							if not regleDejaAppliquee:
								noeud_n = graphe.creer_noeud_regle('terme', *[noeud_x, noeud_y, noeud_z] )
								graphe.add_r_pos_to_node('GV:', noeud_n)
								graphe.add_edge(noeud_n, noeud_x, label='r_chef', w=1)
								graphe.add_edge(noeud_n, noeud_x, label='r_sub_node:GV:', w=1)
								graphe.add_edge(noeud_n, noeud_z, label='r_sub_node:COI:', w=1)



def regle9(graphe, moteurRegle):
	nomRegle = 'regle9'
	for noeud_x in graphe.get_all_nodes_terme():
		if 'GV:' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'à' == graphe.nodes[noeud_y]['name']:
					for noeud_z in graphe.get_successors_with_labelled_edge(noeud_y, 'r_succ'):
						if 'GN:' in graphe.get_r_pos_of_node(noeud_z) :
							regleDejaAppliquee = moteurRegle.regle_deja_appliquee('regle9', (('x', noeud_x), ('y', noeud_y), ('z', noeud_z)))
							if not regleDejaAppliquee:
								noeud_n = graphe.creer_noeud_regle('terme', *[noeud_x, noeud_y, noeud_z] )
								graphe.add_r_pos_to_node('GV:', noeud_n)
								graphe.add_edge(noeud_n, noeud_x, label='r_chef', w=1)
								graphe.add_edge(noeud_n, noeud_x, label='r_sub_node:GV:', w=1)
								graphe.add_edge(noeud_n, noeud_z, label='r_sub_node:COI:', w=1)



def regle10(graphe, moteurRegle):
	nomRegle = 'regle10'
	for noeud_x in graphe.get_all_nodes_terme():
		if 'Adj:' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_predecessors_with_labelled_edge(noeud_x, 'r_succ'):
				for noeud_z in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
					regleDejaAppliquee = moteurRegle.regle_deja_appliquee('regle10', (('x', noeud_x), ('y', noeud_y), ('z', noeud_z)))
					if not regleDejaAppliquee:
						graphe.add_edge(noeud_y, noeud_z, label='r_succ', w=1)
						graphe.add_edge(noeud_z, noeud_y, label='r_pred', w=1)



def regle11(graphe, moteurRegle):
	nomRegle = 'regle11'
	for noeud_x in graphe.get_all_nodes_terme():
		if 'Adj:' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'Nom:' in graphe.get_r_pos_of_node(noeud_y) :
					regleDejaAppliquee = moteurRegle.regle_deja_appliquee('regle11', (('x', noeud_x), ('y', noeud_y)))
					if not regleDejaAppliquee:
						noeud_n = graphe.creer_noeud_regle('terme', *[noeud_x,noeud_y] )
						graphe.add_r_pos_to_node('Nom:', noeud_n)
						graphe.add_edge(noeud_n, noeud_y, label='r_chef', w=1)
						graphe.add_edge(noeud_n, noeud_x, label='r_sub_node:Adj:', w=1)
						graphe.add_edge(noeud_n, noeud_y, label='r_sub_node:Nom:', w=1)



def regle12(graphe, moteurRegle):
	nomRegle = 'regle12'
	for noeud_x in graphe.get_all_nodes_terme():
		if 'Nom:' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'Adj:' in graphe.get_r_pos_of_node(noeud_y) :
					regleDejaAppliquee = moteurRegle.regle_deja_appliquee('regle12', (('x', noeud_x), ('y', noeud_y)))
					if not regleDejaAppliquee:
						noeud_n = graphe.creer_noeud_regle('terme', *[noeud_x,noeud_y] )
						graphe.add_r_pos_to_node('Nom:', noeud_n)
						graphe.add_edge(noeud_n, noeud_x, label='r_chef', w=1)
						graphe.add_edge(noeud_n, noeud_y, label='r_sub_node:Adj:', w=1)
						graphe.add_edge(noeud_n, noeud_x, label='r_sub_node:Nom:', w=1)



def regle13(graphe, moteurRegle):
	nomRegle = 'regle13'
	for noeud_x in graphe.get_all_nodes_terme():
		if 'Adv:' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_predecessors_with_labelled_edge(noeud_x, 'r_succ'):
				for noeud_z in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
					regleDejaAppliquee = moteurRegle.regle_deja_appliquee('regle13', (('x', noeud_x), ('y', noeud_y), ('z', noeud_z)))
					if not regleDejaAppliquee:
						graphe.add_edge(noeud_y, noeud_z, label='r_succ', w=1)
						graphe.add_edge(noeud_z, noeud_y, label='r_pred', w=1)



def regle14(graphe, moteurRegle):
	nomRegle = 'regle14'
	for noeud_x in graphe.get_all_nodes_terme():
		if 'Punc:' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				for noeud_b in graphe.get_predecessors_with_labelled_edge(noeud_x, 'r_succ'):
					for noeud_a in graphe.get_successors_with_labelled_edge(noeud_y, 'r_succ'):
						regleDejaAppliquee = moteurRegle.regle_deja_appliquee('regle14', (('x', noeud_x), ('y', noeud_y), ('b', noeud_b), ('a', noeud_a)))
						if not regleDejaAppliquee:
							graphe.add_edge(noeud_b, noeud_a, label='r_succ', w=1)
							graphe.add_edge(noeud_a, noeud_b, label='r_pred', w=1)



def regle15(graphe, moteurRegle):
	nomRegle = 'regle15'
	for noeud_x in graphe.get_all_nodes_terme():
		if 'GN:' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'Pro:' in graphe.get_r_pos_of_node(noeud_y) :
					for noeud_z in graphe.get_successors_with_labelled_edge(noeud_y, 'r_succ'):
						if 'GV:' in graphe.get_r_pos_of_node(noeud_z) :
							regleDejaAppliquee = moteurRegle.regle_deja_appliquee('regle15', (('x', noeud_x), ('y', noeud_y), ('z', noeud_z)))
							if not regleDejaAppliquee:
								noeud_n = graphe.creer_noeud_regle('terme', *[noeud_x, noeud_y, noeud_z] )
								graphe.add_r_pos_to_node('S:', noeud_n)
								graphe.add_edge(noeud_n, noeud_x, label='r_chef', w=1)
								graphe.add_edge(noeud_n, noeud_x, label='r_sub_node:GN:', w=1)
								graphe.add_edge(noeud_n, noeud_y, label='r_sub_node:Pro:', w=1)
								graphe.add_edge(noeud_n, noeud_z, label='r_sub_node:GV:', w=1)



def regle16(graphe, moteurRegle):
	nomRegle = 'regle16'
	for noeud_x in graphe.get_all_nodes_terme():
		if 'ne' == graphe.nodes[noeud_x]['name']:
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'Ver:Inf' in graphe.get_r_pos_of_node(noeud_y) :
					for noeud_z in graphe.get_successors_with_labelled_edge(noeud_y, 'r_succ'):
						if 'pas' == graphe.nodes[noeud_z]['name']:
							regleDejaAppliquee = moteurRegle.regle_deja_appliquee('regle16', (('x', noeud_x), ('y', noeud_y), ('z', noeud_z)))
							if not regleDejaAppliquee:
								noeud_n = graphe.creer_noeud_regle('terme', *[noeud_x, noeud_y, noeud_z] )
								graphe.add_r_pos_to_node('Ver:Inf', noeud_n)
								graphe.add_edge(noeud_n, noeud_x, label='r_sub_node:Ver:Inf', w=1)
								graphe.add_edge(noeud_n, noeud_y, label='r_chef', w=1)



def regle17(graphe, moteurRegle):
	nomRegle = 'regle17'
	for noeud_x in graphe.get_all_nodes_terme():
		if 'Ver:Inf' in graphe.get_r_pos_of_node(noeud_x) :
			regleDejaAppliquee = moteurRegle.regle_deja_appliquee('regle17', (('x', noeud_x)))
			if not regleDejaAppliquee:
				graphe.add_r_pos_to_node('GV:', noeud_x)



def regle18(graphe, moteurRegle):
	nomRegle = 'regle18'
	for noeud_x in graphe.get_all_nodes_terme():
		if 'Ver:Passive:' in graphe.get_r_pos_of_node(noeud_x) :
			regleDejaAppliquee = moteurRegle.regle_deja_appliquee('regle18', (('x', noeud_x)))
			if not regleDejaAppliquee:
				graphe.add_r_pos_to_node('GV:Passive:', noeud_x)



def regle19(graphe, moteurRegle):
	nomRegle = 'regle19'
	for noeud_x in graphe.get_all_nodes_terme():
		if 'être' == graphe.nodes[noeud_x]['name']:
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'Ver:PPas' in graphe.get_r_pos_of_node(noeud_y) :
					regleDejaAppliquee = moteurRegle.regle_deja_appliquee('regle19', (('x', noeud_x), ('y', noeud_y)))
					if not regleDejaAppliquee:
						noeud_n = graphe.creer_noeud_regle('terme', *[noeud_x, noeud_y] )
						graphe.add_r_pos_to_node('Ver:Passive:', noeud_n)
						graphe.add_r_pos_to_node('Ver:', noeud_n)
						graphe.add_edge(noeud_n, noeud_x, label='r_sub_node:Ver:', w=1)
						graphe.add_edge(noeud_n, noeud_y, label='r_sub_node:Ver:', w=1)
						graphe.add_edge(noeud_n, noeud_y, label='r_chef', w=1)



def regle20(graphe, moteurRegle):
	nomRegle = 'regle20'
	for noeud_x in graphe.get_all_nodes_terme():
		if 'avoir' == graphe.nodes[noeud_x]['name']:
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'Ver:PPas' in graphe.get_r_pos_of_node(noeud_y) :
					regleDejaAppliquee = moteurRegle.regle_deja_appliquee('regle20', (('x', noeud_x), ('y', noeud_y)))
					if not regleDejaAppliquee:
						noeud_n = graphe.creer_noeud_regle('terme', *[noeud_x, noeud_y] )
						graphe.add_r_pos_to_node('Ver:', noeud_n)
						graphe.add_edge(noeud_n, noeud_x, label='r_sub_node:Ver:', w=1)
						graphe.add_edge(noeud_n, noeud_y, label='r_sub_node:Ver:', w=1)
						graphe.add_edge(noeud_n, noeud_y, label='r_chef', w=1)



def regle21(graphe, moteurRegle):
	nomRegle = 'regle21'
	for noeud_x in graphe.get_all_nodes_terme():
		if 'avoir' == graphe.nodes[noeud_x]['name']:
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'été' == graphe.nodes[noeud_y]['name']:
					for noeud_z in graphe.get_successors_with_labelled_edge(noeud_y, 'r_succ'):
						if 'Ver:PPas' in graphe.get_r_pos_of_node(noeud_z) :
							regleDejaAppliquee = moteurRegle.regle_deja_appliquee('regle21', (('x', noeud_x), ('y', noeud_y), ('z', noeud_z)))
							if not regleDejaAppliquee:
								noeud_n = graphe.creer_noeud_regle('terme', *[noeud_x, noeud_y, noeud_z] )
								graphe.add_r_pos_to_node('Ver:', noeud_n)
								graphe.add_r_pos_to_node('Ver:Passive:', noeud_n)
								graphe.add_edge(noeud_n, noeud_x, label='r_sub_node:Ver:', w=1)
								graphe.add_edge(noeud_n, noeud_y, label='r_sub_node:Ver:', w=1)
								graphe.add_edge(noeud_n, noeud_z, label='r_sub_node:Ver:', w=1)
								graphe.add_edge(noeud_n, noeud_z, label='r_chef', w=1)



def regle22(graphe, moteurRegle):
	nomRegle = 'regle22'
	for noeud_x in graphe.get_all_nodes_terme():
		if 'GV:Passive:' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'par' == graphe.nodes[noeud_y]['name']:
					for noeud_z in graphe.get_successors_with_labelled_edge(noeud_y, 'r_succ'):
						if 'GN:' in graphe.get_r_pos_of_node(noeud_z) :
							regleDejaAppliquee = moteurRegle.regle_deja_appliquee('regle22', (('x', noeud_x), ('y', noeud_y), ('z', noeud_z)))
							if not regleDejaAppliquee:
								noeud_n = graphe.creer_noeud_regle('terme', *[noeud_x, noeud_y, noeud_z] )
								graphe.add_r_pos_to_node('GV:Passive:', noeud_n)
								graphe.add_edge(noeud_n, noeud_x, label='r_chef', w=1)
								graphe.add_edge(noeud_n, noeud_x, label='r_sub_node:GV:Passive:', w=1)
								graphe.add_edge(noeud_n, noeud_y, label='r_sub_node:Pre:', w=1)
								graphe.add_edge(noeud_n, noeud_z, label='r_sub_node:GN:', w=1)



def regle23(graphe, moteurRegle):
	nomRegle = 'regle23'
	for noeud_x in graphe.get_all_nodes_terme():
		if 'GN:' in graphe.get_r_pos_of_node(noeud_x) :
			for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_succ'):
				if 'GV:Passive:' in graphe.get_r_pos_of_node(noeud_y) :
					regleDejaAppliquee = moteurRegle.regle_deja_appliquee('regle23', (('x', noeud_x), ('y', noeud_y)))
					if not regleDejaAppliquee:
						noeud_n = graphe.creer_noeud_regle('terme', *[noeud_x, noeud_y] )
						graphe.add_r_pos_to_node('S:', noeud_n)
						graphe.add_edge(noeud_n, noeud_x, label='r_sub_node:GN:', w=1)
						graphe.add_edge(noeud_n, noeud_y, label='r_sub_node:GV:Passive:', w=1)
						graphe.add_edge(noeud_n, noeud_x, label='r_chef', w=1)



def regle24(graphe, moteurRegle):
	nomRegle = 'regle24'
	for noeud_x in graphe.get_all_nodes_terme():
		for noeud_y in graphe.get_successors_with_labelled_edge(noeud_x, 'r_chef'):
			for noeud_z in graphe.get_successors_with_labelled_edge(noeud_y, 'r_chef'):
				regleDejaAppliquee = moteurRegle.regle_deja_appliquee('regle24', (('x', noeud_x), ('y', noeud_y), ('z', noeud_z)))
				if not regleDejaAppliquee:
					graphe.add_edge(noeud_x, noeud_z, label='r_chef', w=1)



