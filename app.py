from flask import Flask, request, render_template, redirect, url_for, flash
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
from werkzeug.utils import secure_filename #allowing file uploads

"i want to get environment variables from my .env"
from dotenv import find_dotenv, load_dotenv
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

UPLOAD_FOLDER = 'resumes'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

uri = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/?retryWrites=true&w=majority&appName=Cluster0&tlsAllowInvalidCertificates=true"
client = MongoClient(uri)
try:
    client.admin.command('ping')
    print('Connected to the database')
except Exception as e:
    print(e)
    print('Unable to connect to the database')    

#Initialize the application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
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

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        action = request.form['action']
        
        if action == 'signin' and email == 'admin@example.com' and password == 'admin':
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
        flash('Registration successful!', 'success')
        return redirect(url_for('search')) 
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
    application = {
            'name': name,
            'email': email,
            'date_applied': datetime.utcnow(),
            'resume': resume,
            'cover_letter': cover_letter,
            'status': 'Pending'  # Initial status of the application
        }
        # Add the application to the database
    try:
            db.applications.insert_one(application)
            flash('Application submitted successfully!', 'success')
            return redirect(url_for('applications'))
    except Exception as e:
            flash('An error occurred while submitting the application.', 'error')
            print(e)
            return redirect(url_for('apply', internship_id=internship_id)) 
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

if __name__ == '__main__':
    app.run(debug=True)

