
import json
from copy import deepcopy
from pathlib import Path

from main import json_mode


# 원본 data.json 읽기
base_dir = Path(__file__).resolve().parent

with open(base_dir / "data.json", "r", encoding="utf-8") as file:
    original = json.load(file)


# 원본 데이터 복사
test_data = deepcopy(original)

# 오류 검증에 사용할 패턴 5개 구성
test_data["patterns"] = {
    "size_5_91": deepcopy(original["patterns"]["size_5_2"]),
    "size_5_92": deepcopy(original["patterns"]["size_5_2"]),
    "size_5_93": deepcopy(original["patterns"]["size_5_2"]),
    "size_5_94": deepcopy(original["patterns"]["size_5_2"]),
    "size_13_95": deepcopy(original["patterns"]["size_13_1"]),
}

# 테스트 1: 열 개수 오류
test_data["patterns"]["size_5_91"]["input"][0].pop()

# 테스트 2: 알 수 없는 라벨
test_data["patterns"]["size_5_92"]["expected"] = "Circle"

# 테스트 3: 숫자 형식 오류
test_data["patterns"]["size_5_93"]["input"][0][0] = "abc"

# 테스트 4: 정상 데이터 (수정하지 않음)

# 테스트 5: 13x13 X 필터 누락
del test_data["filters"]["size_13"]["x"]


# 별도 검증 파일 저장
test_file = base_dir / "data_validation.json"

with open(test_file, "w", encoding="utf-8") as file:
    json.dump(test_data, file, ensure_ascii=False, indent=2)


# 오류 검증 실행
print("=== JSON 오류 주입 테스트 ===")
json_mode(test_file)
