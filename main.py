import os
from crewai import Crew, Process
from dotenv import load_dotenv
from src.agents import report_analyser,researcher, recommender
from src.tasks import analyze_report,research_health, health_recommendations
from langchain_groq import ChatGroq
from src.utils import create_pdf, send_email, generate_token, decode_token
from flask import Flask, request, jsonify
from src.llms import openai_llm
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from bson import ObjectId


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

bcrypt = Bcrypt(app)
mongo = MongoClient("mongodb://localhost:27017/")
db = mongo.wingify

@app.route('/')
def home():
    return "Server is up and running"

@app.route('/register', methods=['POST'])
def register():
    users = db.users
    data = request.get_json()
    email = data['email']
    print(email)
    password = data['password']
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    users.insert_one({'email': email, 'password': hashed_pw})
    return "Registered Successfully"


@app.route('/login', methods=['POST'])
def login():
    users = db.users
    data = request.get_json()
    email = data['email']
    password = data['password']
    user = users.find_one({'email': email})
    if user and bcrypt.check_password_hash(user['password'], password):
        token = generate_token(str(user["_id"]))
        if not isinstance(token, str):
            return "An error occurred during token generation", 500
        resp = jsonify({"message": "Login successful"})
        print(token)
        resp.set_cookie('token', token, httponly=True, secure=True)
        return resp
    return "Invalid credentials", 401


@app.route('/recommend', methods=['POST'])
def main():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "Please attach your blood test report"
        print(request.files['file'])
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file:
            file.save("uploads/blood_test_report.pdf")
        token = request.cookies.get('token')
        if not token:
            return jsonify({"message": "Please log in"}), 401
        try:
            user_id = decode_token(token) 
        except Exception as e:
            return jsonify({"message": "Invalid token, please log in again"}), 401
        user = db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({"message": "User not found"}), 404
        health_recommender_crew = Crew(
            agents=[report_analyser, researcher, recommender],
            tasks=[analyze_report, research_health, health_recommendations],
            process=Process.hierarchical,
            manager_llm=openai_llm(),
            verbose=2
        )
        result = health_recommender_crew.kickoff();
        create_pdf(result)
        send_email("output/health_recommendations.pdf", user["email"])
        return "Email sent successfully"


if __name__ == "__main__":
      app.run(debug=True)