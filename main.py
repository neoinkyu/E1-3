

def mac(pattern, filter_matrix, show_steps=False):
    score = 0

    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            # 같은 위치의 값끼리 곱하기
            product = pattern[i][j] * filter_matrix[i][j]

            # 기존 점수에 곱셈 결과 누적
            score += product

            # 상세 계산 과정 출력
            if show_steps:
                print(
                    f"({i+1},{j+1}) "
                    f"{pattern[i][j]} x {filter_matrix[i][j]} "
                    f"= {product} → 누적 점수: {score}"
                )

    return score


# 십자가 패턴
cross = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
]

# X 패턴
x_filter = [
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1]
]

print("십자가 필터 점수:", mac(cross, cross))
print("X 필터 점수:", mac(cross, x_filter))

print("\n=== MAC 상세 계산 과정 ===")
mac(cross, cross, show_steps=True)