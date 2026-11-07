import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["custom_builders_db"]

projects_col = db["projects"]
quotes_col = db["quotations"]

# প্রথমবার রান করলে ১০টি প্রজেক্ট ডাটাবেজে যুক্ত করার ফাংশন
def seed_initial_projects():
    if projects_col.count_documents({}) < 10:
        projects_col.delete_many({}) # পুরনো কম ডেটা থাকলে রিসেট করে ১০টি দিয়ে ভরবে
        initial_projects = [
            {
                "title": "The Obsidian Villa",
                "category": "Residential",
                "location": "Gulshan, Dhaka",
                "year": "2025",
                "area": "6,500 sq. ft.",
                "image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80",
                "description": "Modern luxury duplex residence featuring architectural concrete, smart home automation, and sustainable solar integration."
            },
            {
                "title": "Apex Corporate Tower",
                "category": "Commercial",
                "location": "Banani, Dhaka",
                "year": "2025",
                "area": "45,000 sq. ft.",
                "image": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=800&q=80",
                "description": "14-story commercial glass tower built with seismic-resistant steel framing and LEED-certified energy-saving systems."
            },
            {
                "title": "Horizon Industrial Hub",
                "category": "Architectural",
                "location": "Savar, Dhaka",
                "year": "2024",
                "area": "80,000 sq. ft.",
                "image": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=800&q=80",
                "description": "Pre-engineered heavy manufacturing facility designed for maximum logistics efficiency and natural ventilation."
            },
            {
                "title": "Greenwood Heights Duplex",
                "category": "Residential",
                "location": "Uttara, Dhaka",
                "year": "2025",
                "area": "4,200 sq. ft.",
                "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
                "description": "Family-centric modern home featuring open-plan living spaces, landscaped rooftop garden, and natural lighting."
            },
            {
                "title": "Metropolitan Plaza",
                "category": "Commercial",
                "location": "Motijheel, Dhaka",
                "year": "2024",
                "area": "30,000 sq. ft.",
                "image": "https://images.unsplash.com/photo-1554469384-e58fac16e23a?auto=format&fit=crop&w=800&q=80",
                "description": "A multi-story retail and corporate shopping plaza equipped with modern elevators, central HVAC, and basement parking."
            },
            {
                "title": "Serenity Lake Resort",
                "category": "Architectural",
                "location": "Purbachal, Dhaka",
                "year": "2025",
                "area": "25,000 sq. ft.",
                "image": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80",
                "description": "Eco-friendly boutique resort villas built with natural timber finishes, stone patios, and panoramic lake views."
            },
            {
                "title": "Skyline Penthouse Suites",
                "category": "Residential",
                "location": "Dhanmondi, Dhaka",
                "year": "2024",
                "area": "5,100 sq. ft.",
                "image": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=800&q=80",
                "description": "Ultra-luxury high-rise penthouse featuring private infinity pool, custom Italian marble flooring, and smart glass walls."
            },
            {
                "title": "Nova Tech Park",
                "category": "Commercial",
                "location": "Agargaon, Dhaka",
                "year": "2026",
                "area": "65,000 sq. ft.",
                "image": "https://images.unsplash.com/photo-1577495508048-b635879837f1?auto=format&fit=crop&w=800&q=80",
                "description": "State-of-the-art IT park designed for software firms, featuring high-speed fiber grids, conference centers, and cafes."
            },
            {
                "title": " Heritage Villa Renovation",
                "category": "Renovation",
                "location": "Wari, Old Dhaka",
                "year": "2024",
                "area": "3,800 sq. ft.",
                "image": "https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=800&q=80",
                "description": "Complete structural restoration and interior modernization of a 40-year-old heritage colonial-style residence."
            },
            {
                "title": "Apex Logistics Warehouse",
                "category": "Architectural",
                "location": "Gazipur, Dhaka",
                "year": "2025",
                "area": "120,000 sq. ft.",
                "image": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=800&q=80",
                "description": "Massive distribution hub with reinforced loading docks, high-bay LED lighting, and fire safety compliance."
            }
        ]
        projects_col.insert_many(initial_projects)

@app.route('/')
def home():
    seed_initial_projects()
    all_projects = list(projects_col.find())
    return render_template('index.html', projects=all_projects)

@app.route('/api/quote', methods=['POST'])
def submit_quote():
    try:
        data = request.json
        new_quote = {
            "name": data.get("name"),
            "email": data.get("email"),
            "phone": data.get("phone"),
            "service": data.get("service"),
            "budget": data.get("budget"),
            "message": data.get("message"),
            "status": "Pending",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        quotes_col.insert_one(new_quote)
        return jsonify({"success": True, "message": "Your quote request has been saved to our database!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/admin')
def admin_panel():
    all_projects = list(projects_col.find())
    all_quotes = list(quotes_col.find().sort("_id", -1))
    return render_template('admin.html', projects=all_projects, quotes=all_quotes)

@app.route('/admin/add-project', methods=['POST'])
def add_project():
    new_project = {
        "title": request.form.get("title"),
        "category": request.form.get("category"),
        "location": request.form.get("location"),
        "year": request.form.get("year"),
        "area": request.form.get("area"),
        "image": request.form.get("image"),
        "description": request.form.get("description")
    }
    projects_col.insert_one(new_project)
    return redirect(url_for('admin_panel'))

@app.route('/admin/delete-project/<project_id>')
def delete_project(project_id):
    projects_col.delete_one({"_id": ObjectId(project_id)})
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)