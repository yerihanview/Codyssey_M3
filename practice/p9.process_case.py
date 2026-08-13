def process_case(case_key, case_data, filters_dict):

    n_size = get_size_from_key(case_key)
    filter_set = get_filter_set(filters_dict, n_size)
    if filter_set is None:
        return {
            "key": case_key,
            "pass": False,
            "reason": "요구하는 크기의 필터가 없습니다."
        }

    int_case_size = len(case_data["input"])
    if int_case_size != n_size:
        return {
            "key": case_key,
            "pass": False,
            "reason": f"필터의 크기{n_size}와 케이스의 크기 {int_case_size}가 다릅니다."
        }

    score_cross = mac(case_data['input'], filter_set['cross'])
    score_x = mac(case_data['input'], filter_set['x'])

    predicted = judge_label(score_cross, score_x)
    expected = normalize_label(case_data["expected"])

    is_pass = (predicted == expected)

    return {
        "key": case_key,
        "predicted": predicted,
        "expected": expected,
        "result": is_pass,
        "score_cross": score_cross,
        "score_x": score_x,
    }
    


        
