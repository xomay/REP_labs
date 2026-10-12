import math
import random

def test_equality():
    x = random.random()
    y = random.random()
    z = random.random()
    try:
        assert (x+y) + z == x + (y+z)
        return True
    except AssertionError:
        print("AssertionError: (x+y)+z != x+(y+z)")
        return False
    
def banking_problem(n : int):
    deposit = math.e
    for i in range(1, n+1):
        deposit = (deposit-1) * i
        #print(f"Year {i}: Deposit after interest: {deposit:.2f}")
    return deposit-1 # 1 euro fee
    

if __name__ == "__main__":
    #random.seed(42)  # Set a seed for reproducibility
    count = 0
    for i in range(100):  # Run the test multiple times
        if not test_equality():
            count += 1
            print("Test failed: (x+y)+z != x+(y+z)")
    print(f"Total failed tests: {count}%")
    
    print(f"Banking problem result for 50 years: ")
    res = [banking_problem(50)]
    banking_count = 0
    for i in range(20):
        res.append(banking_problem(50))
        if res[i] != res[i+1]:
            banking_count += 1
    print(f"Total changes in banking problem result over 50 years for 20 trials: {banking_count}")
    print(f"All results: {res}")
        
    