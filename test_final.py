
import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from main import (
    mac,
    mac_flat,
    flatten_matrix,
    generate_pattern,
    classify,
    normalize_label,
    validate_matrix,
    json_mode,
)


class TestMiniNPU(unittest.TestCase):

    def test_basic_mac(self):
        cross = generate_pattern(3, "Cross")
        x = generate_pattern(3, "X")
        self.assertEqual(mac(cross, cross), 5)
        self.assertEqual(mac(cross, x), 1)

    def test_label_normalization(self):
        self.assertEqual(normalize_label("+"), "Cross")
        self.assertEqual(normalize_label("cross"), "Cross")
        self.assertEqual(normalize_label("x"), "X")

    def test_epsilon(self):
        self.assertEqual(
            classify(0.9, 0.8999999999999999),
            "UNDECIDED"
        )
        self.assertEqual(classify(5, 1), "A")
        self.assertEqual(classify(1, 5), "B")

    def test_pattern_generation(self):
        for size in (3, 5, 13, 25):
            for shape in ("Cross", "X"):
                matrix = generate_pattern(size, shape)
                validate_matrix(matrix, size)

    def test_matrix_validation(self):
        with self.assertRaises(ValueError):
            validate_matrix([[1, 0], [0, 1]], 3)

        with self.assertRaises(ValueError):
            validate_matrix(
                [[1, 0, 1], [0, "abc", 1], [1, 0, 1]],
                3
            )

    def test_flat_mac_consistency(self):
        for size in (3, 5, 13, 25):
            for shape in ("Cross", "X"):
                matrix = generate_pattern(size, shape)
                flat = flatten_matrix(matrix)

                self.assertAlmostEqual(
                    mac(matrix, matrix),
                    mac_flat(flat, flat)
                )

    def test_json_original(self):
        output = io.StringIO()

        with redirect_stdout(output):
            json_mode()

        text = output.getvalue()

        self.assertIn("총 테스트: 6개", text)
        self.assertIn("통과: 3개", text)
        self.assertIn("실패: 3개", text)

    def test_json_validation(self):
        test_file = Path(__file__).with_name(
            "data_validation.json"
        )
        output = io.StringIO()

        with redirect_stdout(output):
            json_mode(test_file)

        text = output.getvalue()

        self.assertIn("총 테스트: 5개", text)
        self.assertIn("통과: 1개", text)
        self.assertIn("실패: 4개", text)


if __name__ == "__main__":
    unittest.main()
