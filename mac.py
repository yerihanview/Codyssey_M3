

def mac(pattern, pattern_filter):
    """
    MAC(Multiply-Accumulate)연산.
    pattern과 pFilter는 같은 크기의 n x n 리스트이어야 한다.
    같은 위치(i, j)의 값끼리 곱한 뒤, 그 결과를 모두 더해서 하나의 점수(floqt)로 반환한다.
    """

    pattern_size = len(pattern)
    score = 0

    for row in range(pattern_size):
        for col in range(pattern_size):
            score += pattern[row][col] * pattern_filter[row][col]

    return score