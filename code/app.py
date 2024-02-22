from flask import Flask, render_template,redirect , request, session, flash
from database import User,add_to_db, open_db



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

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)