
import time
import json

# --------------------------------------------------
# 2단계: MAC 연산
# --------------------------------------------------
def mac(pattern, pFilter):

    n = len(pattern)
    score = 0

    for i in range(n):
        for j in range(n):
            score += pattern[i][j] * pFilter[i][j]

    return score


# --------------------------------------------------
# 3단계: 콘솔 입력 + 판정 (모드 1)
# --------------------------------------------------

EPSILON = 1e-9

# 입력 파싱 : 한 중 입력을 검증하며 파싱 후, 저장하기
def read_grid(name, n=3):

    grid = []

    for row_idx in range(n):
        while True:  # 정상적인 입력을 받을 때까지 계속
            line = input()
            tokens = line.split()

            # 검증: 토큰의 수가 n과 일치하는 지
            if len(tokens) != n:
                print("입력 형식 오류:")
                continue

            # 검증: 숫자(실수)가 아닌 문자/특수기호가 섞여 있는 지
            try:
                row = [float(t) for t in tokens] # 문자 리스트를 숫자 리스트로 바꾼다. 
            except ValueError:
                print("입력 형식 오류: 숫자만 입력하세요.")
                continue

            # grid에 row 추가
            grid.append(row)
            break

    return grid

# 판정 : A/B 점수 비교(epsilon 처리)
def judge(score_a, score_b, epsilon=EPSILON):
    """
    두 점수를 비교해 "A", "B", "판정 불가" 중 하나를 반환한다.
    차이가 epsilon보다 작으면 부동소수점 오차로 보고 "판정 불가" 처리한다.
    """

    diff = abs(score_a - score_b)

    # epsilon 검사: 부동소수점 계산 과정의 미세한 차이라면, 판정불가 
    if diff < epsilon:
        return "판정 불가"

    # A/B중 누구의 점수가 높은 지를 알려준다.
    if score_a > score_b:
        return "A"
    else:
        return "B"



def run_mode1():
    """
    모드 1: 사용자가 3x3 필터 A, B와 패턴을 입력하면
    MAC 연산으로 점수를 계산하고 판정 결과를 출력한다
    """

    print("\n#-----------------------")
    print("# [1] 필터 입력")
    print("#-----------------------")
    filter_a = read_grid("Filter A", n=3)
    filter_b = read_grid("Filter B", n=3)

    print("\n#-----------------------")
    print("# [2] 필터 입력")
    print("#-----------------------")
    pattern = read_grid("Pattern", n=3)


    print("\n#-----------------------")
    print("# [3] MAC 결과")
    print("#-----------------------")
    pattern = read_grid("Pattern", n=3)
    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)
    result = judge(score_a, score_b)

    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print(f"판정: {result}")


# --------------------------------------------------
# 4단계: JSON 로드 + 검증 + 배치 판정 (모드 2)
# --------------------------------------------------

# 라벨 정규화 매핑: 데이터에 등장하는 다양한 표기 --> 표준 라벨
LABEL_MAP = {
    "cross": "Cross",
    "+": "Cross",
    "x": "X"
}


# 다양하게 표기된 라벨을 표준 라벨('Cross' 또는 'X)로 변환한다.
def normalize_label(raw_label):
    
    key = str(raw_label).strip().lower()

    if key not in LABEL_MAP:
        raise ValueError(f"알 수 없는 라벨입니다.:{raw_label!r}")  #!r : 따옴포 표시, 이스케이프 문자 노출
    
    return LABEL_MAP[key]

# pattern_key로부터 필터 size를 추출한다.
def get_size_from_key(pattern_key):

    parts = pattern_key.split("_")
    filter_size = int(parts[1])

    return filter_size

# data에서 숫자 n에 해당하는 filter를 찾아준다.
def get_filter_set(data, n):

    key = f"size_{n}"
    filter_set = data["filters"].get(key) # get()을 사용하면, 키가 없어도 에러없이 None을 반환한다.
    return filter_set


# Cross필터 점수와 X필터 점수를 비교해 Cross/X/UNDECIDED 중 하나를 반환합니다. 
def judge_label(score_cross, score_x, epsilon=EPSILON):

    diff = abs(score_cross - score_x)

    # epsilon 검사: 부동소수점 계산 과정의 미세한 차이라면, 판정불가 
    if diff < epsilon:
        return "UNDECIDED"

    # A/B중 누구의 점수가 높은 지를 알려준다.
    if score_cross > score_x:
        return "Cross"
    else:
        return "X"

# 패턴 처리 함수
def process_case(dta, pattern_key, pattern_entry):

    # 필터 사이즈 추출 + 필터 셋트 찾기
    filter_size = get_size_from_key(pattern_key) # "size_5_1" --> 5
    filter_set = get_filter_set(data, filter_size)

    if filter_set in None:
        return {
            "key": pattern_key,
            "pass": False,
            "reason": f"크기 {n}에 해당하는 필터를 찾을 수 없음"
        }

    # 필터와 패턴 찾기
    cross_filter = filter_set["cross"]
    x_filter = filter_set["x"]
    pattern_input = pattern_entry["input"]

    # 필터와 패턴의 크기 일치 검증 (row)
    if len(cross_filter) != len(pattern_input):
        return {
            "key": pattern_key,
            "pass": False,
            "reason": f"크기 불일치(행): 필터={len(cross_filter)}, 패턴={len(pattern_input)}"
        }

    # 필터와 패턴의 크기 일치 검증 (column), 모든 row 검사
    for row in pattern_input:
        if len(row) != len(cross_filter):
            return {
                "key": pattern_key,
                "pass": False,
                "reason": "크기 불일치(열): 패턴이 정사각형이 아님"
            }

    # Cross/X 필터 각각과 MAC 연산
    score_cross = mac(pattern_input, cross_filter)
    score_x = mac(pattern_input, x_filter)
    

    # 두 점수 비교해서 판정 (Cross/X/UNDECIDED) + 라벨 정규화
    prediected = judge_label(score_cross, score_x)
    expected = normalize_label(pattern_entry(["expected"]))

    # PASS/FAIL 결정
    is_pass = (predicted == pretented)

    # 결과 딕셔너리 반환
    return {
        "key": pattern_key,
        "predicted": prediected,
        "expected": expected,
        "pass": is_pass,
        "score_cross": score_cross,
        "score_x": score_x,
    }



def run_mode2():
    """
    모드 2: data.json을 로드해서 모든 패턴 케이스를 일괄 판정하고,
    전체/PASS/FAIL 개수와 실패 케이스 목록을 출력한다.
    """

    # 화일 열어서 읽어 들이기
    with open("data.json") as f:
        data = json.load(f)

    # 읽어들인 패턴과 필터로 MAC연산하기
    results = []
    for pattern_key, pattern_entry in data["patterns"].items():
        result = process_case(data, pattern_key, pattern_entry)
        results.append(result)

    # 전체/PASS/FAIL 개수 집계 + 출력
    total = len(results)
    pass_count = sum(r["pass"] for r in results)
    fail_count = total - pass_count

    # 실패 케이스 목록 출력
    if fail_count > 0:
        print("실패 케이스")
        for r in results:
            if not r["pass"]:
                # reason 필드가 채워져 있으면, reason을 출력
                # reasons 필드가 없으면, predicted와 expected를 reason으로 출력
                reason = r.get("reason", f"predicted={r.get('predicted')}, expected={r.get('expected')}")
                print(f"  - {r['key']}: {reason}")


import time

# --------------------------------------------------
# 5단계: 성능 분석 (모드 3)
# --------------------------------------------------

def measure_mac_time(size, repeat=10):
    """
    n x n 크기의 더미 패턴/필터로 mac()을 repeat번 반복 호출해서
    평균 소요 시간(ms)를 측정한다.
    """

    # 크기가 size인 시험용 패턴과 필터 만들기
    pattern = [[1.0] * size for _ in range(size)]
    filt = [[1.0] * size for _ in range(size)]


    # mac()함수 실행 시간 측정하기
    elapsed_times = []

    for _ in range(repeat):
        start_time = time.perf_counter()
        mac(pattern, filt)
        end_time = time.perf_counter()
        elapsed_ms = (end_time - start_time) * 1000 # ms로 바꾸기
        elapsed_times.append(elapsed_ms)

    # 평규 시간 계산하기
    avg_ms = sum(elapsed_times) / len(elapsed_times)

    return avg_ms


def run_performace_analysis(filter_sizes=None, repeat=10):
    """
    지정된 크기들에 대해 measure_mac_time을 호출하고,
    "크기(NxN) / 평균 시간(ms) / 연산 횟수" 표를 출력한다.
    """

    if filter_sizes is None: sizes = [3, 5, 13, 25]

    print("\n#--------------------------------")
    print("# 성능 분석")
    print("#--------------------------------")
    print(f"{'크기 (NxN)':<12}{'평균 시간(ms)':16}{'연산 횟수(NxN)':<12}")

    for n in filter_sizes:
        avg_ms = measure_mwhmaac_time(n, repeat=repeat)
        op_count = n * n
        print(f"{n}x{n:<10}{avg_ms:<16.5f}{op_count:<12}")


# --------------------------------------------------
# 메뉴 / 진입점
# --------------------------------------------------

def show_menu():
    """ 메뉴를 출력하고, 사용자가 고른 번호(문자열)을 반환한다."""
    print("\n#-----------------------")
    print("# Mini NPU Simulator")
    print("#-----------------------")
    print("1. 모드 1 - 콘솔 입력으로 판정")
    print("2. 모드 2 - data.json 배치 판정")
    print("3. 성능 분석")
    print("0. 종료")

    choice = input("선택: ").strip()
    return choice

def main():
    """메뉴를 반복 출력하며, 선택에 따라 각 모드를 실행한다. 0을 고르면 종료"""
    while True:
        choice = show_menu()

        if choice == "1":
            run_mode1()
        elif choice == "2":
            run_mode2()
        elif choice == "3":
            run_performace_analysis()
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 0~3 중에서 선택하세요.") 


if __name__ == "__main__":
    main()

    




    
