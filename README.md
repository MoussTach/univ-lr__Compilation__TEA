Projet de TEA (Travail en accompagnement/Travail en autonomie, rayez la mention inutile)</br> 
Réalisé pour le cours de Compilation en Licence 3 à l'université de La Rochelle.
<div style="background-color:yellow; width:100%; height: 3px"></div>
<h3>Groupe :</h3>
<b>
BRENCKLE Gaetan</br>
JUBERT Baptiste</br>
DECOUTY Hugo</br>
GUITTON Elie</br>
</b></br>
<div style="background-color:green; width:100%; height: 3px"></div>
<h2>Explication du projet:</h2>
<p>
Ce projet répond aux questions et problématiques que vous pourrez retrouver dans "misc/ProjetTEA2020-2021.pdf".
Cette problématique était de pouvoir charger un automate selon un format fixe, afin de pouvoir l'executer et de pouvoir créer un .dot associé.

A cela, les automates ainsi donnés pouvaient être non-déterministes et ils devaient être rendu à souhait déterministe.
Pour ce faire, nous avons implémentés le pseudo-code vu en cours, se basant sur les lambda-transitions.
</p></br>
<div style="background-color:red; width:100%; height: 3px"></div>
<h2>Execution:</h2>
Tout se déroule sur notre classe d'automate appelé  <a href="https://en.wikipedia.org/wiki/J.A.R.V.I.S.">Jarvis</a>.</br>
<code>
Jarvis("../dir/NDSL04.descr")
</code></br>
En L'initialisant, vous devez lui donner le chemin d'un fichier correspondant au formatage attendu, tel que défini dans le fichier "misc/Format desc.txt".
A noter qu'il est possible de charger à la volé d'autres fichier .desc sur la même instance: </br>
<code>
jarvis.useFileDesc("../dir/NDSL04.descr")
</code></br>
A partir d'ici, le fichier .desc sera chargé si vous n'êtes pas confronté à l'une des nombreuses exeptions géré par notre parser.
Vous pouvez dès lors utiliser l'automate comme ceci, en lui proposant un nombre indéfini de mots. Ce dernier va lui-même les segmenter pour les lire l'un après l'autre.</br>
<code>
jarvis.useAutomate("baaabbaabb bbaabbaaa babaa")
</code></br>
Ici, vous aurez en retour une liste contenant des tuples de chacun des mots d'entrés, avec leur résultat de sorti.
A noter que si le mot venais à ne pas être cohérent, tant dans sa grammaire, selon l'automate que vous utilisez, que dans sa point d'arrêt sur son execution, notre code vous le signalera par une exception ou un retour comme output d'une information identifiant les erreurs retrouvés.</br></br>
Il est possible aussi d'afficher plus d'information sur l'execution du code avec la fonction suivante, permettant d'activer l'affichage de ces dites informations:</br>
<code>
jarvis.setVerbose(True)
</code></br></br>
A partir d'ici, vous pouvez aussi afficher sous un format .dot l'automate chargé actuellement par l'utilisation de la fonction suivante:</br>
<code>
jarvis.createDot()
</code></br>
Cela créera un fichier "graph.dot" à l'emplacement de votre classe Jarvis.</br></br>
Concernant le passage en déterminisme, cela est possible en spécifiant un tag à True dans la fonction de l'utilisation de l'automate.
Cela va générer le passage en déterministe de l'automate pour chaque mot lu.
Cependant, cela n'est que possible si vous spécifiez un ou plusieurs symboles du vocabulaire d'entrée, pour que cela soit bien pris en compte.
A ce moment, les fonctions de déterminisation prennent le relais à la place de vous afficher une execution de l'automate tel que cela à été expliqué plus tôt.
A la fin de cette éxécution, un fichier .dot appelé "determinizedGraph.dot" est généré par l'algorithme, encore une fois à l'emplacement de votre classe Jarvis.
<code>
jarvis.useAutomate("b", determinisation=True)
</code></br></br></br>
Si vous êtes amenés à utiliser la fonction verbose de notre programme avec la déterminisation comprenez le code couleur comme étant le suivant :</br>
(A noter que cette note prend en compte directement le code)</br></br>
<code>
[\33[35m]magenta = determinisation_transition</br>
[\33[34m]blue = determinisation_lambda</br>
[\33[33m]Yellow = __transiter</br>
[\33[32m]Green = __lambdafermeture</br>
White = __use</br>
</code></br>