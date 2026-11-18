# REP — Travaux pratiques

Ce dépôt étudie la reproductibilité des calculs numériques à travers deux problèmes :
l'associativité de l'addition et le problème du placement bancaire. Il compare plusieurs
implémentations, génère des variantes et analyse les facteurs qui influencent les résultats.

## Organisation

```text
lab1/                  Premières implémentations et réponses
lab2/                  Travaux du deuxième laboratoire
llm-lab2/              Solutions Java/Python du LLM et historique des échanges
lab3/
  Banking.uvl          Modèle des configurations possibles
  sample.py            Sélection des configurations dans un CSV
  generate.py          Génération de tests de propriétés arithmétiques
  configs/             Configurations sélectionnées
  serializing/         Templates, génération et exécution des variantes bancaires
  analysis/            Notebook d'analyse, expériences causales et CSV
.github/workflows/     Automatisation avec GitHub Actions
```

Le fonctionnement principal suit cette chaîne :
**modèle UVL → configurations CSV → programmes générés → résultats CSV → notebook**.

## Reproduire les résultats

Les commandes suivantes s'exécutent depuis la racine du dépôt.
Utiliser Python 3.12 et, pour les variantes Java, les JDK 17 et 21.

### 1. Préparer l'environnement

```sh
python3.12 -m venv .env
source .env/bin/activate
python -m pip install -r lab3/analysis/requirements.txt flamapy==2.6.0
```

### 2. Générer et exécuter les variantes

```sh
python lab3/sample.py lab3/Banking.uvl --size 14 --seed 1 -o lab3/configs/sample.csv
python lab3/serializing/run_sample.py
```

Le script exécute chaque configuration cinq fois et écrit les réponses dans
`lab3/serializing/results.csv`. Les runtimes absents sont signalés et ignorés ;
`--strict` permet de faire échouer l'exécution à la place.
Pour couvrir toutes les configurations, il faut aussi Python 3.10, 3.11 et PyPy.
Les chemins des exécutables peuvent être adaptés dans le script ; voir le
[README des variantes](lab3/serializing/README.md).

Pour générer les tests d'associativité et de distributivité :

```sh
python lab3/generate.py
```

### 3. Consulter l'analyse

```sh
python -m jupyter lab lab3/analysis/variability_analysis.ipynb
```

Le notebook lit les CSV fournis dans `lab3/analysis/data/` sans lancer d'expérience.
Il présente les effets des facteurs, un arbre de décision et les conclusions sur
les labs 1 et 2. Les résultats locaux des variantes ne remplacent pas automatiquement
les CSV conservés pour cette analyse.

Pour refaire les expériences causales, séparément du notebook :

```sh
python lab3/analysis/run_experiments.py
```

Avant chaque commit du notebook : **Restart Kernel and Run All Cells**, puis enregistrer.
Les détails sont dans le [README de l'analyse](lab3/analysis/README.md).

## GitHub Actions

Le workflow **Banking results** lance la chaîne bancaire sur `ubuntu-24.04` et
`ubuntu-24.04-arm`, avec les versions Python et Java du modèle. Il se déclenche
sur les modifications de `lab3` ou du workflow, ou manuellement depuis l'onglet Actions.
Il enregistre les CSV par commit dans `lab3/serializing/results/`.

La première tentative a été bloquée par un problème de facturation du compte GitHub.
L'analyse fournie ne contient donc pas encore de comparaison ARM/x86.

## Utilisation de l'IA

Une intelligence artificielle a été utilisée pour certaines parties du travail,
notamment les solutions du lab 2, l'automatisation et l'aide à l'analyse et à la rédaction.
Son utilisation ne se limite pas aux fichiers identifiés comme « LLM » : elle a aussi
pu servir d'aide à l'écriture ou à la correction d'autres parties du code.
Le dossier [llm-lab2](llm-lab2/) regroupe les solutions et les échanges réalisés
dans le cadre de l'exercice qui demandait explicitement de faire appel à un LLM.

L'auteur conserve la pleine responsabilité du code, des résultats et des conclusions.
