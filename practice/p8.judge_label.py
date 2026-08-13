EPSILON = 1.e-9

def judge_label(score_cross, score_x):

    decision = judge(score_cross, score_x)

    if decision == "UNDECIDED":
        return decision
    elif decision == "A":
        return "Cross"
    else:
        return "X"