# Projet_langage_naturel


les trucs à installer : 

pip install requests-html


pour lancer, se mettre à la racine du projet et lancer la commande 

python3 ./src/main.py 

ou bien (pour refaire des anciennes inférences)

rlwrap python3 ./src/main.py 




les inférences sont stockées dans src/schema_inference.json dans un format particulier


En se demandant comment était effectuée une inférence, nous avons modélisé ceci:


pour réaliser une inférence  A rt B,
Nous passons par un intermédiaire C,   et nous faisons par exemple,

A rt1 C  &   C rt2 B,   donc  A rt B

Cela nécessite d'extraire les noeuds sortants de A par la relation rt1, et ensuite de vérifier si ces noeuds sont bien en relation avec B (en prenant le conversif depuis B pour ne pas avoir à télécharger chaque noeud à chaque fois)


nous avons séparé les inférences en deux types : les inférences "triangles", qui ne nécessitent qu'un seul intermédiaire (le "C") et les inférences "carrés", qui nécessitent deux intermédiaires 

le format json pour les relation triangles sont comme ceci :
(exemple pour une inférence déductive)

{           
    "nombreInf":2,
    "C":"A;r_isa",
    "inference": "C;rt;B",
    "score":"0.5;1.5"
 }

    - nombreInf désigne le nombre d'inférences à montrer pour ce schéma


    - "C" désigne comment sont extraits les noeuds intermédiaires à partir de quel terme et avec quelle relation (ici, prendre tous les x tels que A r_isa x)


    -"inference" désigne le lien entre les intermédiaires et le noeud à atteindre, et avec quelle relation

    ici tous les x tels que x rt B 
    rt désigne la relation demandée en entrée, puisque l'inférence déductive est générique, cela peut être n'importe laquelle

    par exemple  A r_agent-1 B    ->     A r_isa x   &   x r_agent-1 B
                A r_patient B    ->     A r_isa x   &   x r_patient B


    -"score" sert à mettre un poids entre la relation qui sert à extraire les intermédiaires et la relation qui sert à faire l'inférence

    par exemple pour     A r_isa x   &   x r_agent-1 B,   
    qu'est ce qui est le + important?   que A r_isa x   ou  que x r_agent-1 B ?

    le premier et le deuxième coefficient servent à indiquer l'importance de l'intermédiaire et de l'inférence respectivement




Calcul du score (triangle):

Pour savoir si une inférence  A rt1 C  &  C rt2 B   est une bonne inférence, on se réfère au poids de    A rt1 C   et de    C rt2 B
si jamais un poids est plus important qu'un autre on modifie son importance comme cela:


soit p1 le poids de A rt1 C  et p2 le poids de C rt2 B

on calcule leur importance relative (impRel) dans l'inférence avec ce calcul:

impRel1 = p1 / (p1 + p2)
impRel2 = p2 / (p1 + p2)

on modifie maintenant cette importance avec les coefficients renseignés.
(avec l'exemple json plus haut)

impRel1 = impRel1 * 0.5
impRel2 = impRel2 * 1.5

on calcul ensuite le score qui est une simple multiplication:

score = (p1*impRel1) * (p2 * impRel2)

((((puisque la multiplication est associative, on n'impacte pas vraiment le poids directement de p1 et de p2, mais on modifie le score global p1*p2 avec des "bonus" et des "malus" selon l'inférence ))))
    




inférence carré: c'est la même chose mais y a deux intermédiaires cette fois

