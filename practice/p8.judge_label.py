EPSILON = 1.e-9

def judge_label(score_cross, score_x):

    diff = abs(score_cross, score_x)

    if diff < EPSILON:
        return "UNDEFINED"

    if score_cross > score_x:
        return "Cross"
    else:
        return "X"