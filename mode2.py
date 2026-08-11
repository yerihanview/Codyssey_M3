# --------------------------------------------------
# JSON 로드 + 검증 + 배치 판정 (모드 2)
# --------------------------------------------------

from mac import mac
import json

# 라벨 정규화 매핑: 데이터에 등장하는 다양한 표기 --> 표준 라벨
LABEL_MAP = {
    "cross": "Cross",
    "+": "Cross",
    "x": "X"
}


def normalize_label(raw_label):
    '''
    다양하게 표기된 라벨을 표준 라벨('Cross' 또는 'X)로 변환한다.
    '''

    # 입력받은 문자열의 좌우 공백을 제거 + 소문자로 변환
    key = str(raw_label).strip().lower()

    # 라벨 정규화 매핑 테이블에 포함되는 지 확인
    if key not in LABEL_MAP:
        raise ValueError(f"알 수 없는 라벨입니다.:{raw_label!r}")  #!r : 따옴포 표시, 이스케이프 문자 노출

    # 매핑된 표준 라벨 반환
    return LABEL_MAP[key]


def get_size_from_key(pattern_key):
    """
    pattern_key로부터 필터 size(N)를 추출한다.
    pattern_key 형식 : "size_{N}_{idx}"
    pattern_key 예시 : "size_5_1", "size_13_2"
    """

    # "_"를 delimiter로 문자열 분할하려 리스트 parts에 담는다. 2번째 값을 정수로 변환 
    parts = pattern_key.split("_")
    filter_size = int(parts[1])

    # 필터 size를 반환한다.
    return filter_size


def get_filter_set(data, filter_size):
    """
    data = data.json을 읽어들인 값
    "filters"에 "size_5", "size_13"등의 필터가 포함되어 있다.
    data에서 필터 사이즈가 일치하는 filter를 찾는다.
    """

    key = f"size_{filter_size}"
    filter_set = data["filters"].get(key) # get()을 사용하면, 키가 없어도 에러없이 None을 반환한다.
    return filter_set


EPSILON = 1e-9

def judge_label(score_cross, score_x, epsilon=EPSILON):
    '''
    Cross필터 점수와 X필터 점수를 비교해 Cross/X/UNDECIDED 중 하나를 반환합니다. 
    '''

    # 두 값의 차이
    diff = abs(score_cross - score_x)

    # epsilon 검사: 부동소수점 계산 과정의 미세한 차이라면, 판정불가 
    if diff < epsilon:
        return "UNDECIDED"

    # A/B중 누구의 점수가 높은 지를 알려준다.
    if score_cross > score_x:
        return "Cross"
    else:
        return "X"


def process_case(data, pattern_key, pattern_entry):
    """
    pattern 하나를 입력 받아서, 2가지 filter로 매핑한다.
    필터 매핑 --> 크기 검증 --> MAC 연산 --> 판정 --> expected 비교(PASS/FAIL)까지 처리한다.
    필터가 없거나 크기가 안 맞으면 pass=False와 실패 사유(reason)을 담아 반환한다.
    """

    # 필터 사이즈 추출("size_5_1" -> 5) + 필터 셋트 찾기
    filter_size = get_size_from_key(pattern_key) 
    filter_set = get_filter_set(data, filter_size)

    if filter_set is None: 
        return {
            "key": pattern_key,
            "pass": False,
            "reason": f"크기 {filter_size}에 해당하는 필터를 찾을 수 없음"
        }

    # Cross/X 필터 준비
    cross_filter = filter_set["cross"]
    x_filter = filter_set["x"]

    # 패턴 준비
    pattern_data = pattern_entry["input"]

    # 필터와 패턴의 크기 일치 검증 (row)
    if len(cross_filter) != len(pattern_data):
        return {
            "key": pattern_key,
            "pass": False,
            "reason": f"크기 불일치(행): 필터={len(cross_filter)}, 패턴={len(pattern_data)}"
        }

    # 필터와 패턴의 크기 일치 검증 (column), 모든 row 검사
    for row in pattern_data:
        if len(row) != len(cross_filter):  # column 개수 비교
            return {
                "key": pattern_key,
                "pass": False,
                "reason": "크기 불일치(열): 패턴이 정사각형이 아님"
            }

    # Cross/X 필터 각각과 MAC 연산
    score_cross = mac(pattern_data, cross_filter)
    score_x = mac(pattern_data, x_filter)
    

    # 두 점수 비교해서 판정 (Cross/X/UNDECIDED)
    predicted = judge_label(score_cross, score_x)

    # expected 값의 정규화
    expected = normalize_label(pattern_entry(["expected"]))

    # PASS/FAIL 결정
    is_pass = (predicted == expected)

    # 결과 딕셔너리 반환
    return {
        "key": pattern_key,
        "predicted": predicted,
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
    for pattern_key, pattern_entry in data["patterns"].items(): # items()는 딕셔너리에 저장된 모든 Key와 Value 쌍을 튜플(Tuple) 형태로 한번에 묶어서 반환
        result = process_case(data, pattern_key, pattern_entry) # 하나의 패턴에 대해 2개 필터를 매핑한 결과를 딕셔너리로 반환
        results.append(result)  # 딕셔너리를 리스트에 저장

    # 전체/PASS/FAIL 개수 집계
    total = len(results)
    pass_count = sum(r["pass"] for r in results)
    fail_count = total - pass_count

    # 실패 케이스 목록 출력
    if fail_count > 0:
        print("실패 케이스")
        for r in results:
            if not r["pass"]: # pass == False
                # reason 필드가 채워져 있으면, reason을 출력
                # reasons 필드가 없으면, predicted와 expected의 값을 reason으로 출력
                # dictionary의 get(key, default) 메써드를 사용하여, key로 찾을 수 없을 때, default 반환값
                ## reason = r.get("reason", f"predicted={r.get('predicted')}, expected={r.get('expected')}")
                ## print(f"  - {r['key']}: {reason}")

                # 쉽게 작성한 코드
                reason = r.get("reason")
                if reason is None:
                    output = f"predicted={r.get('predicted')}, expected={r.get('expected')}"
                else:
                    output = reason
                    
                print(f"  - {r['key']}: {output}")


