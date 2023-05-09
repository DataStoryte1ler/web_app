from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/market'
db = SQLAlchemy(app)

class Customer(db.Model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))

    def __init__(self, name, email, phone, address):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address

@app.route('/')
def index():
    customers = Customer.query.all()
    return render_template('index.html', customers=customers)

@app.route('/search', methods=['POST'])
def search():
    search_query = request.form['search_query']
    customers = Customer.query.filter(Customer.name.ilike(f'%{search_query}%')).all()
    return render_template('index.html', customers=customers)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        customer = Customer(name, email, phone, address)
        db.session.add(customer)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('add.html')

@app.route('/edit/<int:customer_id>', methods=['GET', 'POST'])
def edit(customer_id):
    customer = Customer.query.filter_by(customer_id=customer_id).first()
    if request.method == 'POST':
        customer.name = request.form['name']
        customer.email = request.form['email']
        customer.phone = request.form['phone']
        customer.address = request.form['address']
        db.session.commit()
        return redirect('/')
    else:
        return render_template('edit.html', customer=customer)

@app.route('/delete/<int:customer_id>', methods=['POST'])
def delete(customer_id):
    customer = Customer.query.filter_by(customer_id=customer_id).first()
    db.session.delete(customer)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

