from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import csv
import os
import time
from data_structures import dijkstra_shortest_path, greedy_assemble_fragments, max_overlap_kmp
from markupsafe import escape
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from models import Product
from data_structures import (
    Stack, Queue, HashTable, PriorityQueue, BinarySearchTree,
    Graph, kmp_search, product_name_list
)

load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

PRODUCT_FILE = os.path.join(app.config['UPLOAD_FOLDER'], 'products.csv')
ALLOWED_EXTENSIONS = {'csv'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def read_products(filepath=None):
    """Return list of Product objects read from CSV (if exists)."""
    if filepath is None:
        filepath = PRODUCT_FILE
    products = []
    if os.path.exists(filepath):
        with open(filepath, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 4:
                    name, price, desc, img = row
                    try:
                        price = float(price)
                    except ValueError:
                        # leave as-is if not parsable
                        pass
                    products.append(Product(name, price, desc, img))
    return products


def write_product(product: Product):
    with open(PRODUCT_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([product.name, product.price, product.description, product.image_url])


def sort_products(products, key="name"):
    if key == "price":
        return sorted(products, key=lambda p: float(p.price))
    return sorted(products, key=lambda p: p.name.lower())


def binary_search(products, target):
    low, high = 0, len(products) - 1
    target = target.lower()

    while low <= high:
        mid = (low + high) // 2
        name = products[mid].name.lower()
        if name == target:
            return mid
        elif name < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def greedy_budget(products, budget):
    products_sorted = sorted(products, key=lambda p: float(p.price))
    chosen = []
    total = 0.0
    for p in products_sorted:
        try:
            price = float(p.price)
        except Exception:
            continue
        if total + price <= budget:
            chosen.append(p)
            total += price
    return chosen


def dp_budget(products, budget):
    n = len(products)
    B = int(budget)
    dp = [[0] * (B + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        price = int(float(products[i - 1].price))
        val = float(products[i - 1].price)
        for b in range(1, B + 1):
            if price <= b:
                dp[i][b] = max(val + dp[i - 1][b - price], dp[i - 1][b])
            else:
                dp[i][b] = dp[i - 1][b]
    chosen = []
    b = B
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            chosen.append(products[i - 1])
            b -= int(float(products[i - 1].price))
    return chosen[::-1]


# ----- ROUTES ----- #

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = escape(request.form.get('name', '')).strip()
        price_raw = request.form.get('price', '').strip()
        description = escape(request.form.get('description', '')).strip()
        image_url = escape(request.form.get('image_url', '')).strip()
        try:
            price = float(price_raw)
        except ValueError:
            return render_template('add_product.html', error="Enter a valid numeric price", form=request.form), 400
        p = Product(name, price, description, image_url)
        write_product(p)
        return redirect(url_for('view_products'))
    return render_template('add_product.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_csv():
    message = None
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            message = "No file selected."
        elif not allowed_file(file.filename):
            message = "Invalid file type. Please upload a .csv file."
        else:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            message = f"Uploaded {filename} successfully."
    return render_template('upload.html', message=message)


@app.route('/view')
def view_products():
    sort = request.args.get('sort', 'name')
    products = read_products()
    products = sort_products(products, key=sort)
    return render_template('view_products.html', products=products, sort=sort)


@app.route('/search', methods=['GET', 'POST'])
def search_products():
    query = request.args.get('q', '').strip()
    products = sort_products(read_products())
    if request.method == 'POST' or query:
        idx = binary_search(products, query) if query else -1
        if idx != -1:
            results = [products[idx]]
        else:
            results = [p for p in products if query.lower() in p.name.lower() or query.lower() in p.description.lower()]
        return render_template('search.html', products=results, query=query)
    return render_template('search.html', products=[], query='')


@app.route('/budget-picker', methods=['GET'])
def budget_picker():
    amount = request.args.get('amount', '').strip()
    try:
        budget = float(amount)
    except Exception:
        return render_template('budget.html', products=[], total=0.0, budget=0.0)
    products = read_products()
    chosen = greedy_budget(products, budget)
    return render_template('budget.html', products=chosen, total=sum(float(p.price) for p in chosen), budget=budget)


@app.route('/dp-budget', methods=['GET'])
def dp_budget_picker():
    amount = request.args.get('amount', '').strip()
    try:
        budget = float(amount)
    except Exception:
        return render_template('budget.html', products=[], total=0.0, budget=0.0)
    products = read_products()
    chosen = dp_budget(products, budget)
    return render_template('budget.html', products=chosen, total=sum(float(p.price) for p in chosen), budget=budget)


@app.route('/accessibility')
def accessibility_statement():
    return render_template('accessibility_statement.html')


@app.route('/ds/stack')
def ds_stack_demo():
    s = Stack()
    s.push('first'); s.push('second'); s.push('third')
    popped = s.pop()
    return jsonify(stack_now=s._data, popped=popped)


@app.route('/ds/queue')
def ds_queue_demo():
    q = Queue()
    q.enqueue('a'); q.enqueue('b'); q.enqueue('c')
    front = q.dequeue()
    return jsonify(queue_now=list(q._data), dequeued=front)


@app.route('/ds/hashtable')
def ds_hashtable_demo():
    ht = HashTable()
    ht.insert('apple', 5); ht.insert('banana', 3)
    return jsonify(items=dict((k, v) for bucket in ht._table.values() for (k, v) in bucket), apple=ht.get('apple'))


@app.route('/ds/pq')
def ds_pq_demo():
    pq = PriorityQueue()
    pq.push(5, "low")
    pq.push(1, "high")
    pq.push(3, "medium")
    popped = pq.pop()
    return jsonify(remaining=[i for (_, i) in pq.queue], popped=popped)


@app.route('/ds/bst')
def ds_bst_demo():
    bst = BinarySearchTree()
    for k in [50, 30, 70, 20, 40, 60, 80]:
        bst.insert(k, str(k))
    inorder = bst.inorder()
    found = bst.search(60)
    notfound = bst.search(999)
    return jsonify(inorder=inorder, found60=found, notfound999=notfound)


@app.route('/ds/graph')
def ds_graph_demo():
    g = Graph()
    edges = [('A', 'B', 1), ('B', 'C', 2), ('A', 'C', 4), ('C', 'D', 1)]
    for u, v, w in edges:
        g.add_edge(u, v, w)
        g.add_edge(v, u, w) 
    path, dist = g.shortest_path('A', 'D')
    return jsonify(path=path, distance=dist)


@app.route('/ds/kmp')
def ds_kmp_demo():
    text = request.args.get('text', 'this is a simple text example')
    patt = request.args.get('pattern', 'simple')
    pos = kmp_search(text, patt)
    return jsonify(text=text, pattern=patt, position=pos)


@app.route('/ds/map')
def ds_map_demo():
    g = Graph()
    roads = [
        ('Cape Town', 'Stellenbosch', 50),
        ('Stellenbosch', 'Paarl', 35),
        ('Paarl', 'Worcester', 55),
        ('Cape Town', 'Somerset West', 45),
        ('Somerset West', 'Stellenbosch', 18),
        ('Worcester', 'Ceres', 60),
        ('Paarl', 'Ceres', 70),
    ]
    for a, b, w in roads:
        g.add_edge(a, b, w)
        g.add_edge(b, a, w)
    start = 'Cape Town'; end = 'Ceres'
    path, distance = g.shortest_path(start, end)
    return jsonify(start=start, end=end, shortest_path=path, distance_km=distance)

@app.route('/ds/map-large')
def ds_map_large():
    try:
        n = int(request.args.get('nodes', '500'))  
        m = int(request.args.get('edges', '2000'))  
    except ValueError:
        return "Invalid nodes/edges params", 400

    nodes = [f"n{i}" for i in range(n)]
    import random
    edges = {node: [] for node in nodes}
    for _ in range(m):
        u = random.choice(nodes)
        v = random.choice(nodes)
        if u == v:
            continue
        w = random.randint(1, 50)
        edges[u].append((v, w))
        edges[v].append((u, w))

    start = request.args.get('start', nodes[0])
    end = request.args.get('end', nodes[-1])

    t0 = time.perf_counter()
    path, dist = dijkstra_shortest_path(edges, start, end)
    elapsed = time.perf_counter() - t0

    return {
        "nodes": n, "edges": m,
        "start": start, "end": end,
        "path_length": len(path) if path else None,
        "distance": dist,
        "time_seconds": elapsed
    }

@app.route('/ds/genome-demo')
def ds_genome_demo():
    fragments = request.args.getlist('f') 
    if not fragments:
        fragments = ["ATCGTAC", "GTACGGA", "CGGATTA", "ATTACCA"]
    import time
    t0 = time.perf_counter()
    assembled = greedy_assemble_fragments(fragments)
    elapsed = time.perf_counter() - t0
    return {
        "fragments": fragments,
        "assembled_length": len(assembled),
        "assembled": assembled,
        "time_seconds": elapsed
    }


print("ROUTES LOADED:")
print(app.url_map)


if __name__ == '__main__':
    app.run(debug=True)



