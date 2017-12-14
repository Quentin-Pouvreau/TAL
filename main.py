# -*- coding: utf-8 -*-

import sys
import tweets_processing

mode = input("Que shouaitez-vous faire : \n - Créer un corpus d'apprentissage, taper 1 \n - Faire une recherche sur le harcèlement taper 2 \n")
if mode == "1":
    print("wait...")
    tweets_processing.building_learning_corpus()
elif mode == "2":
    select = input("Votre recherche porte sur : \n - Une victime, taper 1 \n - Un agresseur, taper 2 \n")
    tweets_processing.building_corpus(select)
else:
    sys.exit("Mauvaise valeur")
