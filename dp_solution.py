from dp_helpers import calculate_expected_value, calculate_prob_that_pick_is_red

def solve(n):
    # n is the number of balls in the bags

    # initialize T, which is a 5d array
    T = [[[[[-1, -1, -1, -1, -1] for _ in range(n+1)] for _ in range(n+1)] for _ in range(n+1)] for _ in range(n+1)]

    # We will get values from T using T[k_a][p_a][k_b][p_b] where
    # 
    # - k_a represents the number of balls removed from bag A
    # - p_a represents the number of balls removed from bag A that are red
    # - k_b represents the number of balls removed from bag B
    # - p_b represents the number of balls removed from bag B that are red

    # The innermost array of T is an array of length 5, where
    #
    # - [0] represents the maximum expected reward
    # - [1] represents the expected reward of taking bag A
    # - [2] represents the expected reward of taking bag B
    # - [3] represents the expected reward of taking from bag A
    # - [4] represents the expected reward of taking from bag B

    # Set the initial values that we know
    for i in range(n+1):
        for j in range(n+1):
            for k in range(n+1):
                if j >= k:
                    exp = calculate_expected_value(n, j, k)
                    T[n][i][j][k][0] = exp
                    T[n][i][j][k][1] = 0
                    T[n][i][j][k][2] = exp
                    T[n][i][j][k][3] = 0
                    T[n][i][j][k][4] = max(0,exp - 1)

    for i in range(n+1):
        for j in range(n+1):
            for k in range(n+1):
                if i >= j:
                    exp = calculate_expected_value(n, i, j)
                    T[i][j][n][k][0] = exp
                    T[i][j][n][k][1] = exp
                    T[i][j][n][k][2] = 0
                    T[i][j][n][k][3] = max(0, exp - 1)
                    T[i][j][n][k][4] = 0

    # Now we can set the other values
    for k_a in range(n-1, -1, -1):
        for k_b in range(n-1, -1, -1):
            for p_a in range(k_a, -1, -1):
                for p_b in range(k_b, -1, -1):
                    exp_rew_of_A = calculate_expected_value(n, k_a, p_a)
                    exp_rew_of_B = calculate_expected_value(n, k_b, p_b)
                    prob_drawing_red_from_A = calculate_prob_that_pick_is_red(n, k_a, expected_value=exp_rew_of_A)
                    prob_drawing_red_from_B = calculate_prob_that_pick_is_red(n, k_b, expected_value=exp_rew_of_B)

                    c1 = T[k_a+1][p_a+1][k_b][p_b][0]
                    c2 = T[k_a+1][p_a][k_b][p_b][0]
                    c3 = T[k_a][p_a][k_b+1][p_b+1][0]
                    c4 = T[k_a][p_a][k_b+1][p_b][0]

                    if c1 == -1 or c2 == -1 or c3 == -1 or c4 == -1:
                        raise ValueError("Value in array not been set yet.")

                    exp_rew_draw_from_A = prob_drawing_red_from_A * c1 + (1-prob_drawing_red_from_A) * c2
                    exp_rew_draw_from_B = prob_drawing_red_from_B * c3 + (1-prob_drawing_red_from_B) * c4

                    T[k_a][p_a][k_b][p_b][0] = max(exp_rew_of_A, exp_rew_of_B, exp_rew_draw_from_A, exp_rew_draw_from_B)
                    T[k_a][p_a][k_b][p_b][1] = exp_rew_of_A
                    T[k_a][p_a][k_b][p_b][2] = exp_rew_of_B
                    T[k_a][p_a][k_b][p_b][3] = exp_rew_draw_from_A
                    T[k_a][p_a][k_b][p_b][4] = exp_rew_draw_from_B

    return T

T = solve(25)

print(f"Expected number of red balls gotten: {T[0][0][0][0][0]}")
