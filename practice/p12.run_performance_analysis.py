def run_performance_analysis(sizes, pattern_dict, filters_dict):

    for n in sizes:
        avg_time = measure_mac_time(pattern_dict[n],filters_dict[n])
        print(f"크기: {n} / 평균시간(ms): {avg_time} / 연산횟수: {avg_time}") 
