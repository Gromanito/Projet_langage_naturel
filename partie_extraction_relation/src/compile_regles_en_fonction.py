"""
fichier qui est convertit une règle (txt) en une fonction python 
qui réalise (sémantiquement) ce que décrit la règle




étape 1 déjà lire le fichier hein


ensuite il faudrait que j'arrive à détecter 
quand est ce qu'une règle commence et quand est ce qu'une règle finit

je propose qu'on se facilite la tache et que nos règles aient la forme:


begin;
<partieGauche>
==>
<partieDroite>
end;




(veut dire: "si les conditions de la partie gauche sont respectées, alors la partie droite se réalise)






les fonctions associées seront de la forme:


def regle1(graphe):
    for noeud in graphe:
        if (premisse1) and (premisse2) and ... :
            <action sur le graphe>



et ce programme s'occupe de traduire chaque règle dans cette fonction en python



"""



#on ouvre le fichier txt qui contient les règles (on suppose qu'elle sont syntaxiquement correctes)


compteurRegle = 0



def recup_regles_string(fichierTxt):
   
    # Extraire les blocs de règles en enlevant "begin;" et "end;"
    regles_brutes = fichierTxt.split("begin;")[1:]  # Split à partir de "begin;" et ignorer le premier élément vide
    regles = [regle.split("end;")[0].strip() for regle in regles_brutes]  # Prendre tout ce qui est avant "end;"
    
    # Retourner la liste des règles sous forme de chaînes de caractères
    return regles



def recup_variables(regle):
    return set([ string[0].strip() for string in regle.split("$")[1:]])
    


"""
def regle1(graphe):
    for noeud in graphe.nodes:
        #pour chaque noeud, on regarde si la règle s'applique

        


        if (premisse1) and (premisse2) and ... :
            <action sur le graphe>
"""



"""
stratégie de compilation
dans chaque règle il va y avoir une prémisse avec un '=' (j'arrive pas à trouver de contre exemple)
on prend une de ces prémisses, et on fait comme si le noeud qu'on est en train de tester était le = qqc

par exemple la règle 
$x = DET:
& $y = GN:
& $x r_succ $y

on va dire que le noeud qu'on teste correspond à la variable $x (juste prck c'est la première prémisse à avoir un = )
"""






def compile_regle_en_fonction(regleString):

    conversifs={"r_succ":"r_pred", "r_pred":"r_succ"}


    partieGauche, partieDroite = regleString.split("==>")[0], regleString.split("==>")[1]
    
    listePremisses = partieGauche.split("&")
    listeActions = partieDroite.split("&")


    # on sépare les prémisses en 2 types : 
    #   celles avec "=" ($x = DET:)
    #   celles avec r_succ ($x r_succ $y)

    listePremissesTestLabel = []
    listePremissesSucc = []
    for premisse in listePremisses:
        if premisse.find("=") == -1:
            listePremissesSucc.append(premisse)
        else:
            listePremissesTestLabel.append(premisse)

    

    #je commence vite fait à écrire le code de la fonction (que le corps de la fonction, pas la signature, ça sera fait en dehors)

    stringCodeFonction = \
    """\
    for noeud{variableDebut} in graphe.nodes:
        if noeud{variableDebut}['label'] == {labelDebut}:
    """

    premisseDebut = listePremissesTestLabel.pop(0)
    variableDebut = recup_variables(premisseDebut)[0]
    labelDebut = premisseDebut.split("=")[1].strip()

    #on récupère les variables de la partieGauche
    variablesPasInstanciees = list(recup_variables(partieGauche))
    variablesPasInstanciees.remove(variableDebut)

    variablesTestLabel = recup_variables('\n'.join(listePremissesTestLabel))

    variablesInstanciees = [variableDebut]

    #tant qu'il reste des prémisses avec r_succ, on continue "d'instancier" les variables aux noeuds

    #chiant à expliquer mais si on a instancié un noeud à la variable x, il faut réussir à instancier d'autres noeuds mais à partir de x
    # donc on chercher des prémisses de la forme $x qqc $z    ou  $y qqc $x ,  bref il faut qu'il y ait x qui apparaisse quelque part, sinon on lie les variables à absolument tous les noeuds possibels et c'est long

    nombreTabulation = 3
    templatePremisse_r_succ = "for noeud{variablePasInstanciee} in graphe.successors(noeuds{variableInstanciee}):"
    templatePremisseTestLabel = "if noeud{variable}['label'] == {POS}:"

    templateActionCreerNoeud = """\
{nombreTabulation}noeud{nouvelleVariable} = graphe["compteur"]
{nombreTabulation}graphe["compteur"] += 1
{nombreTabulation}graphe.add_node(noeud{nouvelleVariable}, {'label':'{POS}', 'w':1})
"""

    templateActionRelierArete = """\
{nombreTabulation}graphe.add_edge(noeud{variable}, noeud{nouvelleVariable}, {'w':1, 'rel':'{relation}'})
{nombreTabulation}graphe.add_edge(noeud{nouvelleVariable}, noeud{variable}, {'w':1, 'rel':'{relation}'})
"""

    #on s'occupe d'abord de la partie gauche (des prémisses)
    while listePremissesSucc:
        
        #on va choisir des prémisses dans lesquelles y a des variables déjà instanciées
        #et si possible une variable qui est dans un test label
        premisseCandidate = None
        yAeuUnBreak = False #c'est moche mais vasy j'ai la flemme de réfléchir

        for premisse in listePremissesSucc:
            variablesPremisse = recup_variables(premisse)
            if (variablesPremisse[0] in variablesInstanciees and variablesPremisse[1] in variablesTestLabel)\
            or\
            (variablesPremisse[1] in variablesInstanciees and variablesPremisse[0] in variablesTestLabel):
                premisseCandidate = premisse



            #cas particulier ou la prémisse contient 2 variables déjà instanciées, y a juste un test à faire
            elif variablesPremisse[0] in variablesInstanciees and variablesPremisse[1] in variablesInstanciees:
                if '$'+variablesPremisse[0] in premisse.split('r_succ')[0]:
                    variableGauche = variablesPremisse[0]
                    variableDroite = variablesPremisse[1]
                else:
                    variableGauche = variablesPremisse[1]
                    variableDroite = variablesPremisse[0]
                stringCodeFonction += '\n' + '\t' * nombreTabulation + "if noeud{variableGauche} in in graphe.successors(noeuds{variableDroite}):".format(variableGauche = variableGauche, variableDroite = variableDroite)
                listePremissesSucc.remove(premisse)
                nombreTabulation += 1
                yAeuUnBreak = True
                break

        #ça c'est si j'avais eu un cas particulier, et que je voulais break mais j'étais déjà dans le boucle for et en fait je voulais break de la boucle while(il est long le commentaire wesh)
        if yAeuUnBreak:
            yAeuUnBreak = False
            break



        #y a pas de prémisse qui amène à un test rapidement: bah on prend une prémisse qui au moins fait une liaison
        if premisseCandidate == None:
            for premisse in listePremissesSucc:
                variablesPremisse = recup_variables(premisse)
                if (variablesPremisse[0] in variablesInstanciees or variablesPremisse[1] in variablesInstanciees):
                premisseCandidate = premisse




        # on a une premisse qui permet de lier une variable à un noeud, on la traite

        # on regarde quelle variable est celle instanciée et quelle variable ne l'est pas
        variablesPremisse = recup_variables(premisseCandidate)
        variableInstanciee = variablesPremisse[0]
        nouvelleVariable = variablesPremisse[1]

        if variablesPremisse[1] in variablesInstanciees:
            nouvelleVariable, variableInstanciee = variableInstanciee, nouvelleVariable


        #on a notre prochain noeud, on ajoute le code
        stringCodeFonction += '\n' + '\t' * nombreTabulation + templatePremisse_r_succ.format(variableInstanciee = variableInstanciee,   variablePasInstanciee = nouvelleVariable) + '\n'

        nombreTabulation += 1

        #on peut faire un test de label sur cette variable, on le fait (il faut d'abord récupérer la prémisse)
        if nouvelleVariable in variablesTestLabel:
            stringCodeVariable = '$' + nouvelleVariable
            for premisseLabel in listePremissesTestLabel:
                if stringCodeVariable in premisseLabel:
                    label = premisseLabel.split("=")[1].strip()
                    stringCodeFonction += '\n' + '\t' * nombreTabulation + templatePremisseTestLabel.format(variable = nouvelleVariable,   POS = label) + '\n'
                    listePremissesTestLabel.remove(premisseLabel)
                    variablesTestLabel.remove(nouvelleVariable)
                    nombreTabulation += 1
        

        #on a fini de traiter cette prémisse, on actualise les listes et on passe à la suivante
    
        variablesInstanciees += nouvelleVariable
        variablesPasInstanciees.remove(nouvelleVariable)
        listePremissesSucc.remove(premisseCandidate)

    


    #on a fini de traiter la partie gauche de la règle (ouf)
    #maintenant on s'occupe de la partie droite

    # déjà faut voir si des noeuds ont été créés
    