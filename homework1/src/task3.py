"""
Task 3: Control structures
- classify_number: if/elif/else
- first_primes: while loop + helper
- sum_1_to_100: for loop accumulation
"""
from typing import List

def classify_number(n: int) -> str:
    if n > 0:
        return "positive"
    elif n < 0:
        return "negative"
    return "zero"

def first_primes(k: int = 10) -> List[int]:
    """Return the first k prime numbers."""
    def is_prime(x: int) -> bool:
        if x < 2:
            return False
        if x % 2 == 0:
            return x == 2
        i = 3
        while i * i <= x:
            if x % i == 0:
                return False
            i += 2
        return True

    out, n = [], 2
    while len(out) < k:
        if is_prime(n):
            out.append(n)
        n += 1
    return out

def sum_1_to_100() -> int:
    total = 0
    for i in range(1, 101):
        total += i
    return total
