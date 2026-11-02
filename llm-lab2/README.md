# Deux problemes numeriques en Java et Python

Versions Python 3, sans dependance externe :

```sh
python3 associativity.py
python3 associativity.py 100000
python3 banking.py
```

`associativity.py` reprend les quatre experiences de la version Java.
Les `int` Python sont des entiers de precision arbitraire : leurs additions
sont exactes. Les `float` jouent ici le role des `double` Java. Les tirages
Python et Java different : leurs pourcentages experimentaux peuvent differer.
Les valeurs et sommes flottantes de ces experiences restent finies.
`banking.py` utilise `decimal.Decimal` a 100 chiffres et controle son resultat
avec une seconde evaluation a 120 chiffres. Il utilise la meme serie stable
et les memes hypotheses que la version Java expliquee ci-dessous.

Depuis ce dossier, avec Java 17 ou plus recent :

```sh
javac -d /tmp/llm-lab2-classes Associativity.java Banking.java
java -cp /tmp/llm-lab2-classes Associativity
java -cp /tmp/llm-lab2-classes Banking
```

`Associativity` accepte un nombre de triplets en argument (par defaut un million).
La graine fixe rend les experiences reproductibles. Le test emploie bien `==`,
sans tolerance. Sur les reels ou entiers exacts, l'addition est associative.
Sur les `int` Java, elle reste associative meme en cas de debordement, car
l'addition se fait modulo 2^32. Sur les `double`, les arrondis intermediaires
peuvent changer le resultat. Les distributions testees sont indiquees dans le
programme ; il n'existe pas de distribution uniforme sur tous les reels.
Les experiences excluent NaN et les infinis, qui demanderaient de preciser
encore la question (`NaN == NaN` est faux).

Pour le placement, on interprete « je prends 1 euro puis multiplie par n » par
`B_0 = e` et `B_n = n (B_(n-1) - 1)`. En divisant par n! puis en sommant :

```text
B_n / n! = e - somme_{k=0}^n 1/k!
B_n = somme_{j=1}^infini n!/(n+j)!
Montant apres retrait = B_50 - 1.
```

Le programme calcule la derniere serie sous forme imbriquee avec `BigDecimal`.
La troncature a 250 laisse une erreur inferieure a
`(50!/251!) * (252/251)`, donc inferieure a 10^-400 euro, hors arrondis
arithmetiques. Une seconde evaluation a 120 chiffres et une troncature a 350
controle l'accord a 10^-98 pres.

Le solde avant retrait est environ 0,01999216584 EUR ; apres le frais,
le montant algebrique est environ -0,98000783416 EUR (soit -0,98 EUR au centime).
Le placement ne permet donc aucun retrait positif apres paiement du frais.
L'enonce ne precise pas si une dette est effectivement exigible.

Une erreur initiale delta est amplifiee en `50! * delta` : utiliser `Math.E`
et appliquer directement la recurrence donne un resultat enorme et errone.
De meme, prendre litteralement 2,71828 comme mise initiale definit un autre
probleme. Ici la mise est supposee etre le nombre mathematique e exact.
Aucun arrondi contractuel annuel au centime n'est suppose.
