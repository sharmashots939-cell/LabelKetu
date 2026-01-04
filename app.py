app = Flask(__name__)
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import json

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Update User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), default='customer') # 'admin' or 'customer'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- AUTH ROUTES ---

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Hash the password for security
        hashed_pw = generate_password_hash(password, method='sha256')
        
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            # Redirect based on role
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('index'))
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return "Access Denied: Admins Only", 403
    
    # ... (rest of your visualization code from before)
# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False) # In production, use hashing!
    role = db.Column(db.String(10), default='customer') # 'admin' or 'customer'

# Product Model (Updated with Rating)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, default=5.0)

# Sales/Order Model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    amount = db.Column(db.Float)
    date_ordered = db.Column(db.DateTime, default=datetime.utcnow)
    
# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
db = SQLAlchemy(app)


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
    
@app.route('/admin/dashboard')
def admin_dashboard():
    # Logic to protect this page (Admin Only) would go here
    
    # Calculate Data for Visuals
    products = Product.query.all()
    orders = Order.query.all()
    
    total_sales = sum(order.amount for order in orders)
    
    # Prepare data for Chart.js
    labels = [p.name for p in products]
    prices = [p.price for p in products]
    ratings = [p.rating for p in products]

    return render_template('admin.html', 
        labels=json.dumps(labels), 
        prices=json.dumps(prices),
        ratings=json.dumps(ratings),
        total_sales=total_sales)