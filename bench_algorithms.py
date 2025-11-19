import timeit
from app import binary_search, greedy_budget, dp_budget, sort_products, read_products

prods = sort_products(read_products('uploads/perf_products.csv'))

print("binary_search:", timeit.timeit(lambda: binary_search(prods, 'item2500'), number=1000))
print("greedy_budget:", timeit.timeit(lambda: greedy_budget(prods, 100.0), number=100))
small = prods[:30]
print("dp_budget (n=30):", timeit.timeit(lambda: dp_budget(small, 100.0), number=10))