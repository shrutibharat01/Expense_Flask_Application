from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime


app = Flask(__name__)
app.secret_key = os.urandom(24)


# Configuring the SQLAlchemy connection string
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/user_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Define a User model
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)  # Primary key field
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


# Define a Expense model
class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    # Relationship to Users
    user = db.relationship('Users', backref=db.backref('expenses', lazy=True))

    def __repr__(self):
        return f'<Expense {self.description} - Rs {self.amount}>'


# Define a Income model
class Income(db.Model):
    __tablename__ = 'incomes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    # Relationship to Users
    user = db.relationship('Users', backref=db.backref('incomes', lazy=True))

    def __repr__(self):
        return f'<Income {self.description} - Rs {self.amount}>'



@app.route('/')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/home')
def home():
    if 'user_id' in session:
        user_id = session['user_id']
        user = Users.query.get(user_id)
        
        # Fetch total earnings
        total_earnings = db.session.query(db.func.sum(Income.amount)).filter_by(user_id=user_id).scalar() or 0
        # Fetch total expenses
        total_expenses = db.session.query(db.func.sum(Expense.amount)).filter_by(user_id=user_id).scalar() or 0
        # Fetch counts for transactions
        total_expenses_count = Expense.query.filter_by(user_id=user_id).count()
        total_income_count = Income.query.filter_by(user_id=user_id).count()
        # Fetch recent expenses
        recent_expenses = Expense.query.filter_by(user_id=user_id).order_by(Expense.date.desc()).limit(5).all()
        # Fetch recent income
        recent_income = Income.query.filter_by(user_id=user_id).order_by(Income.date.desc()).limit(5).all()
        return render_template('home.html', total_earnings=total_earnings, total_expenses=total_expenses, 
                               total_expenses_count=total_expenses_count, total_income_count=total_income_count,
                               recent_expenses=recent_expenses, recent_income=recent_income)
    else:
        return redirect(url_for('login'))


@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')

    user = Users.query.filter_by(email=email).first()

    # Check if user exists and password is correct
    if user and user.password == password:
        session['user_id'] = user.id  # Store user ID in session
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))


@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')
    
    # Create a new instance of the Users model
    new_user = Users(name=name, email=email, password=password)
    # Add the new user to the session
    db.session.add(new_user)
    # Commit the transaction to the database
    db.session.commit()
    
    return redirect(url_for('login'))


@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        description = request.form.get('description')
        amount = float(request.form.get('amount'))
        date = request.form.get('date')
        entry_type = request.form.get('entry_type')  # 'expense' or 'income'

        if entry_type == 'expense':
            new_entry = Expense(user_id=session['user_id'], description=description, amount=amount, date=date)
        elif entry_type == 'income':
            new_entry = Income(user_id=session['user_id'], description=description, amount=amount, date=date)
        else:
            return redirect(url_for('home'))  # Invalid entry type

        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('add_entry.html')


@app.route('/add_expense', methods=['POST'])
def add_expense():
    if 'user_id' in session:
        description = request.form.get('description')
        amount = request.form.get('amount')
        date = request.form.get('date')
        user_id = session['user_id']
        
        # Create a new expense instance
        new_expense = Expense(description=description, amount=amount, date=datetime.strptime(date, '%Y-%m-%dT%H:%M'), user_id=user_id)
        db.session.add(new_expense)
        db.session.commit()
        
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/add_income', methods=['POST'])
def add_income():
    if 'user_id' in session:
        description = request.form.get('description')
        amount = request.form.get('amount')
        date = request.form.get('date')
        user_id = session['user_id']
        
        # Create a new income instance
        new_income = Income(description=description, amount=amount, date=datetime.strptime(date, '%Y-%m-%dT%H:%M'), user_id=user_id)
        db.session.add(new_income)
        db.session.commit()
        
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))
    

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)