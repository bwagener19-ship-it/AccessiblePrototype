import time, csv, os
from app import read_products
os.makedirs('uploads', exist_ok=True)
path = os.path.join('uploads', 'perf_products.csv')

# generate large CSV (adjust n if slow)
n = 5000
with open(path, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    for i in range(n):
        w.writerow([f'item{i}', f'{(i%100)+0.99}', f'desc{i}', ''])

t0 = time.time()
prods = read_products(path)
t1 = time.time()
print(f"Read {len(prods)} rows in {t1-t0:.3f} seconds")

