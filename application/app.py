
from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        action = request.form['action']
        
        if action == 'signin' and email == 'admin@example.com' and password == 'admin':
            return 'Signed in successfully'
        elif action == 'signup':
            return 'Sign up not implemented yet'
        else:
            error = 'Invalid credentials'
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)

