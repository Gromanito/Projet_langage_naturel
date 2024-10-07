
def regle1(graphe):
    for noeudX in graphe.nodes:
        #pour chaque noeud, on regarde si la règle s'applique
        if noeudX['label'] == 'DET:':
            for noeudY in graphe.successors(noeudX):
                if noeudY['label'] == 'GN:':
                    for noeudZ in graphe.predecessors(noeudX):
                        for noeudW in graphe.successors(noeudY):
                            noeudA = graphe["compteur"]
                            graphe["compteur"] += 1
                            graphe.add_node(noeudA, {'label':'GNDET:', 'w':1})
                            graphe.add_edge(noeudA, noeudW, {'w':1, 'rel':'r_succ'})
                            graphe.add_edge(noeudW, noeudA, {'w':1, 'rel':'r_pred'})
                            graphe.add_edge(noeudZ, noeudA, {'w':1, 'rel':'r_succ'})
                            graphe.add_edge(noeudA, noeudZ, {'w':1, 'rel':'r_pred'})





        if (premisse1) and (premisse2) and ... :
            <action sur le graphe>