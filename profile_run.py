import cProfile, pstats, io
from app import read_products

def run():
    read_products('uploads/perf_products.csv')

pr = cProfile.Profile()
pr.enable()
run()
pr.disable()
s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
ps.print_stats(30)
print(s.getvalue())
