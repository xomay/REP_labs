# Analyse de la variabilité

`variability_analysis.ipynb` lit les CSV et présente les effets des facteurs,
un arbre de décision, les tests causaux et les conclusions sur les labs 1 et 2.
Il ne lance aucune expérience et ne produit aucun fichier de données.

Depuis la racine du dépôt :

```sh
python -m pip install -r lab3/analysis/requirements.txt
python -m jupyter lab lab3/analysis/variability_analysis.ipynb
```

Dans VS Code, choisir le Python où ces dépendances sont installées.
Avant chaque commit : **Restart Kernel and Run All Cells**, puis enregistrer.

Les données sont dans `data/` :

- `observed.csv` : copie du CSV local, six configurations répétées cinq fois.
- `causal_banking.csv` et `causal_associativity.csv` : expériences causales exécutées séparément.
- `references.csv` : montants bancaires de référence.
- `provenance.csv` et `workflow_status.csv` : sources utilisées et diagnostic GitHub Actions.

Pour refaire les mesures, en dehors du notebook :

```sh
python lab3/analysis/run_experiments.py
```

Le script utilise le Python qui le lance et nécessite Java 17 et 21.
`JAVA_17` et `JAVA_21` peuvent préciser les chemins des exécutables Java.
Il remplace les CSV expérimentaux ; relancer ensuite toutes les cellules.

Le résultat attendu après retrait est **0,019992… €**.
Aucune mesure ARM n'est encore disponible : les jobs GitHub Actions ont été bloqués
par un problème de facturation. Il faudra relancer le workflow pour cette comparaison.
