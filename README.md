# MGA802 — Mini-Projet A : Chiffrement de César et Énigma César

Dépôt du projet portant sur le chiffrement de César et de Énigma César réalisé par l'équipe 12


---

## Description du projet
Ce projet a pour but de réaliser un code qui permet de chiffrer et déchiffrer des messages en français à l'aide la la technique de César our de Énigma César. La méthode de César est une méthode de chiffrement par le décalage de chaque lettre par la valeur d'une clé numérique composé de 1 seul chiffre. La technique de chiffrement de Énigma César est une techique similaire mais qui utilise une clé composée de 3 chiffres qui sont applqieué successivement à chaque lettre successive et de facon répétitive. FI alemebt, le projet omporte également une fonction qui permet de brute force des messages chifférs afind e retrouver la clé et le message original.

## Installation des librairies nécessaires au projet
Le projet utilise les librairies standards suivantes :

```python
import argparse
import os
import string
import unicodedata
import re
import itertools
from time import perf_counter
```

Les tests unitaires utilisent également :

```bash
pytest
```

Installation de `pytest` :

```bash
pip install pytest
```
## Principales commandes du projet
Les commandes ci-dessous illustrent les exemples d'utilisation de chaque fonctionnalité du projet.
L'argument -c représente la clé de déchiffrement et le texte "est le message à chiffrer ou déchiffrer"
### Chiffrer César
```
python main.py chiffrer "bonjour" -c 3
```
### Déchiffrer César
```
python main.py dechiffrer "erqmrxu" -c 3
```
### Chiffrer Énigma
```
python main.py enigma "bonjour" -c 7-16-9
```
### Déchiffrer Énigma

### Brute force César

### Brute force Énigma


## Fonctions actuellement supportées
- Chiffrement César d'un message ou d'un fichhier texte
- Déchiffrement César d'un message ou d'un fichhier texte
- Chiffrement Énigma César d'un message ou d'un fichhier texte
- Déchiffrement Énigma César d'un message ou d'un fichhier texte
- Brute force d'une message en César
- Brute force d'une message en Énigma César

## Auteurs
Le code de ce projet a été réalisé par **Nicolas Allard (Nallard92), Mohammad Shohoudimojdehi (mshohoudi) et Hamza Amri-Jouidel (Hamza-MGA802)**


