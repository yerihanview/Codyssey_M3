EPSILON = 1e-9

def judge(score_a, score_b):

    diff = abs(score_a-score_b)
    if diff < EPSILON:
        return "UNDECIDED"

    if score_a > score_b:
        return "A"
    else:
        return "B"
        
    