def process_case(case_key, case_data, filters_dict):

    n_size = get_size_from_key(case_key)
    filter_set = get_filter_set(filters_dict, n_size)
    if filter_set is None:
        return {
            "key": {case_key},
            "pass": False,
            "reason": "요구하는 크기의 필터가 없습니다."
        }

    int_case_size = len(case_data["input"])
    if int_case_size != n_size:
        return {
            "key": {case_key},
            "pass": False,
            "reason": "필터의 크기{n_size}와 케이스의 크기 {int_case_size}가 다릅니다."
        }

    score_cross = mac(case_data, filter_set['cross'])
    score_x = mac(case_data, filter_set['x'])

    decision = judge(score_cross, score_x)
    if decision != "UNDECIDED":
        if decision == "A"
            decision = "Cross"
        else:
            decision = "X"

    


        
