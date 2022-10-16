from math import comb

def calculate_expected_value(n, k, p):
    # n - total number of balls in bag at beginning
    # k - balls removed from bag
    # p - balls removed from bag that are red
    s = 0
    for i in range(n+1):
        if i+p > n:
            continue

        num = comb(i+p, p) * comb(n-(i+p), k-p)
        den = 0
        for j in range(n+1):
            den += comb(j, p) * comb(n-j, k - p)
        
        s += i * num / den

    return s

def calculate_prob_that_pick_is_red(n, k, p = None, expected_value = None):
    # n - total number of balls in bag at beginning
    # k - balls removed from bag
    # p - balls removed from bag that are red

    if expected_value is not None:
        return expected_value / (n-k)

    n_of_reds = calculate_expected_value(n, k, p)

    return n_of_reds / (n-k)
