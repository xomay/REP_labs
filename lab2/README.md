# Part 1 : Reproducible?

* Run the script lab2.py to get the results in lab2/answer_associativity.txt and lab2/answer_banking.txt
* No libraries need to be installed

## Expected results : 

* **Associativity** : the same error rate is expected for the same fixed seed. Generally, the error rate should be around 17%
* **Banking problem** : the value returned should be ~0.01999216


# Part 2 : Docker

Here is the guide to use the Dockerfile :

### Step 1 : navigate to the lab2 folder

Go to the folder lab2 located in REP_Labs/lab2

```bash
cd lab2
```

### Step 2 : build the docker image

```bash
docker build -t rep-lab2 .
```

### Step 3 : run the container

```bash
docker run --rm -v "$(pwd)":/out rep-lab2
```