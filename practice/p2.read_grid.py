def read_grid(n):
    grid = []

    print(f"{n}x{n}행렬을 입력하세요. 각 행마다 {n}개의 숫자를 공백을 두고 입력하세요.")
    for i in range(n):
        while True:
            tokens = input().split()
            if len(tokens) != n:
                print(f"숫자 개수가 틀립니다. 각 열마다 {n}개의 수를 입력하세요.")
                continue

            try:
                row = [float(t) for t in tokens] 
            except (ValueError):
                print("입력 형식 오류: 숫자를 입력하세요.")
                continue
                
            grid.append(row)
            break

    return grid

