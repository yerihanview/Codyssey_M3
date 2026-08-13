def read_grid(n):
    grid = []

    print(f"{n}x{n}행렬을 입력하세요. 각 행마다 {n}개의 숫자를 공백을 두고 입력하세요.")
    for i in range(n):
        while True:
            tokens = input().split()
            if len(tokens) != n:
                print(f"숫자 개수가 틀립니다. 각 열마다 {n}개의 수를 입력하세요.")
                continue

            row = []
            for t in tokens:
                try:
                    row.append(float(t))
                except (ValueError):
                    print(f"{t}을 입력하셨어요. 숫자를 입력하세요.")
                    break
                
            grid.append(row)

    return grid

