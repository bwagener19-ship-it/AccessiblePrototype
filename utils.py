"""Small utility functions for AccessiblePrototype.

Contains:
- parse_price: safely parse a price string to float.
- total_price: sum product prices (list of dicts or objects).
- greedy_budget_select: greedy selection to fit under a budget.
"""

from typing import List, Dict, Any, Optional

def parse_price(s: Any) -> Optional[float]:
    """Try to convert input to float. Return None if invalid."""
    try:
        if s is None:
            return None
        return float(s)
    except (ValueError, TypeError):
        return None


def total_price(items: List[Dict[str, Any]]) -> float:
    """Return sum of item['price'] for items with valid numeric price."""
    total = 0.0
    for it in items:
        p = parse_price(it.get("price") if isinstance(it, dict) else getattr(it, "price", None))
        if p is not None:
            total += p
    return total


def greedy_budget_select(items: List[Dict[str, Any]], budget: float) -> List[Dict[str, Any]]:
    """Return a list of items chosen greedily (cheapest first) without exceeding budget."""
    if budget <= 0:
        return []

    priced = []
    for it in items:
        p = parse_price(it.get("price") if isinstance(it, dict) else getattr(it, "price", None))
        if p is not None and p >= 0:
            priced.append((p, it))

    priced.sort(key=lambda x: x[0]) 

    chosen = []
    total = 0.0
    for p, it in priced:
        if total + p <= budget:
            chosen.append(it)
            total += p

    return chosen

