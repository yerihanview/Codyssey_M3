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

    
