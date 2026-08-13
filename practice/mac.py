def mac(pattern, filter):

    n = len(pattern)
    score = 0

    for i in range(n):
        for j in range(n):
            score += pattern[i][j] * filter[i][j]

    return score


