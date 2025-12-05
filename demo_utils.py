from utils import greedy_budget_select, total_price

items = [
    {"name":"Ball", "price": 45.0},
    {"name":"Rope Toy", "price": 25.0},
    {"name":"Treat", "price": 10.0},
]

budget = 60.0
chosen = greedy_budget_select(items, budget)
print("Budget:", budget)
print("Chosen items:", [c["name"] for c in chosen])
print("Total chosen price:", total_price(chosen))
