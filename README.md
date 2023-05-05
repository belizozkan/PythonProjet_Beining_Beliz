# PythonProjet_Beining_Beliz

## README.md

C'est un fichier qui informe sur le contenu de tous les autres fichiers déposés sur GitLab.

## Utilisation

Ce code est écrit en Python et utilise les modules stanza, spacy, ufal.udpipe, parse, os, urllib.request et xml.etree.ElementTree. Les instructions pour l'installation de ces modules sont disponibles en ligne. Il est très important que les utilisateurs installent la bibliothèque stanza spacy et udpipe à l'avance avant d'utiliser le code.

Les bibliothèques Stanza, UDPipe et SpaCy peuvent être installées en utilisant la commande pip depuis un terminal ou une ligne de commande, en fonction du système d'exploitation utilisé.

Pour installer Stanza, vous pouvez utiliser la commande suivante:
pip install stanza

Pour installer SpaCy, vous pouvez utiliser la commande suivante:
pip install spacy

Pour installer UDPipe, vous pouvez utiliser la commande suivante:
pip install ufal.udpipe

(Téléchargez également le fichier french-partut-ud-2.5-191206.udpipe ou french-gsd-ud-2.5-191206.udpipe pour le modèle que vous souhaitez utiliser.)

Disposant d'une série de fonctions Python, ce code fusionne les résultats de différents analyseurs, tels que Spacy, UDPipe et Stanza, dans un même fichier CoNLL-U. Les fonctions développées permettent d'intégrer des colonnes telles que LEMMA, POS, FEA et DEPREL dans le fichier CoNLL-U. Il est possible personnaliser le processeur en modifiant les outils et les modèles utilisés pour le lemmatisation, l'étiquetage morpho-syntaxique, l'analyse syntaxique et la représentation en fonctionnalités.

Ce code Python contient deux classes : xml_conll et process.

### xml_conll ###

Ce code Python est une classe nommée xml_conll qui contient des méthodes pour transformer un fichier XML en format CoNNLu. Le format CoNNLu est un format de données utilisé pour représenter les annotations linguistiques, en particulier pour les tâches d'analyse syntaxique.

La classe xml_conll contient trois méthodes principales :

# Méthode tokenize #
(text:str) -> list : Cette méthode prend une chaîne de caractères text en entrée et retourne une liste de tokens. Elle parcourt chaque caractère du texte et sépare les mots en fonction des espaces et des ponctuations spécifiées dans la liste punctuations.

# Méthode find_offset #
(tokens, data) -> list : Cette méthode prend une liste de tokens tokens et une chaîne de caractères data en entrée et retourne une liste d'entiers correspondant au décalage de chaque token dans le texte. Elle utilise la méthode index() de la chaîne de caractères pour trouver le décalage de chaque token dans le texte.

# Méthode xml_to_conllu # 
(input_file, output_file, xpath_expression): Cette méthode prend trois arguments : le nom du fichier d'entrée input_file, le nom du fichier de sortie output_file et une expression XPath xpath_expression. Elle analyse le fichier d'entrée en utilisant la bibliothèque xml.etree.ElementTree, récupère le texte du fichier en utilisant l'expression XPath, tokenize le texte, calcule le décalage de chaque token dans le texte, formate les données dans le format CoNNLu et écrit le résultat dans le fichier de sortie.

La méthode xml_to_conllu() fait appel aux deux autres méthodes pour réaliser la transformation. Elle commence par parser le fichier XML et récupérer le texte à traiter en utilisant l'expression XPath spécifiée. Ensuite, elle tokenise le texte, calcule le décalage de chaque token dans le texte, formatte les données pour le format CoNNLu et écrit le résultat dans le fichier de sortie.

### process ###

Ce code contient une classe nommée "process" qui a trois méthodes suivantes pour traiter des fichiers textes avec différents modèles du traitement du langage naturel :

# Méthode process_stanza #
Cette méthode utilise la bibliothèque Stanza pour effectuer une analyse NLP sur les données d'entrée. La méthode lit un fichier texte et utilise la fonction parse du module "conllu" pour diviser le texte en phrases. Ensuite, pour chaque phrase, elle effectue une analyse NLP en utilisant le pipeline Stanza pour le français, puis stocke les résultats dans une liste. Les résultats incluent des informations telles que l'ID du mot, sa forme, son lemme, sa partie du discours, ses traits morphologiques, son dépendant (HEAD) et sa relation de dépendance (DEPREL).

# Méthode process_spacy #
Cette méthode utilise la bibliothèque Spacy pour effectuer une analyse NLP sur les données d'entrée. La méthode lit un fichier texte et utilise la fonction parse du module "conllu" pour diviser le texte en phrases. Ensuite, pour chaque phrase, elle effectue une analyse NLP en utilisant le modèle Spacy chargé en paramètre, puis stocke les résultats dans une liste. Les résultats incluent des informations telles que l'ID du mot, sa forme, son lemme, sa partie du discours, ses traits morphologiques, son dépendant (HEAD) et sa relation de dépendance (DEPREL).

# Méthode process_udpipe #
Cette méthode utilise le modèle UDPipe pour effectuer une analyse NLP sur les données d'entrée. La méthode télécharge le modèle UDPipe pour le français depuis une URL donnée, puis charge le modèle et l'utilise pour initialiser un pipeline UDPipe. Ensuite, la méthode lit un fichier texte et utilise le pipeline UDPipe pour effectuer une analyse NLP sur les données d'entrée, puis stocke les résultats dans une liste. Les résultats incluent des informations telles que l'ID du mot, sa forme, son lemme, sa partie du discours, ses traits morphologiques, son dépendant (HEAD) et sa relation de dépendance (DEPREL).

### main ###

Le main permettra d'éxecuter ce code qui traite un fichier d'entrée en utilisant différents outils de traitement de langage naturel et crée un fichier de sortie qui contient les informations de chaque token dans le format CoNLL-U. Les suivants sont utilisés à cet effet : xml_conll et process.

Le code :

Importe les bibliothèques xml_conll et process ainsi que la bibliothèque os.
Définit différentes variables qui personnalisent le processeur en fonction des outils et des modèles de langue choisis.
Définit une fonction process_dict pour traiter un fichier d'entrée en utilisant différents outils de traitement et créer un dictionnaire de tokens.
Définit une fonction dict_to_conllu_line pour convertir un dictionnaire de token en une ligne au format CoNLL-U.
Définit une fonction dicts_to_conllu_sentence pour convertir une liste de dictionnaires de tokens en une phrase au format CoNLL-U.
Définit une fonction write_offset pour écrire des informations telles que le décalage dans un nouveau fichier.
Obtient le chemin absolu du fichier actuel pour faciliter l'accès au fichier plus tard.
Appelle la fonction process_dict pour traiter le fichier d'entrée avec différents outils et créer une liste de dictionnaires de tokens.
Appelle la fonction dicts_to_conllu_sentence pour convertir la liste de dictionnaires de tokens en une phrase au format CoNLL-U.
Écrit les informations dans un fichier de sortie et ajoute les décalages à chaque ligne du fichier de sortie en appelant la fonction write_offset.

## french-gsd-ud-2.5-191206.udpipe & french-partut-ud-2.5-191206.udpipe

C'est un modèle de traitement du langage naturel pour le français, qui utilise le format de représentation linguistique Universal Dependencies (UD).

## output_nlp.txt

Le fichier obtenu après avoir utilisé la classe process.

## output_xml_to_conllu.txt

Le fichier obtenu après avoir utilisé la classe xml_conll. 

## input_conllu.txt

Le fichier à utiliser pour tester la classe process. 

## input_xml.xml

Le fichier à utiliser pour tester la classe xml_conll. 
