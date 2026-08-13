def run_mode1():
    n=3
    filter_A = read_grid(n)
    filter_B = read_grid(n)
    pattern = read_grid(n)

    score_a = mac(pattern, filter_A)
    score_b = mac(pattern, filter_B)

    decision = judge(score_a, score_b)

    print(f"A 점수: {score_a}, B 점수: {score_b}, 판정: {decision}")
        
