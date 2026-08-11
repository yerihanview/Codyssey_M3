# --------------------------------------------------
# 콘솔 입력 + 판정 (모드 1)
# --------------------------------------------------

import mac

# 입력 파싱 : 한 줄씩 입력을 검증하며 파싱 후, 저장하기
def read_grid(name, n=3):
    '''
    사용자로부터 n줄을 입력받아 n x n 리스트로 만든다.
    형식이 틀리면 안내 메시지를 출력하고, 그 줄을 다시 입력 받는다.
    '''

    print(f"{name} ({n}줄 입력, 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요.)")
    grid = []

    for row_idx in range(n): # n개의 줄 입력을 받는다.
        while True:  # 정상적인 한 줄 입력을 받을 때까지 계속
            # 한 줄 입력
            line = input()
            tokens = line.split()

            # 검증: 토큰의 수가 n과 일치하는 지
            if len(tokens) != n:
                print("입력 형식 오류: 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요.")
                continue

            # 검증: 숫자(실수)가 아닌 문자/특수기호가 섞여 있는 지
            try:
                row = [float(t) for t in tokens] # 문자 리스트를 숫자 리스트로 바꾼다. 
            except ValueError:
                print("입력 형식 오류: 숫자만 입력하세요.")
                continue

            # 정상적인 한 줄 입력 : grid에 row 추가
            grid.append(row)
            break

    return grid

# 판정 : A/B 점수 비교 + 의미있는 차이인지 확인(epsilon 비교)
def judge(score_a, score_b, epsilon=EPSILON):
    """
    두 점수를 비교해 "A", "B", "판정 불가" 중 하나를 반환한다.
    차이가 epsilon보다 작으면 부동소수점 오차로 보고 "판정 불가" 처리한다.
    """

    diff = abs(score_a - score_b)

    # 오차 범위 검사 (epsilon): 부동소수점 계산 과정의 미세한 차이라면, 판정불가 
    if diff < epsilon:
        return "판정 불가"

    # A/B중 누가 높은 점수인지를 알려준다.
    if score_a > score_b:
        return "A"
    else:
        return "B"



def run_mode1():
    """
    사용자가 3x3 필터를 A, B패턴과 함께 입력하면
    MAC 연산으로 점수를 계산하고 판정 결과를 출력한다
    """

    print("\n#-----------------------")
    print("# [1] 필터 입력")
    print("#-----------------------")
    filter_a = read_grid("필터 A", n=3)
    filter_b = read_grid("필터 B", n=3)

    print("\n#-----------------------")
    print("# [2] 패턴 입력")
    print("#-----------------------")
    pattern = read_grid("패턴", n=3)


    print("\n#-----------------------")
    print("# [3] MAC 결과")
    print("#-----------------------")
    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)
    result = judge(score_a, score_b)

    print(f"필터 A 점수: {score_a}")
    print(f"필터 B 점수: {score_b}")
    print(f"판정: 필터 {result}")