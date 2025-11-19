import os
import csv
import tempfile
import unittest
from app import app, read_products, greedy_budget, binary_search, sort_products, PRODUCT_FILE

class AppFunctionalTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        app.config['TESTING'] = True
        app.config['UPLOAD_FOLDER'] = self.tempdir.name
        self.prodpath = os.path.join(app.config['UPLOAD_FOLDER'], 'products.csv')
        with open(self.prodpath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['apple','5.00','green apple',''])
            writer.writerow(['banana','3.00','ripe banana',''])
            writer.writerow(['carrot','2.50','purple carrot',''])

    def tearDown(self):
        self.tempdir.cleanup()

    def test_read_products(self):
        prods = read_products(self.prodpath)
        self.assertEqual(len(prods), 3)
        self.assertTrue(any(p.name == 'apple' for p in prods))

    def test_sort_products_by_price(self):
        prods = read_products(self.prodpath)
        sorted_by_price = sort_products(prods, key='price')
        prices = [p.price for p in sorted_by_price]
        self.assertEqual(prices, sorted(prices))

    def test_binary_search_exact(self):
        prods = sort_products(read_products(self.prodpath))
        idx = binary_search(prods, 'banana')
        self.assertGreaterEqual(idx, 0)
        self.assertEqual(prods[idx].name.lower(), 'banana')

    def test_greedy_budget(self):
        prods = read_products(self.prodpath)
        chosen = greedy_budget(prods, 6.0)
        total = sum(p.price for p in chosen)
        self.assertLessEqual(total, 6.0)
        self.assertTrue(len(chosen) >= 1)

    def test_index_route(self):
        client = app.test_client()
        resp = client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Bulk Upload', resp.data)

    def test_upload_route_rejects_non_csv(self):
        client = app.test_client()
        data = {'file': (tempfile.SpooledTemporaryFile(), 'file.txt')}
        resp = client.post('/upload', data=data, content_type='multipart/form-data')
        self.assertIn(b'Invalid file type', resp.data)

def test_read_products_malformed_row(self):
    path = os.path.join(app.config['UPLOAD_FOLDER'], 'bad.csv')
    with open(path, 'w', newline='', encoding='utf-8') as f:
        f.write("onlyonefield\none,two,three\n")
    prods = read_products(path)
    self.assertIsInstance(prods, list) 



if __name__ == '__main__':
    unittest.main()
