## Part 1 — Three programs, one list of variability factors

* **List all possible factors that can have an effect on the computed answer** (we have already done that informally on the whiteboard), starting
  from your program (lab #1, in language L1), the one an LLM generated in lab #2 (in
  language L2), and the programs of your colleagues:
  * revisit what you have done, each decision and detail that may or may not have an effect on the result
  * be inspired by what LLMs have implemented: if an LLM's solution differs from yours, it is
    certainly due to some variability...
  * be creative ;)

  A **comparison matrix** helps: one row per program, one column per factor, and in each
  cell the choice the program makes. For example, starting with the number of repetitions:

  | Program | repetitions | representation | result |
  |---|---|---|---|
  | associativity : in python (lab #1) | 10 000 | random.random() | 83% |
  | distributivity : in python (lab #3) | 10 000 | random.random() | 69% |
  | associativity : LLM, in java (lab #2) | 1 000 000 or user choice | Random | 82,85% |
  | associativity : LLM, in python | 100 000 or user choice | random.randint() | 82,88% |
  | banking : in python (lab #1) | 20 | Math.exp() | -4.3968039301820685e+48 |
  | banking : LLM, in java (lab #2) | 1 | BigDecimal and MathContext | 0,019992 |
  | banking : LLM, in python | 1 | Decimal() | 0,019992 |