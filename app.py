from flask import Flask, request, render_template, redirect, url_for, flash
from flask_pymongo import PyMongo
import flask_login
from werkzeug.security import generate_password_hash, check_password_hash




app = Flask(__name__)
app.secret_key = 'your_secret_key'

login_manager = flask_login.LoginManager()

login_manager.init_app(app)

# Set up MongoDB with PyMongo
app.config["MONGO_URI"] = "mongodb+srv://teammate:teammate@cluster0.dnhpnsb.mongodb.net/internships?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)



# Mock dataset of internships - will be deleted once MongoDB database is active
internships = [
    {
        'id': 1,
        'title': 'Software Engineering Intern',
        'company_name': 'Tech Innovations Inc.',
        'location': 'San Francisco, CA',
        'duration': '3 months',
        'description': 'Experience hands-on software development...',
        'logo': 'path_to_logo_1.jpg' 
    },
    {
        'id': 2,
        'title': 'Marketing Intern',
        'company_name': 'Market Gurus',
        'location': 'New York, NY',
        'duration': '6 months',
        'description': 'Dive into digital marketing strategies...',
        'logo': 'path_to_logo_2.jpg'
    },
]

# Mock Login Data.
users = {'foo@bar.tld': {'password': 'secret'}}

# Mock user profile data - will be deleted once MongoDB database is active
user_profile = {
    'photo': '/path/to/photo.jpg', 
    'name': 'John Doe',
    'title': 'Software Developer',
    'location': 'New York, NY',
    'email': 'john.doe@example.com',
    'linkedin': 'https://linkedin.com/in/johndoe',
    'phone': '123-456-7890',
    'portfolio': 'http://johndoeportfolio.com',
    'university': 'University of Technology',
    'major': 'Computer Science'
}

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        action = request.form['action']
        accounts = mongo.db.login
        results = accounts.find_one({'email' : email})

        if action == 'signin' and results and check_password_hash(results['password'], password):
            user = User()
            user.id = email
            flask_login.login_user(user)
            # Redirect to the home page upon successful login - need database interaction added
            return redirect(url_for('search'))
        elif action == 'signup':
            return redirect(url_for('register'))
        else:
            error = 'Invalid credentials'
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        accounts = mongo.db.login
        existing_user = accounts.find_one({'email' : email})
        if existing_user is None:
            hash_pass = generate_password_hash(password)
            accounts.insert_one({'email' : email, 'password' : hash_pass, 'name' : name})
            flash('Registration successful!', 'success')
            return redirect(url_for('search')) 
        return 'That email already exists!'
    return render_template('register.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search', '')  
        filtered_internships = [internship for internship in internships if search_query.lower() in internship['title'].lower()]
        return render_template('search.html', internships=filtered_internships, search_query=search_query)
    else:
        return render_template('search.html', internships=internships, search_query='')

@app.route('/apply/<int:internship_id>', methods=['GET', 'POST'])
def apply(internship_id):
    internship = next((item for item in internships if item["id"] == internship_id), None)
    
    if not internship:
        flash('Internship not found.', 'error')
        return redirect(url_for('search'))
    
    if request.method == 'POST':
        flash('Application submitted successfully!', 'success')
        return redirect(url_for('applications')) 
    
    return render_template('apply.html', internship=internship)


@app.route('/applications')
def applications():
    # Mock data until MongoDB database implemented
    user_applications = [
        {
            'logo': 'path_to_logo.jpg',
            'title': 'Software Development Intern',
            'company': 'Tech Innovations Inc.',
            'status': 'Pending',
            'date_applied': '2024-01-01'
        },
    ]
    return render_template('applications.html', applications=user_applications)

@app.route('/chat')
def chat():
    return render_template('campus_chat.html')

@app.route('/profile')
def profile():
    return render_template('profile.html', profile=user_profile)

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401

if __name__ == '__main__':
    app.run(debug=True)

