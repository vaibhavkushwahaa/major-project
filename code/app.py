from flask import Flask, render_template,redirect , request, session, flash
from database import User,add_to_db, open_db
import os


app = Flask(__name__)
app.secret_key = 'vaibhavkushwaha'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email=request.form.get('email')
        password=request.form.get('password')
        print("email->",email)
        print("password->",password)
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        cpassword=request.form.get('cpassword')
        print("username->",username)
        print("email->",email)
        print("password->",password)
        print("cpassword->",cpassword)


        if len(username) == 0 or len(email) == 0 or len(password) == 0 or len(cpassword) == 0:
            flash("All fields are required", "danger")
            return redirect('/register')
        user=User(username=username,email=email,password=password)

        if password != cpassword:
            flash("Password and Confirm Password should be same", "danger")
            return redirect('/register')
        
        add_to_db(user)


    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/stock/prediction', methods=['GET', 'POST'])
def stock():
    if request.method == 'POST':
        stockname=request.form.get('stockname')
        # yfinance fetch data
        model_path =os.path.join(os.getcwd(), 'static','trained_model',f'{stockname}_prediction.h5')
        if os.path.exists(model_path):
            print("Model loaded")
            return render_template('prediction.html')
        else:
            print("Model not found")
    return render_template('stock.html')

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)