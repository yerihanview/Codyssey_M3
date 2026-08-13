# =========================================================
# 성능 분석 (모드 3)
# =========================================================

import time
from mac import mac


def measure_mac_time(n, repeat=10):
    """
    n x n 크기의 더미 패턴/필터로 mac()을 반복 호출해서
    평균 소요 시간(ms)을 측정한다.
    """

    # 테스트용 패턴과 필터를 입력된 사이즈 n에 맞추어 준비한다.
    pattern = [[1.0] * n for _ in range(n)]
    filt = [[1.0] * n for _ in range(n)]


    # mac()함수를 반복 호출한다. 시작/종료 시간을 측정한다.
    times = []
 
    for _ in range(repeat):
        start = time.perf_counter()
        mac(pattern, filt)
        end = time.perf_counter()
 
        elapsed_ms = (end - start) * 1000  # ms로 단위를 바꾼다.
        times.append(elapsed_ms)           # 측정된 시간을 기록한다.  

    # 평균 처리 시간을 구한다.
    avg_ms = sum(times) / len(times)
 
    return avg_ms
 
 
def run_performance_analysis(sizes=None, repeat=10):
    """
    지정된 크기들에 대해 measure_mac_time을 호출하고,
    "크기(N×N) / 평균 시간(ms) / 연산 횟수(N²)" 표를 출력한다.
    """
  
    if sizes is None:
        sizes = [3, 5, 13, 25]
 
    print("\n 성능 분석")
    print("--------------------------------------------")
    print(f"{'크기(N×N)':<10}{'평균 시간(ms)':<12}{'연산 횟수(N²)':<10}")
    print("--------------------------------------------")
 
    for n in sizes:
        avg_ms = measure_mac_time(n, repeat)
        op_count = n * n
        label = f"{n}×{n}"
      
        print(f"{label:<12}{avg_ms:<16.5f}{op_count:<12}")
