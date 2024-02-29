from dotenv import load_dotenv
from pymongo import MongoClient
import os


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

uri = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/?retryWrites=true&w=majority&appName=Cluster0&tlsAllowInvalidCertificates=true"
client = MongoClient(uri)
db = client.get_database("internships")
internships_collection = db.get_collection("internships")
internships_collection = db.internships

# List of dummy internships
additional_dummy_internships = [
    {"title": "Marketing Intern", "company_name": "Market Masters Inc.", "location": "Los Angeles, CA", "duration": "4 months", "description": "Assist in developing and implementing marketing strategies to increase our brand awareness."},
    {"title": "Graphic Design Intern", "company_name": "Creative Designs Studio", "location": "San Diego, CA", "duration": "3 months", "description": "Support our design team in creating marketing materials, branding assets, and digital content."},
    {"title": "Finance Intern", "company_name": "Finance First LLC", "location": "New York, NY", "duration": "6 months", "description": "Get hands-on experience in financial modeling, analysis, and reporting with our finance department."},
    {"title": "Human Resources Intern", "company_name": "People Partners", "location": "Chicago, IL", "duration": "5 months", "description": "Learn about recruitment, employee relations, and HR best practices in a dynamic HR team."},
    {"title": "Environmental Science Intern", "company_name": "Green Earth Advocates", "location": "Portland, OR", "duration": "4 months", "description": "Contribute to our environmental projects, research, and initiatives aimed at promoting sustainability."},
]

# Insert additional dummy internships into the MongoDB collection
internships_collection.insert_many(additional_dummy_internships)

print(f"Inserted {len(additional_dummy_internships)} dummy internships into the database.")
