"""
fichier qui est convertit une règle (txt) en une fonction python 
qui réalise (sémantiquement) ce que décrit la règle




faudrait que j'arrive à détecter 
quand est ce qu'une règle commence et quand est ce qu'une règle finit

je propose qu'on se facilite la tache et que nos règles aient la forme:


begin;
<partieGauche>
==>
<partieDroite>
end;


(veut dire: "si les conditions de la partie gauche sont respectées, alors la partie droite se réalise)



dans la partie gauche, pour indiquer les précédents/successeurs, on utilisera
UNIQUEMENT r_succ et non pas r_pred
(pour pas se faire chier)
edit : je crois que ça marche quand même au final mais j'ai pas testé




les fonctions associées seront de la forme:


def regle1(graphe):
    for noeud in graphe:
        if <prémisses respectées>
            create node .... etc




le fait que des prémisses soient respectées c'est pas juste des "if", quand y aura des
"r_succ", il faudra faire un "for succ in successors($x)" , et donc ça va être chiant mais bon




et ce programme s'occupe de traduire chaque règle dans cette fonction en python


pour pas que ce programme déjà compliqué le soit encore plus, 
je fais appel à des méthodes de la classe héritée "Graphe", 
comme ça je délègue des bouts de code à un autre fichier

et pareil je fais appel des fonctions de MoteurRegle qui gere si des regles ont déjà été appliquées 
et d'autres trucs





"""



#on ouvre le fichier txt qui contient les règles (on suppose qu'elle sont syntaxiquement correctes)


compteurRegle = 0



def recup_regles_string(fichierTxt):
   
    # Extraire les blocs de règles en enlevant "begin;" et "end;"
    regles_brutes = fichierTxt.split("begin;")[1:]  # Split à partir de "begin;" et ignorer le premier élément vide
    regles = [regle.split("end;")[0].strip() for regle in regles_brutes]  # Prendre tout ce qui est avant "end;"
    # Retourner la liste des règles sous forme de chaînes de caractères
    return regles


#recupère les variables d'un bout de string (le caractère après les $)
def recup_variables(regle):
    return [ string[0].strip() for string in regle.split("$")[1:]]
    

#récupère la variable à gauche et à droite ($x r_succ $y) -> x, y
def recup_variables_gauche_droite(premisseOuAction):
    indexPremierDollar = premisseOuAction.find('$')
    variableGauche = premisseOuAction[indexPremierDollar+1]
    variableDroite = premisseOuAction[premisseOuAction.find('$', indexPremierDollar+1) +1 ]
    return variableGauche, variableDroite






"""
stratégie de compilation
dans chaque règle, on va d'abord tester les choses testables directement,


par exemple   
"si x -> y    et   si x = Nom:"
si on fait
pour tout x,
    pour tout les successeurs de x,
        si x = Nom:
            blabla...




si x est pas égal à Nom: on va passer dans le if autant de fois qu'il y a de successeurs,
alors qu'on pourrait juste tester x direct avec

pour tout x,
    si x = Nom:
        pour tout les successeurs de x,
            blabla...


dooooonc, on va remonter le plus possible les prémisses qui testent une condition le plus haut possible dans l'arbre



Pour les actions, on va, en général, créer un nouveau noeud du graphe
Ce noeud sera un noeud qui couvrira plusieurs noeuds déjà existants (et existants dans les prémisses )
on va avoir une action de type  $n < [$x,$y,$z]
qui veut dire "crée le nouveau noeud $n, qui couvre x y et z (dans cet ordre)
(et ça doit suivre l'ordre des r_succ dans les prémisses of course)




"""

def premisse_candidate(premissesName, premisses_r_poss, premissesRelation, variablesInstanciees):
    #ptite fonction qui retourne la premisse "idéale" à traiter

    

    #on essaye d'abord avec les prémisses Name

    for premisse in premissesName:
        for variable in recup_variables(premisse):
            if variable in variablesInstanciees:
                return premisse, 'Name'
    

    #on essaye ensuite avec les prémisses r_pos

    for premisse in premisses_r_poss:
        for variable in recup_variables(premisse):
            if variable in variablesInstanciees:
                return premisse, 'r_pos'
    
    
    #si y a pas, on prend une prémisses Relation

    for premisse in premissesRelation:
        for variable in recup_variables(premisse):
            if variable in variablesInstanciees:
                return premisse, 'Relation'

    print(premissesName)
    print(premisses_r_poss)
    print(premissesRelation)
    print('test')






def compile_regle_en_fonction(nomRegle, regleString):




    partieGauche, partieDroite = regleString.split("==>")[0], regleString.split("==>")[1]
    
    listePremisses = partieGauche.split("&")
    listeActions = partieDroite.split("&")



    # on sépare les prémisses en 2 types : 
    #   celles avec "=" ($x = "être"), on teste le nom du noeud, le terme quoi
    #   celles avec une relation ($x r_succ $y,  $x r_succ $y)

    listePremissesName = []
    listePremisses_r_poss = []
    listePremissesRelation = []

    for premisse in listePremisses:
        if premisse.find("=") != -1:
            listePremissesName.append(premisse)
        else:
            if 'r_pos' in premisse:
                listePremisses_r_poss.append(premisse)
            else:
                listePremissesRelation.append(premisse)

    

    
    
    

    #chiant à expliquer mais si on a instancié un noeud à la variable x, il faut réussir à instancier d'autres noeuds mais à partir de x
    # donc on cherche des prémisses de la forme $x qqc $z    ou  $y qqc $x ,  bref il faut qu'il y ait x qui apparaisse quelque part, sinon on lie les variables à absolument tous les noeuds possibles et c'est long
    
    #par exemple si j'ai  $x r_succ $y     $y r_succ $z     $z r_succ $t
    # je peux pas faire          
    
    # pour y tous les successeurs de x:
    #     pour t tous les successeurs de z:      
    
    #t et z pas encore instanciés, faut d'abord faire  


    # pour y tous les successeurs de x:
    #     pour z tous les successeurs de y:   
    #           ...   




    

    variableCentrale = listePremisses[0].split('$')[1][0]

    #on mémorise les variables qui ont été instanciées 
    variablesInstanciees = [variableCentrale]

    #tant qu'il reste des prémisses avec r_succ, on continue "d'instancier" les variables aux noeuds

   



    #je commence vite fait à écrire le code de la fonction (que le corps de la fonction, pas la signature, ça sera fait en dehors)


    stringCodeFonction = \
    """\
\tnomRegle = '{nomRegle}'
\tfor noeud_{variableCentrale} in graphe.get_all_nodes_terme():
""".format(nomRegle = nomRegle, variableCentrale = variableCentrale)



    nombreTabulation = 1


    templatePremisseRelation = "for noeud_{variablePasInstanciee} in graphe.get_{sens}_with_labelled_edge(noeud_{variableInstanciee}, '{relation}'):\n"
    templatePremisse_r_pos = "if '{pos}' in graphe.get_r_pos_of_node(noeud_{variableInstanciee}) :\n"
    templatePremisse_name = "if '{name}' == graphe.nodes[noeud_{variableInstanciee}]['name']:\n"
    
    #je sais pas s'il faudrait faire un template "relation" mais bon j'ai pas l'impression, et au pire 


    #on s'occupe d'abord de la partie gauche (des prémisses)
    while listePremisses:

        
        nombreTabulation += 1
        
        #on va choisir des prémisses dans lesquelles y a des variables déjà instanciées
        #et si possible une variable qui teste un r_pos ou un name



        premisseChoisie, typePremisse = premisse_candidate(listePremissesName, listePremisses_r_poss, listePremissesRelation, variablesInstanciees)
        

        #si on traite une prémisse Name, il faut juste rajouter un if avec le template et la bonne valeur
        if typePremisse == 'Name':
            listePremissesName.remove(premisseChoisie)
            listePremisses.remove(premisseChoisie)

            variable = recup_variables(premisseChoisie)[0]
            valeurName = premisseChoisie.split('"')[1]

            stringCodeFonction +=  '\t' * nombreTabulation + templatePremisse_name.format(name=valeurName, variableInstanciee = variable)
            


        #si on traite une prémisse r_pos, c'est juste un if avec le bon template aussi, oklm
        if typePremisse == 'r_pos':
            listePremisses_r_poss.remove(premisseChoisie)
            listePremisses.remove(premisseChoisie)

            variable = recup_variables(premisseChoisie)[0]
            valeur_r_pos = premisseChoisie.strip().split(' ')[-1]

            stringCodeFonction +=  '\t' * nombreTabulation + templatePremisse_r_pos.format(pos=valeur_r_pos, variableInstanciee = variable)


        #si c'est un r_succ, un peu chiant (faut voir dans quel sens est le r_succ, et faire la boucle blabla)
        if typePremisse == 'Relation':
            listePremissesRelation.remove(premisseChoisie)
            listePremisses.remove(premisseChoisie)

            relation = 'r_' + premisseChoisie.split('r_')[1].split(' ')[0]

            variableGauche, variableDroite = recup_variables_gauche_droite(premisseChoisie)

            #la variable à gauche du r_succ a été instanciéé et pas celle de droite
            if variableGauche in variablesInstanciees and variableDroite not in variablesInstanciees:

                stringCodeFonction +=  '\t' * nombreTabulation +  templatePremisseRelation.format(variablePasInstanciee=variableDroite, variableInstanciee = variableGauche, sens='successors', relation=relation)
                variablesInstanciees.append(variableDroite)
                continue


            #la variable à gauche du r_succ n'a pas été instanciéé mais celle de droite oui
            if variableGauche not in variablesInstanciees and variableDroite in variablesInstanciees:

                stringCodeFonction +=  '\t' * nombreTabulation +  templatePremisseRelation.format(variablePasInstanciee=variableGauche, variableInstanciee = variableDroite, sens='predecessors', relation=relation)
                variablesInstanciees.append(variableGauche)
                continue

            #les deux variables ont été instanciées, il s'agit juste d'un test
            if variableGauche in variablesInstanciees and variableDroite in variablesInstanciees:

                stringCodeFonction +=  '\t' * nombreTabulation +  "if noeud_" + variableDroite + " in graphe.get_successors_with_labelled_edge(noeud_" + variableGauche + ", 'r_succ'):\n"
                continue

        
    nombreTabulation += 1




    # on vient de traiter les prémisses

    # ptite optimisation,
    # Quand toutes les prémisses ont été "validées" (on va produire une action)
    # on va envoyer un "ticket" au moteur de règle pour lui dire "j'ai trouvé ce pattern"
    # le moteur de règle va voir si ces prémisses ont pas déjà été validées par le passé,
    # et donc si ces actions ont pas déjà été effectuées avant
    # un ticket c'est juste de la reconnaissance de pattern, c'est à dire,
    # pour chaque variable $x, $y, blabla, on a associé un noeud du graphe
    # par exemple $x -> 3   $y -> 16    etc
    # donc c'est juste une substitution, qu'on garde en mémoire, 
    # et à chaque fois qu'une règle trouve une substitution, elle demande au moteur de règle
    # si ça a pas déjà été fait, et, le cas échéant, elle fait rien



    stringSubstitution = "("
    for variable in variablesInstanciees:
        stringSubstitution += "('" + variable + "', noeud_" + variable + '), '
    
    stringSubstitution = stringSubstitution[:-2] + ')'
    
  
    
    
    
    stringCodeFonction +=  '\t' * nombreTabulation + "regleDejaAppliquee = moteurRegle.regle_deja_appliquee('" + nomRegle + "', " + stringSubstitution + ")\n"
    stringCodeFonction +=  '\t' * nombreTabulation + "if not regleDejaAppliquee:\n"

    nombreTabulation += 1




    #on vient de traiter la partie gauche de la règle (ça veut dire, le corps de la fonction existe)
    #on passe maintenant à la partie droite (les actions)
            
    templateActionCreerNoeud = "noeud_{nouvelleVariable} = graphe.creer_noeud_regle('terme', *{liste_noeuds_couverts} )\n"
    templateActionAjouter_r_pos = "graphe.add_r_pos_to_node('{pos}', noeud_{variable})\n"
    templateActionAjouterArete = "graphe.add_edge(noeud_{node1}, noeud_{node2}, label='{label}', w=1)\n"



    #on va d'abord crée les nouveaux noeuds
    # on les repère prck la règle de création c'est :  $n < [$x,$y,$z]


    

    listeActionsCreerNoeuds = []

    for action in listeActions:
        if '<' in action:
            listeActionsCreerNoeuds.append(action)
            listeActions.remove(action)

    
  
    #parmi toutes les actions à faire, on s'occupe d'abord des nouveaux noeuds à créer
    for action in listeActionsCreerNoeuds:
        nouvelleVariable = action.split('<')[0].strip()[1]
        liste_noeuds_couverts = action.split('<')[1].strip().replace('$', 'noeud_')

        # print(liste_noeuds_couverts)

        stringCodeFonction += '\t' * nombreTabulation + templateActionCreerNoeud.format(nouvelleVariable=nouvelleVariable, liste_noeuds_couverts = liste_noeuds_couverts)



    #une fois qu'on a créé tous les noeuds, on s'occupe des r_pos et des ajouts d_arêtes
    
    for action in listeActions:
        
        #il faut ajouter un noeud r_pos
        if 'r_pos' in action:
            variable = recup_variables(action)[0]
            pos = action.split('r_pos')[1].strip()

            stringCodeFonction += '\t' * nombreTabulation + templateActionAjouter_r_pos.format(pos=pos, variable = variable)

        #il faut ajouter une arête avec le bon label
        else:
            label = 'r_' + action.split('r_')[1].split(' ')[0]
            variableGauche, variableDroite = recup_variables_gauche_droite(action)

            stringCodeFonction += '\t' * nombreTabulation + templateActionAjouterArete.format(node1= variableGauche, node2=variableDroite, label = label)


    

    #on a traité toutes les actions ........
    # Je crois bien que c'est fini .........

    return stringCodeFonction





#creation de toutes les fonctions + écriture dans un fichier

#on récupère les règles haut niveau
with open("partie_extraction_relation/res/regles.txt", 'r', encoding='utf-8') as fichier:
    chaine = fichier.read()
    regles =  recup_regles_string(chaine)




templateSignature = "def {nomRegle}(graphe, moteurRegle):\n"



with open("partie_extraction_relation/src/regles_compilees.py", 'w', encoding='utf-8') as fichier:
    for i in range(len(regles)):
        nomRegle = "regle"+str(i)
        fonction_regle = compile_regle_en_fonction(nomRegle, regles[i])

        fichier.write(templateSignature.format(nomRegle=nomRegle))
        fichier.write(fonction_regle)
        fichier.write('\n\n\n')

