# =========================================================
# 성능 분석 (모드 3)
# =========================================================

from mac import mac, measure_mac_time

def make_dummy_grid(n):
    """
    성능 테스트용 n x n 더미 패턴/필터를 만든다. (값은 모두 1.0)
    """
    return [[1.0] * n for _ in range(n)]

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
        pattern = make_dummy_grid(n)
        filt - make_dummy_grid(n)
        avg_ms = measure_mac_time(pattenr, filt)
        op_count = n * n
        label = f"{n}×{n}"
      
        print(f"{label:<12}{avg_ms:<16.5f}{op_count:<12}")
