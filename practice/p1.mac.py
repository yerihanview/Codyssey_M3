def mac(pattern, pattern_filter):

    n = len(pattern)
    score = 0

    for i in range(n):
        for j in range(n):
            score += pattern[i][j] * pattern_filter[i][j]

    return score


