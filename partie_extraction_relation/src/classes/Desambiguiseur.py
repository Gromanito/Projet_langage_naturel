from classes.inferences.Inferateur import *


class NoeudPhrase:
    """ Ptite classe qui représente un noeud dans la structure de la phrase
    c'est donc quelque chose qui a été "généré" par les règles de grammaires
    ça peut être de 3 "grands types", un Nom: un GN: ou un GV:  et, "pas important"
    """

    graphe = None


    #attribut de classe, partagés par tous les noeuds, pour que tous les noeuds puissent se trouver entre eux
    map_id_vers_noeud_phrase = {}


    def __init__(self, id_noeud):

        self.id_noeud = id_noeud
        NoeudPhrase.map_id_vers_noeud_phrase[id_noeud] = self

        #on récupère le prosodic du noeud
        self.prosodic = NoeudPhrase.graphe.nodes[self.id_noeud]["name"]


        self.noeud_d_une_phrase = False
        


    #lorsqu'on crée le noeud dans le graphe, il n'est connecté à personne, on a donc aucune info sur le noeud
    #cette fonction sert à aller chercher les infos lorsque tout est prêt
    def update(self):

        #on récupère (tous les) r_pos du noeud
        self.r_pos = NoeudPhrase.graphe.get_r_pos_of_node(self.id_noeud)


        #on récupère tous les sous-noeuds du noeud
        #peut être vide si c'est un noeud "feuille"
        self.sous_noeuds = NoeudPhrase.graphe.get_sub_nodes_of_node(self.id_noeud)

        
        if self.sous_noeuds:
            
            self.isFeuille = False
            self.r_chef = NoeudPhrase.graphe.get_successors_with_labelled_edge(self.id_noeud, 'r_chef' )[0]

        else:
            self.isFeuille = True
            self.r_chef = self.prosodic



        
        

    
    

    def get_r_chef(self):
        
        if self.isFeuille:
            return self.prosodic
        else:
            return NoeudPhrase.map_id_vers_noeud_phrase[self.r_chef].get_r_chef()

    
    def ticket(self):
        """ bon flemme d'expliquer mais c'est pour moi, quand y a un choix à faire entre 2 noeuds qui
        génèrent le même prosodic, y a un conflit. Je vais donc demander aux 2 noeuds un "ticket" 
        le ticket génère les inférences qu'il faudrait faire pour "justifier" ce noeud
        
        intéret : faire seulement des inférences sur des choses qui diffèrent des noeuds"""



        if self.isFeuille:
            return []
        
        if len(self.sous_noeuds) == 1:
            type_decomposition = list(self.sous_noeuds.keys())[0]
            return self.get_sous_noeud(type_decomposition).ticket()

        
        #maintenant, on doit gérer TOUS les cas possibles, selon le type de noeud qu'on est, selon notre "décompostion"

        type_decomposition = set(self.sous_noeuds.keys())


        #Adj + Nom
        if type_decomposition == set(("Adj:", "Nom:" )):
            noeudAdj = self.get_sous_noeud("Adj:")
            noeudNom = self.get_sous_noeud("Nom:")
            return [(noeudNom.get_r_chef(), "r_carac", noeudAdj.get_r_chef())] + noeudNom.ticket()
    

        #Nom + CDN 

        elif type_decomposition == set(("Nom:", "CDN:" )):
            noeudNom = self.get_sous_noeud("Nom:")
            noeudCDN = self.get_sous_noeud("CDN:")

            #booooon, les compléments du nom chiantos 

            #             "à" :
            #     Relation de contenu : "une pizza à la mozzarella" (contient de la mozzarella).
            #     Relation de fonction/utilisation : "un couteau à beurre" (utilisé pour le beurre).
            #     Relation de destination : "une lettre à un ami" (adressée à un ami).

            #             "de" :
            #     Relation de possession : "le livre de Marie" (appartient à Marie).
            #     Relation de provenance/origine : "un vin de Bordeaux" (provenant de Bordeaux).
            #     Relation de composition : "un mur de briques" (fait de briques).

            # Comment je fais pour savoir quel relation JDM utilser quand j'ai 'à' ? sah j'en sais rien

            #on va dire qu'on utilise une inférence fixe pour chaque préposition (prck je sais pas du tout comment faire)


            # quand j'ai "à la" "au" ...  j'utilise r_has_part (à la mozzarella)
            if noeudCDN.prosodic.startswith("à le") or noeudCDN.prosodic.startswith("au"):
                return [(noeudNom.get_r_chef(), "r_has_part", noeudCDN.get_r_chef())] + noeudNom.ticket() + noeudCDN.ticket()

            #jsp ça marchait bien ...
            elif noeudCDN.prosodic.startswith("de"):
                return [(noeudNom.get_r_chef(), "r_lieu", noeudCDN.get_r_chef())] + noeudNom.ticket() + noeudCDN.ticket()

            #absolument aucune idée
            elif noeudCDN.prosodic.startswith("à"):
                return [(noeudNom.get_r_chef(), "r_associated", noeudCDN.get_r_chef())] + noeudNom.ticket() + noeudCDN.ticket()



        #groupe verbal à la forme passive
        elif type_decomposition == set(("GV:Passive:", "Prep:", "GN" )):
            noeudGV = self.get_sous_noeud("GV:")
            noeudGN = self.get_sous_noeud("GV:Passive:")
            return [(noeudGN.get_r_chef(), "r_agent-1", noeudGV.get_r_chef())] + noeudNom.ticket() + noeudGN.ticket()


        #GV + COD
        elif type_decomposition == set(("GV:", "COD:" )):
            noeudGV = self.get_sous_noeud("GV:")
            noeudCOD = self.get_sous_noeud("COD:")
            return [(noeudCOD.get_r_chef(), "r_patient-1", noeudGV.get_r_chef())] + noeudGV.ticket() + noeudCOD.ticket()


        #GV + COI (même chose qu'avec le COD)
        elif type_decomposition == set(("GV:", "COI:" )):
            noeudGV = self.get_sous_noeud("GV:")
            noeudCOI = self.get_sous_noeud("COI:")
            return [(noeudCOI.get_r_chef(), "r_patient-1", noeudGV.get_r_chef())] + noeudGV.ticket() + noeudCOI.ticket()
        
        
        #GN + GV (c'est une phrase)
        elif type_decomposition == set(("GN:", "GV:" )):
            noeudGN = self.get_sous_noeud("GN:")
            noeudGV = self.get_sous_noeud("GV:")
            return [(noeudGN.get_r_chef(), "r_agent-1", noeudGV.get_r_chef())] + noeudGN.ticket() + noeudGV.ticket()


        #GN + GV:Passive: (c'est une phrase à la forme passive)
        elif type_decomposition == set(("GN:", "GV:Passive:" )):
            noeudGN = self.get_sous_noeud("GN:")
            noeudGV = self.get_sous_noeud("GV:Passive:")
            return [(noeudGN.get_r_chef(), "r_patient-1", noeudGV.get_r_chef())] + noeudGN.ticket() + noeudGV.ticket()


        #GN + Pro: + GV (c'est une phrase (avec pronom))
        elif type_decomposition == set(("GN:","Pro:", "GV:" )):
            noeudGN = self.get_sous_noeud("GN:")
            noeudGV = self.get_sous_noeud("GV:")
            return [(noeudGN.get_r_chef(), "r_agent-1", noeudGV.get_r_chef())] + noeudGN.ticket() + noeudGV.ticket()


        
        else:
            tickets_sous_noeuds = []
            for sous_noeud in self.sous_noeuds.values():
                tickets_sous_noeuds = tickets_sous_noeuds + NoeudPhrase.map_id_vers_noeud_phrase[sous_noeud].ticket()
            
            return tickets_sous_noeuds

        #je crois que j'ai tout?




    def get_sous_noeud(self, type_sous_noeud):
        return NoeudPhrase.map_id_vers_noeud_phrase[self.sous_noeuds[type_sous_noeud]]
    
    #lorsqu'on a fini l'analyse et qu'on tombe sur une phrase, on "prévient" le noeud, 
    # qui prévient tous ces sous-noeuds
    def phrase(self):
        self.noeud_d_une_phrase = True
        #print("noeud d'une phrase : ", self.prosodic)

        for id_sous_noeud in self.sous_noeuds.values():
            NoeudPhrase.map_id_vers_noeud_phrase[id_sous_noeud].phrase()

        


        #je propage les relations sémantiques (vu que je suis une phrase)
        type_decomposition = set(self.sous_noeuds.keys())


       
        #Adj + Nom
        if type_decomposition == set(("Adj:", "Nom:" )):
            id_noeudAdj = self.sous_noeuds["Adj:"]
            id_noeudNom = self.sous_noeuds["Nom:"]
            NoeudPhrase.graphe.add_edge(id_noeudNom, id_noeudAdj, label="r_carac", w=1)
    

        #Nom + CDN 

        elif type_decomposition == set(("Nom:", "CDN:" )):
            id_noeudNom = self.sous_noeuds["Nom:"]
            id_noeudCDN = self.sous_noeuds["CDN:"]

            NoeudPhrase.graphe.add_edge(id_noeudNom, id_noeudCDN, label="r_associated", w=1)



        #groupe verbal à la forme passive
        elif type_decomposition == set(("GV:Passive:", "Prep:", "GN" )):
            id_noeudGV = self.sous_noeuds["GV:"]
            id_noeudGN = self.sous_noeuds["GV:Passive:"]
            NoeudPhrase.graphe.add_edge(id_noeudGN, id_noeudGV, label="r_agent-1", w=1)



        #GV + COD
        elif type_decomposition == set(("GV:", "COD:" )):
            id_noeudGV = self.sous_noeuds["GV:"]
            id_noeudCOD = self.sous_noeuds["COD:"]
            NoeudPhrase.graphe.add_edge(id_noeudCOD, id_noeudGV, label="r_patient-1", w=1)



        #GV + COI (même chose qu'avec le COD)
        elif type_decomposition == set(("GV:", "COI:" )):
            id_noeudGV = self.sous_noeuds["GV:"]
            id_noeudCOI = self.sous_noeuds["COI:"]
            NoeudPhrase.graphe.add_edge(id_noeudCOI, id_noeudGV, label="r_patient-1", w=1)
        
        
        #GN + GV (c'est une phrase)
        elif type_decomposition == set(("GN:", "GV:" )):
            id_noeudGN = self.sous_noeuds["GN:"]
            id_noeudGV = self.sous_noeuds["GV:"]
            NoeudPhrase.graphe.add_edge(id_noeudGN, id_noeudGV, label="r_agent-1", w=1)


        #GN + GV:Passive: (c'est une phrase à la forme passive)
        elif type_decomposition == set(("GN:", "GV:Passive:" )):
            id_noeudGN = self.sous_noeuds["GN:"]
            id_noeudGV = self.sous_noeuds["GV:Passive:"]
            NoeudPhrase.graphe.add_edge(id_noeudGN, id_noeudGV, label="r_patient-1", w=1)


        #GN + Pro: + GV (c'est une phrase (avec pronom))
        elif type_decomposition == set(("GN:","Pro:", "GV:" )):
            id_noeudGN = self.sous_noeuds["GN:"]
            id_noeudGV = self.sous_noeuds["GV:"]
            NoeudPhrase.graphe.add_edge(id_noeudGN, id_noeudGV, label="r_agent-1", w=1)



    


class Desambiguiseur:

    def __init__(self, graphe):
        
        self.inferateur = Inferateur()

        self.graphe = graphe

        self.inferateur = Inferateur()

        #moche mais bon
        NoeudPhrase.graphe = graphe

        #contiendra tous les mots générés, et les noeuds associés
        self.mots_generes = {}





    #ajoute les noeuds créés au fur et à mesure de la création du graphe
    def ajouter_noeud(self, id_noeud):

        nouveau_noeud = NoeudPhrase(id_noeud)
        
        prosodic_noeud = nouveau_noeud.prosodic


        if prosodic_noeud in self.mots_generes:
            self.mots_generes[prosodic_noeud].append(nouveau_noeud)
        else:
            self.mots_generes[prosodic_noeud] = [nouveau_noeud]


    #lorsque le graphe nous demandera de désambiguiser, des termes auront peut-être changé de r_pos ou quoi, donc on les instancie
    def update_noeuds(self):
        
        for noeud_phrase in NoeudPhrase.map_id_vers_noeud_phrase.values():
            noeud_phrase.update()
    


    def desambiguiser(self):
        #on va prendre tous les conflits un par un et on va les résoudre avec l'inférateur
        #on essaie de désambiguiser que les phrases, pas le reste
        self.update_noeuds()
        

            # print("phrase enregistrée")
            # for phrase in self.mots_generes.keys():
            #     print(phrase)

            # print("mot + r_pos  (dans noeudPhrase)")
            # for noeud in NoeudPhrase.map_id_vers_noeud_phrase.values():
            #     print(noeud.prosodic, noeud.r_pos)
        

        

        for liste_noeuds_conflits in self.mots_generes.values():

            listeConflit = []

            for noeud in liste_noeuds_conflits:
                if "S:" in noeud.r_pos:
                    listeConflit.append(noeud)

            
            

            #la phrase en question n'a qu'une seule interprétation possible,
            #le noeud est donc une phrase
            if len(listeConflit) == 1:
                listeConflit[0].phrase()
                
            
            #faut faire un tournoi de la meilleure interprétation
            elif len(listeConflit) > 1:

                gagnant = listeConflit[0]
                for adversaire in listeConflit[1:]:
                    gagnant = self.duel(gagnant, adversaire)

                gagnant.phrase()




    
    def duel(self, noeud1, noeud2):
        #fonction pour déterminer l'interprétation la plus probable

            
            ticket1, ticket2 = noeud1.ticket(), noeud2.ticket()

            # print("duel!!", noeud1.prosodic)
            # print(ticket1, ticket2)
            

            #cas le plus simple, le conflit "n'existe pas"
            if ticket1 == ticket2:
                #on garde le + récent (jsp pk)
                return noeud1
                
            

            #y a un conflit (faut faire des inférences)
            else:
                intersectionTicket = set(ticket1) & set(ticket2)

                listeInference1 = list(set(ticket1) - intersectionTicket)
                listeInference2 = list(set(ticket2) - intersectionTicket)
                

                listeScore1 = [self.inferateur.inference(*inf) for inf in listeInference1]
                listeScore2 = [self.inferateur.inference(*inf) for inf in listeInference2]

                # print(listeScore1, listeScore2)

                #on a une liste de score pour chaque interprétation, on va d'abord éliminer celle qui a le plus d'incohérence
                
                Negatif1 = [neg for neg in listeScore1 if neg < 0]
                Negatif2 = [neg for neg in listeScore2 if neg < 0]

                # Nul1 = [neg for neg in listeScore1 if neg == 0]
                # Nul2 = [neg for neg in listeScore2 if neg == 0]

                Positif1 = [neg for neg in listeScore1 if neg > 0]
                Positif2 = [neg for neg in listeScore2 if neg > 0]
                
                #d'abord on en garde un s'il est trop incohérent par rapport à l'autre
                if len(Negatif1) > len(Negatif2):
                    return noeud2
                elif len(Negatif2) > len(Negatif1):
                    return noeud1

                #ensuite on regarde c'est qui qui a le plus de sens positif
                else:
                    if len(Positif1) > len(Positif2):
                        return noeud1
                    elif len(Positif2) > len(Positif1):
                        return noeud2
                    
                    #si toujours pas, on garde juste le sens le plus probable (somme des scores)
                    else:
                        if sum(Positif1) > sum(Positif2):
                            return noeud1
                        else:
                            return noeud2




    def couper_noeud_non_phrases(self):

        self.update_noeuds()

        
        #on coupe tous les noeuds qui ne sont pas dans une phrase
        # (exécutée à la fin)

        for noeudPhrase in NoeudPhrase.map_id_vers_noeud_phrase.values():
            if not noeudPhrase.noeud_d_une_phrase:
                self.graphe.couper_noeud(noeudPhrase.id_noeud)
            #     print( "noeud coupé : ", noeudPhrase.prosodic, noeudPhrase.r_pos)

            # else:
            #     print( "appartient à une phrase : ", noeudPhrase.prosodic, noeudPhrase.r_pos)


