import unittest
from utils import parse_price, total_price, greedy_budget_select

class TestUtils(unittest.TestCase):
    def test_parse_price(self):
        self.assertEqual(parse_price("12.34"), 12.34)
        self.assertEqual(parse_price(5), 5.0)
        self.assertIsNone(parse_price("not-a-number"))
        self.assertIsNone(parse_price(None))

    def test_total_price(self):
        items = [{"name":"A","price":"10.5"}, {"name":"B","price":5}, {"name":"C","price":"bad"}]
        self.assertAlmostEqual(total_price(items), 15.5)

    def test_greedy_budget_select(self):
        items = [
            {"name":"cheap","price":1.0},
            {"name":"mid","price":5.0},
            {"name":"expensive","price":10.0},
        ]
        chosen = greedy_budget_select(items, 6.0)
        names = [it["name"] for it in chosen]
        self.assertIn("cheap", names)
        self.assertIn("mid", names)
        self.assertEqual(sum([float(it["price"]) for it in chosen]), 6.0)

if __name__ == "__main__":
    unittest.main()
