from flask import Flask, request, render_template, redirect, url_for, flash
from bson.objectid import ObjectId
from pymongo import MongoClient
from dotenv import find_dotenv, load_dotenv
import os
from werkzeug.utils import secure_filename  # allowing file uploads
from werkzeug.security import generate_password_hash, check_password_hash
import flask_login

"i want to get environment variables from my .env"

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

UPLOAD_FOLDER = "resumes"
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}

# Database Initialization
uri = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/?retryWrites=true&w=majority&appName=Cluster0&tlsAllowInvalidCertificates=true"
client = MongoClient(uri)
db = client.get_database("internships")
internships_collection = db.get_collection("internships")  # Collection for internships
user_collection = db.get_collection("users")  # Collection for users
try:
    client.admin.command("ping")
    print("Connected to the database")
except Exception as e:
    print(e)
    print("Unable to connect to the database")

# Initialize the application
app = Flask(__name__)
app.secret_key = '232323112@@11'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

# Initialize the login manager
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# Mock user profile data - will be deleted once MongoDB database is active
user_profile = {
    "photo": "/path/to/photo.jpg",
    "name": "John Doe",
    "title": "Software Developer",
    "location": "New York, NY",
    "email": "john.doe@example.com",
    "linkedin": "https://linkedin.com/in/johndoe",
    "phone": "123-456-7890",
    "portfolio": "http://johndoeportfolio.com",
    "university": "University of Technology",
    "major": "Computer Science",
}

print(f"123 {internships_collection}")

class User(flask_login.UserMixin):
    pass

# Loads user from current session
@login_manager.user_loader
def user_loader(email):
    results = user_collection.find_one({'email' : email})
    if not results:
        return

    user = User()
    user.id = email
    return user

# Loads user from flask request
@login_manager.request_loader
def request_loader(request):
    email = request.form.get("email")
    results = user_collection.find_one({'email' : email})
    if not results:
        return

    user = User()
    user.id = email
    return user

# The route for the log-in page
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        action = request.form['action']
        
        # Attempts to find a DB entry from the Mongo Database
        results = user_collection.find_one({'email' : email})

        # Checks to see if user is already is in the databse
        if action == 'signin' and results and check_password_hash(results['password'], password):
            user = User()
            user.id = email
            flask_login.login_user(user)
            # Redirect to the home page upon successful login
            return redirect(url_for("search"))
        elif action == "signup":
            return redirect(url_for("register"))
        else:
            error = "Invalid credentials"
    return render_template("login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        existing_user = user_collection.find_one({'email' : email})
        # Adds a Database entry if the user isn't already registered
        if existing_user is None:
            hash_pass = generate_password_hash(password)
            user_collection.insert_one({'email' : email, 'password' : hash_pass, 'name' : name})
            flash('Registration successful!', 'success')
            return redirect(url_for('search')) 
        return 'That email already exists!'
    return render_template('register.html')

@app.route("/search")
def search():

    query = request.args.get("query", "")
    
    #criteria fields for search
    
    criteria = ["title", "location", "company_name", "duration"]
    
    #list of regular expression quries 
    criteria_list = [{"$regex": f"{query}", "$options": "i"} for _ in criteria]
    
       
    search_query = {"$or": [{field: query} for field, query in zip(criteria, criteria_list)]}
     
    # Perform Search based on the query by the user 
    internships = internships_collection.find(search_query)
        
    internship_list = list(internships)
    
    return render_template("search.html", internships=internship_list, query=query)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/apply/<internship_id>", methods=["GET" , "POST"])
def show_apply_form(internship_id):
    # Convert the string ID from the URL to an ObjectId
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        cover_letter = request.form["cover_letter"]
        resume = request.files["resume"]
        applications_collection.insert_one({
            "internship_id": ObjectId(internship_id),
            "name": name,
            "email": email,
            "cover_letter": cover_letter,
            "resume": resume.read()
        })
        return redirect(url_for("submit_application", internship_id=internship_id))
    else:
        internship_id_obj = ObjectId(internship_id)
        internship = internships_collection.find_one({"_id": (internship_id_obj)})
        return render_template('application_form.html' , internship=internship)


@app.route("/application-submitted")
def application_submitted():
    return render_template("application_submitted.html")

# Mock data until MongoDB database implemented
user_applications = [
        
        {
            "logo": "path_to_logo.jpg",
            "title": "Software Development Intern",
            "company": "Tech Innovations Inc.",
            "status": "Pending",
            "date_applied": "2024-01-01",
        },
    ]
    
@app.route("/applications", methods=["GET"])

def applications():
    
    sort=request.args.get("sort", "")
    
    #Filter applications alphabetically 
    
    if sort =="ascending":
        sort_applications = sorted(user_applications, key= lambda x: x["title"])
        
    elif sort =="descending":
        sort_applications = sorted(user_applications, key= lambda x: x["title"], reverse=True)
        
    else:
        sort_applications = user_applications
    
    
    return render_template("applications.html", applications=user_applications)
    

@app.route("/chat")
def chat():
    return render_template("campus_chat.html")


@app.route("/profile")
def profile():
    return render_template("profile.html", profile=user_profile)


@app.route("/logout")
def logout():
    flask_login.logout_user()
    return "Logged out"


@login_manager.unauthorized_handler
def unauthorized_handler():
    return "Unauthorized", 401


if __name__ == "__main__":
    app.run(debug=True)
