
import math
import time


# MAC 연산
def mac(pattern, filter_matrix, show_steps=False):
    score = 0

    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            product = pattern[i][j] * filter_matrix[i][j]
            score += product

            if show_steps:
                print(
                    f"({i+1},{j+1}) "
                    f"{pattern[i][j]} x {filter_matrix[i][j]} "
                    f"= {product} → 누적 점수: {score}"
                )

    return score


# 3x3 배열 입력
def input_matrix(name):
    matrix = []

    print(f"\n{name} (3줄 입력, 공백 구분)")

    while len(matrix) < 3:
        row_number = len(matrix) + 1
        user_input = input(f"{row_number}행: ")

        try:
            row = [float(x) for x in user_input.split()]

            if len(row) != 3:
                print("입력 오류: 숫자 3개를 입력하세요.")
                continue

            if not all(math.isfinite(x) for x in row):
                print("입력 오류: 유한한 숫자만 입력하세요.")
                continue

            matrix.append(row)

        except ValueError:
            print("입력 오류: 숫자만 입력하세요.")

    return matrix


# 점수 비교 및 판정
def classify(score_a, score_b):
    epsilon = 1e-9

    if abs(score_a - score_b) < epsilon:
        return "UNDECIDED"
    elif score_a > score_b:
        return "A"
    else:
        return "B"


# 사용자 입력 모드
def user_mode():
    print("\n=== [1] 필터 입력 ===")

    filter_a = input_matrix("필터 A")
    filter_b = input_matrix("필터 B")

    print("\n=== 저장된 필터 확인 ===")
    print("필터 A:", filter_a)
    print("필터 B:", filter_b)

    print("\n=== [2] 패턴 입력 ===")
    pattern = input_matrix("입력 패턴")

    print("\n=== [3] MAC 연산 결과 ===")

    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)

    result = classify(score_a, score_b)

    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print(f"판정: {result}")

    # MAC 연산 10회 반복 측정
    repeat = 10

    start = time.perf_counter()

    for _ in range(repeat):
        mac(pattern, filter_a)
        mac(pattern, filter_b)

    end = time.perf_counter()

    average_ms = (end - start) * 1000 / repeat

    print(f"연산 시간(평균/{repeat}회): {average_ms:.6f} ms")


def main():
    print("=== Mini NPU Simulator ===")
    user_mode()


if __name__ == "__main__":
    main()
