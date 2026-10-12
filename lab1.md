# Answers : Lab session #1 — How often (x+y)+z == x+(y+z)?

* **Question 1 : Is (x+y)+z == x+(y+z)?**: first part, compute how many times it is not equal.
* **Question 2 : Banking problem**: try investment rules with the euler number.

## Choices and results

* **Question 1 :** Used the random python library to generate 3 random floats between 0.0 and 1.0. Assertion is then made to check the equality and see the results. Tests show that around 15 to 20% of assertions are false, depending on the floats generated. To reproduce the same error rate, we can set the seed for the random generation.
* **Question 2 :** Used the math.e constant to represent the euler number. Tried 20 times for a 50 years investment. No errors seen.