def run_mode2(data):

    results = []

    for case_key, case_data in data["patterns"].items():
        r = process_case(case_key, case_data, data)
        results.append(r)

    count_total = 0
    count_pass = 0
    count_fail = 0
    for r in results:
        print(f"key: {r['key']}, score_cross: {r['score_cross']}, score_x: {r['score_x']}, predicted: {r['predicted']}", {r['pass']})
        total += 1
        if r['pass']:
            count_pass += 1

    count_fail = count_toal - count_pass

    for r in results:
        if not r['pass']:
            print(f"key: {r['key']}, reason: {r['reason']}")