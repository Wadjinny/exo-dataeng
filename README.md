# Exercice ETL Data Engineer

Cet exercice a pour but de tester des compétences d'ETL :)

Choisis ton language de prédilection (python serait un plus), et implémente un ETL qui va venir réconcilier deux Excels, très originalement appelés A.xlsx et B.xslx ;)

Chaque Excel contient des données d'américains imaginaires.

Le fichier A comporte un champ fullname, avec des potentielles typo (utilisation d'une librairie fuzzy pour en ajouter), une ville, et un âge.
Le fichier B, plus structuré, et sans fautes, comporte un champ Firstname, Name, City, email et phone.

L'idée est de créer un fichier csv qui viendrait merger ces deux données issues d'excels pour sortir des lignes réconciliées ou non de ces personnes.

Si jamais tu es très fort et que tu fais ça très vite, je suis aussi preneur d'un scénario de test Pytest du script d'ETL avec quelques données de test.

Pour info: cet exo (les csv) ont entièrement été créés par notre ami chatGPT.
Je lui ai déjà demandé de résoudre l'exerice (ainsi qu'à Claude 3.5-sonnet), du coup, merci de ne pas céder à cette tentation, cela serait rapidement visible ;)