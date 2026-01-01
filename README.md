# LabelKetu
an e commerce website for fashion designer ketu

🏗️ The Architecture
To keep it simple, we will use:

Flask: The Python web framework.

SQLite: A "plug-and-play" database that requires no setup.

Flask-SQLAlchemy: To manage your product list.

HTML/CSS: For the look and feel (using a simple style).

1. Project Setup
First, create a folder for your project and install Flask:

          bash
          mkdir boutique_site
          cd boutique_site
          pip install flask flask-sqlalchemy

   Create this folder structure:

   boutique_site/
│
├── app.py              # Your Python logic
├── database.db         # Generated automatically
├── static/             # Images, CSS, JS
│   └── uploads/        # Where product photos will go
└── templates/          # Your HTML files
    └── index.html


2. The Python Code (app.py)
This script will handle the database, the product uploads, and the main store page.

Python
        from flask import Flask, render_template, request, redirect, url_for
        from flask_sqlalchemy import SQLAlchemy
        import os
        
        app = Flask(__name__)
        
        # Database Configuration
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
        app.config['UPLOAD_FOLDER'] = 'static/uploads/'
        db = SQLAlchemy(app)
        
        # Product Model
        class Product(db.Model):
            id = db.Column(db.ID, primary_key=True)
            name = db.Column(db.String(100), nullable=False)
            price = db.Column(db.Float, nullable=False)
            image = db.Column(db.String(100), nullable=False)
        
        # Initialize Database
        with app.app_context():
            db.create_all()
        
        @app.route('/')
        def index():
            products = Product.query.all()
            return render_template('index.html', products=products)
        
        @app.route('/add', methods=['POST'])
        def add_product():
            name = request.form.get('name')
            price = request.form.get('price')
            file = request.files['image']
            
            if file:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                new_product = Product(name=name, price=float(price), image=file.filename)
                db.session.add(new_product)
                db.session.commit()
                
            return redirect(url_for('index'))
        
        if __name__ == '__main__':
            app.run(debug=True)


3. The Frontend (templates/index.html)
This is what your customers will see. It includes a simple form for you to upload products and a grid to display them.

        <!DOCTYPE html>
        <html>
        <head>
            <title>My Boutique</title>
            <style>
                body { font-family: sans-serif; margin: 40px; }
                .product-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
                .card { border: 1px solid #ddd; padding: 10px; border-radius: 8px; text-align: center; }
                img { max-width: 100%; height: 200px; object-fit: cover; }
                .admin-panel { background: #f4f4f4; padding: 20px; margin-bottom: 40px; }
            </style>
        </head>
        <body>
        
            <h1>✨ My Boutique</h1>
        
            <div class="admin-panel">
                <h3>Upload New Product</h3>
                <form action="/add" method="post" enctype="multipart/form-data">
                    <input type="text" name="name" placeholder="Product Name" required>
                    <input type="number" step="0.01" name="price" placeholder="Price" required>
                    <input type="file" name="image" required>
                    <button type="submit">Upload</button>
                </form>
            </div>
        
            <hr>
        
            <div class="product-grid">
                {% for product in products %}
                <div class="card">
                    <img src="{{ url_for('static', filename='uploads/' + product.image) }}">
                    <h3>{{ product.name }}</h3>
                    <p>${{ product.price }}</p>
                    <button>Buy Now</button>
                </div>
                {% endfor %}
            </div>
        
        </body>
        </html>


🚀 How to Run It
Open your terminal in the boutique_site folder.

Run python app.py.

Open your browser and go to http://127.0.0.1:5000.

