from decimal import Decimal, getcontext
import os
import random
import sys

def test_equality(operation1, operation2):
    x = random.random()
    y = random.random()
    z = random.random()
    
    # Dynamically evaluate the operations
    result1 = eval(operation1)
    result2 = eval(operation2)

    try:
        assert result1 == result2
        return True
    except AssertionError:
        #print("AssertionError: (x+y)+z != x+(y+z)")
        return False
    
# Define possible combinations of operations and repetition counts
operations = [
    {"operation1": "(x + y) + z", "operation2": "x + (y + z)"},  # Associativity
    {"operation1": "x + y", "operation2": "y + x"},              # Commutativity
    {"operation1": "(x * y) * z", "operation2": "x * (y * z)"},  # Associativity (multiplication)
    {"operation1": "x * (y / z)", "operation2": "(x * y) / z"}   # Combination of operations
]

# Define different repetition counts
repetitions_list = [1000, 10000, 50000]

if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    filename = os.path.join(current_dir, "1.txt")
    #random.seed(42)  # Set a seed for reproducibility
    count = 0
    for op in operations:
        operation1 = op["operation1"]
        operation2 = op["operation2"]
        for rep in repetitions_list:
            count = 0
            for i in range(rep):  # Run the test multiple times
                if not test_equality(operation1, operation2):
                    count += 1
                    #print("Test failed: (x+y)+z != x+(y+z)")
            print(f"Total failed tests for {rep} iterations of {operation1} and {operation2}: {count/rep*100:.2f}%")
            with open(os.path.join(current_dir, "answer_parameterized.txt"), "w") as f:
                    f.write(f"Total failed tests for {rep} iterations of {operation1} and {operation2}: {count/rep*100:.2f}%\n")
    