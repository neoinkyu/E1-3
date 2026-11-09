import math
import time
import json
import re
from pathlib import Path



# Cross / X 패턴 자동 생성
def generate_pattern(size, shape):
    if size < 3:
        raise ValueError("배열 크기는 3 이상이어야 합니다.")

    if shape not in ("Cross", "X"):
        raise ValueError("패턴 종류는 Cross 또는 X여야 합니다.")

    matrix = []

    # 짝수 크기에서는 가운데 두 행/열을 사용
    if size % 2 == 0:
        centers = (size // 2 - 1, size // 2)
    else:
        centers = (size // 2,)

    for i in range(size):
        row = []

        for j in range(size):
            if shape == "Cross":
                value = 1 if i in centers or j in centers else 0

            else:
                value = 1 if i == j or i + j == size - 1 else 0

            row.append(value)

        matrix.append(row)

    return matrix



# 2차원 배열을 1차원 배열로 변환
def flatten_matrix(matrix):
    flat = []

    for row in matrix:
        for value in row:
            flat.append(value)

    return flat


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



# 1차원 배열 기반 MAC 연산
def mac_flat(pattern_flat, filter_flat):
    score = 0

    for i in range(len(pattern_flat)):
        score += pattern_flat[i] * filter_flat[i]

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




# 공통 MAC 연산 성능 측정
def benchmark_mac(pattern, filter_matrix, mac_function=mac):
    measurements = 10
    repeats = 100
    times = []

    # 예비 실행
    for _ in range(10):
        mac_function(pattern, filter_matrix)

    # 10개 구간에서 각각 100회 측정
    for _ in range(measurements):
        start = time.perf_counter_ns()

        for _ in range(repeats):
            mac_function(pattern, filter_matrix)

        end = time.perf_counter_ns()

        average_ms = (end - start) / repeats / 1_000_000
        times.append(average_ms)

    return sum(times) / len(times)



# 배열 크기별 성능 분석
def performance_analysis():
    print("\n=== [3] 성능 분석 ===")
    print("측정 기준: 10개 구간 × 구간당 100회 연산 (총 1,000회)")
    print("측정값: MAC 연산 1회당 평균 실행 시간")
    print(f"{'크기':<12}{'평균 시간(ms)':<14}{'연산 횟수':>8}")
    print("-" * 40)

    for size in (3, 5, 13, 25):
        pattern = generate_pattern(size, "Cross")
        filter_matrix = generate_pattern(size, "Cross")

        average_ms = benchmark_mac(pattern, filter_matrix)
        operations = size * size

        print(
            f"{size}x{size:<9}"
            f"{average_ms:<18.6f}"
            f"{operations:>10}"
        )



# 사용자 입력 모드
def user_mode():
    print("\n=== [1] 필터 입력 ===")

    filter_a = input_matrix("필터 A")
    filter_b = input_matrix("필터 B")

    print("\n=== 저장된 필터 확인 ===")
    print("필터 A:", filter_a)
    print("필터 B:", filter_b)

    print("\n=== [2] 패턴 입력 ===")

    while True:
        print("1. 직접 입력")
        print("2. 자동 생성")
        method = input("선택: ").strip()

        if method == "1":
            pattern = input_matrix("입력 패턴")
            break

        elif method == "2":
            shape = input("패턴 선택 (1: Cross, 2: X): ").strip()

            if shape == "1":
                pattern = generate_pattern(3, "Cross")
                break

            elif shape == "2":
                pattern = generate_pattern(3, "X")
                break

            print("입력 오류: 1 또는 2를 선택하세요.")

        else:
            print("입력 오류: 1 또는 2를 선택하세요.")

    print("\n입력 패턴:")
    for row in pattern:
        print(*row)

    print("\n=== [3] MAC 연산 결과 ===")

    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)

    result = classify(score_a, score_b)

    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print(f"판정: {result}")

    # 필터별 MAC 연산 시간 측정
    time_a = benchmark_mac(pattern, filter_a)
    time_b = benchmark_mac(pattern, filter_b)

    average_ms = (time_a + time_b) / 2

    print(f"연산 시간(필터당 평균): {average_ms:.6f} ms")



# 라벨 정규화
def normalize_label(label):
    if not isinstance(label, str):
        return None

    labels = {
        "+": "Cross",
        "cross": "Cross",
        "x": "X"
    }

    return labels.get(label.strip().lower())


# N x N 배열 구조 검증
def validate_matrix(matrix, size):
    if not isinstance(matrix, list) or len(matrix) != size:
        raise ValueError(f"행 수 오류: {size}행이 필요합니다.")

    for i, row in enumerate(matrix, start=1):
        if not isinstance(row, list) or len(row) != size:
            raise ValueError(f"{i}행의 열 수 오류: {size}열이 필요합니다.")

        for value in row:
            if type(value) not in (int, float) or not math.isfinite(value):
                raise ValueError(f"{i}행에 잘못된 숫자가 있습니다.")


# JSON 필터 로드 및 검증
def load_filters(filters_data):
    valid_filters = {}

    print("\n=== [1] 필터 로드 ===")

    for size in (5, 13, 25):
        key = f"size_{size}"

        try:
            group = filters_data.get(key)

            if not isinstance(group, dict):
                raise ValueError("필터 데이터가 없거나 형식이 잘못되었습니다.")

            normalized = {}

            for raw_label, matrix in group.items():
                label = normalize_label(raw_label)

                if label not in ("Cross", "X"):
                    raise ValueError(f"알 수 없는 필터 라벨: {raw_label}")

                if label in normalized:
                    raise ValueError(f"중복 필터 라벨: {label}")

                validate_matrix(matrix, size)
                normalized[label] = matrix

            if set(normalized) != {"Cross", "X"}:
                raise ValueError("Cross 또는 X 필터가 누락되었습니다.")

            valid_filters[size] = normalized
            print(f"size_{size}: 필터 로드 성공 (Cross, X)")

        except ValueError as error:
            print(f"size_{size}: 필터 로드 실패 - {error}")

    return valid_filters


# JSON 분석 모드
def json_mode(file_path=None):
    print("\n=== data.json 분석 모드 ===")

    if file_path is None:
        file_path = Path(__file__).with_name("data.json")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

    except (OSError, json.JSONDecodeError) as error:
        print(f"JSON 파일 읽기 오류: {error}")
        return

    if not isinstance(data, dict):
        print("JSON 구조 오류: 최상위 데이터는 객체여야 합니다.")
        return

    filters_data = data.get("filters")
    patterns_data = data.get("patterns")

    if not isinstance(filters_data, dict):
        print("JSON 구조 오류: filters 객체가 없습니다.")
        return

    if not isinstance(patterns_data, dict):
        print("JSON 구조 오류: patterns 객체가 없습니다.")
        return

    valid_filters = load_filters(filters_data)

    print("\n=== [2] 패턴 분석 ===")

    pass_count = 0
    fail_cases = []

    for case_id, case in patterns_data.items():
        print(f"\n--- {case_id} ---")

        try:
            # 패턴 키에서 크기 추출
            match = re.fullmatch(r"size_(\d+)_(\d+)", case_id)

            if match is None:
                raise ValueError("패턴 키 형식 오류")

            size = int(match.group(1))

            if size not in valid_filters:
                raise ValueError(f"size_{size} 필터가 없거나 유효하지 않습니다.")

            if not isinstance(case, dict):
                raise ValueError("패턴 데이터 형식 오류")

            pattern = case.get("input")
            expected = normalize_label(case.get("expected"))

            # 입력 배열 검증
            validate_matrix(pattern, size)

            if expected not in ("Cross", "X"):
                raise ValueError("expected 라벨 오류")

            # MAC 점수 계산
            filter_cross = valid_filters[size]["Cross"]
            filter_x = valid_filters[size]["X"]

            score_cross = mac(pattern, filter_cross)
            score_x = mac(pattern, filter_x)

            # 기존 classify 함수 재사용
            result = classify(score_cross, score_x)

            if result == "A":
                prediction = "Cross"
            elif result == "B":
                prediction = "X"
            else:
                prediction = "UNDECIDED"

            print(f"Cross 점수: {score_cross:.15g}")
            print(f"X 점수: {score_x:.15g}")

            if prediction == expected:
                pass_count += 1
                print(f"판정: {prediction} | expected: {expected} | PASS")

            else:
                if prediction == "UNDECIDED":
                    reason = "epsilon 기준 동점으로 판정"
                else:
                    reason = f"판정({prediction})과 expected({expected}) 불일치"

                fail_cases.append((case_id, reason))
                print(f"판정: {prediction} | expected: {expected} | FAIL")
                print(f"실패 사유: {reason}")

        except (ValueError, TypeError) as error:
            reason = f"데이터 검증 오류: {error}"
            fail_cases.append((case_id, reason))
            print(f"FAIL - {reason}")

    # 크기별 성능 분석
    performance_analysis()

    # 최종 결과 요약
    print("\n=== [4] 결과 요약 ===")

    total = len(patterns_data)
    fail_count = len(fail_cases)

    print(f"총 테스트: {total}개")
    print(f"통과: {pass_count}개")
    print(f"실패: {fail_count}개")

    if fail_cases:
        print("\n실패 케이스:")
        for case_id, reason in fail_cases:
            print(f"- {case_id}: {reason}")


# 패턴 생성기 모드
def pattern_generator_mode():
    print("\n=== 패턴 자동 생성기 ===")

    while True:
        try:
            size = int(input("배열 크기 N 입력 (3 이상): "))

            if size < 3:
                print("입력 오류: 3 이상의 정수를 입력하세요.")
                continue

            break

        except ValueError:
            print("입력 오류: 정수를 입력하세요.")

    for shape in ("Cross", "X"):
        matrix = generate_pattern(size, shape)

        print(f"\n[{shape} 패턴: {size}x{size}]")

        for row in matrix:
            print(" ".join(str(value) for value in row))

    print("\n패턴 생성 완료")



# 2차원 / 1차원 MAC 성능 비교
def optimization_mode():
    print("\n=== 1차원 배열 최적화 성능 비교 ===")
    print("측정 기준: 10개 구간 x 구간당 100회 (총 1,000회)")
    print("배열 변환 시간은 측정에서 제외")
    print("개선율: 양수는 1차원 방식이 빠름, 음수는 느림")

    print()
    print(
        f"{'크기':<6}"
        f"{'2차원(ms)':>13}"
        f"{'1차원(ms)':>11}"
        f"{'개선율(%)':>11}"
        f"{'검증':>5}"
    )
    print("-" * 60)

    for size in (3, 5, 13, 25):
        # 동일한 입력 데이터 생성
        pattern = generate_pattern(size, "Cross")
        filter_matrix = generate_pattern(size, "Cross")

        # 1차원 배열로 변환 (시간 측정 전)
        flat_pattern = flatten_matrix(pattern)
        flat_filter = flatten_matrix(filter_matrix)

        # 2차원과 1차원 MAC 결과 비교
        score_2d = mac(pattern, filter_matrix)
        score_1d = mac_flat(flat_pattern, flat_filter)

        is_correct = abs(score_2d - score_1d) < 1e-9

        # 두 방식에 동일한 반복 횟수 적용
        time_2d = benchmark_mac(pattern, filter_matrix)
        time_1d = benchmark_mac(
            flat_pattern, flat_filter, mac_flat
        )

        # 개선율 계산
        improvement = (time_2d - time_1d) / time_2d * 100

        status = "PASS" if is_correct else "FAIL"
        size_label = f"{size}x{size}"

        print(
            f"{size_label:<9}"
            f"{time_2d:>13.6f}"
            f"{time_1d:>13.6f}"
            f"{improvement:>+12.2f}%"
            f"{status:>9}"
        )

    print("\n=== X 패턴 계산 결과 추가 검증 ===")

    for size in (3, 5, 13, 25):
        pattern = generate_pattern(size, "X")
        flat_pattern = flatten_matrix(pattern)

        score_2d = mac(pattern, pattern)
        score_1d = mac_flat(flat_pattern, flat_pattern)

        result = (
            "PASS"
            if abs(score_2d - score_1d) < 1e-9
            else "FAIL"
        )

        print(f"{size}x{size}: {result}")




def main():
    print("=== Mini NPU Simulator ===")

    while True:
        print("\n[모드 선택]")
        print("1. 사용자 입력 (3x3)")
        print("2. data.json 분석")
        print("3. 패턴 자동 생성기")
        print("4. 1차원 배열 최적화 비교")

        choice = input("선택: ").strip()

        if choice == "1":
            user_mode()
            break

        elif choice == "2":
            json_mode()
            break

        elif choice == "3":
            pattern_generator_mode()
            break

        elif choice == "4":
            optimization_mode()
            break

        else:
            print("입력 오류: 1~4 중 선택하세요.")


if __name__ == "__main__":
    main()



