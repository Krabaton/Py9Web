import unittest

from src.example.ops import add, sub, mul, div


class TestExamples(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Start before all test')

    @classmethod
    def tearDownClass(cls):
        print('Start after all test')

    def setUp(self):
        print('Start before each test')

    def tearDown(self):
        print('Start after each test')

    def test_add(self):
        print("Add function test")
        self.assertEqual(add(2, 3), 5)

    def test_sub(self):
        print("Sub function test")
        self.assertEqual(sub(2, 3), -1)

    def test_mul(self):
        print("Mul function test")
        self.assertEqual(mul(2, 3), 6)

    def test_div(self):
        print("Div function test")
        self.assertAlmostEqual(div(2, 3), 0.66666666)
        with self.assertRaises(ZeroDivisionError) as cm:
            div(3, 0)


if __name__ == '__main__':
    unittest.main()
