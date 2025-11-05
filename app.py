from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import csv
import os
from markupsafe import escape
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
PRODUCT_FILE = os.path.join(app.config['UPLOAD_FOLDER'], 'products.csv')
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_products():
    products = []
    if os.path.exists(PRODUCT_FILE):
        with open(PRODUCT_FILE, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 4:
                    name, price, desc, img = row
                    try:
                        price = float(price)
                    except:
                        price = price
                    products.append({'name': name, 'price': price, 'description': desc, 'image_url': img})
    return products

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add', methods=['GET','POST'])
def add_product():
    if request.method == 'POST':
        name = escape(request.form.get('name','')).strip()
        price_raw = request.form.get('price','').strip()
        description = escape(request.form.get('description','')).strip()
        image_url = escape(request.form.get('image_url','')).strip()

        try:
            price = float(price_raw)
        except:
            return render_template('add_product.html', error="Enter a valid numeric price", form=request.form), 400

        with open(PRODUCT_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([name, price, description, image_url])
        return redirect(url_for('view_products'))
    return render_template('add_product.html')

@app.route('/upload', methods=['GET','POST'])
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
    sort = request.args.get('sort','name')
    products = read_products()
    if sort == 'price':
        products = sorted(products, key=lambda p: float(p['price']))
    else:
        products = sorted(products, key=lambda p: p['name'].lower())
    return render_template('view_products.html', products=products, sort=sort)


@app.route('/accessibility')
def accessibility_statement():
    return render_template('accessibility_statement.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/debug_static')
def debug_static():
    css_path = os.path.join(app.root_path, 'static', 'style.css')
    exists = os.path.exists(css_path)
    size = os.path.getsize(css_path) if exists else 0
    return f"CSS file found: {exists}, size: {size} bytes, path: {css_path}"

if __name__ == '__main__':
    app.run(debug=True)
