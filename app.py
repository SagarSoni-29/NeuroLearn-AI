from flask import Flask, render_template, request, redirect, session, jsonify
from dotenv import load_dotenv
from groq import Groq
import os
import json
import bcrypt
from PyPDF2 import PdfReader
from docx import Document
from werkzeug.utils import secure_filename

# Load ENV
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# GROQ Config
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# User File
USER_FILE = "users.json"

if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({}, f)

# Upload Folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helpers
def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())


# AI Function
def ask_ai(prompt):

    try:

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ],

            temperature=0.7,
            max_tokens=1024
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Error : {str(e)}"


# Extract PDF Text
def extract_pdf(file_path):

    text = ""

    pdf = PdfReader(file_path)

    for page in pdf.pages:
        content = page.extract_text()

        if content:
            text += content

    return text


# Extract DOCX Text
def extract_docx(file_path):

    doc = Document(file_path)

    text = ""

    for para in doc.paragraphs:
        text += para.text + ""

    return text


# Home
@app.route("/")
def home():
    return render_template("index.html")


# Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        users = load_users()

        if username in users:
            return "User already exists"

        users[username] = hash_password(password)
        save_users(users)

        return redirect("/login")

    return render_template("signup.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        users = load_users()

        if username in users:

            if verify_password(password, users[username]):

                session["user"] = username
                return redirect("/dashboard")

        return "Invalid Credentials"

    return render_template("login.html")


# Dashboard
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html", user=session["user"])


# CHATBOT
@app.route("/chat", methods=["POST"])
def chat():

    data = request.json

    message = data["message"]

    prompt = f"""
    You are NeuroLearn AI,
    a professional educational AI assistant.

    Give answers in a clean professional format.

    Rules:
    - Use headings
    - Use bullet points
    - Keep spacing proper
    - Explain clearly
    - Make output visually structured

    USER QUESTION:
    {message}
    """

    response = ask_ai(prompt)

    return jsonify({"response": response})


# Summarizer
@app.route("/summarize", methods=["POST"])
def summarize():

    data = request.json
    notes = data["notes"]

    prompt = f"Summarize these notes:{notes}"

    response = ask_ai(prompt)

    return jsonify({"summary": response})


# QUIZ Generator
@app.route("/quiz", methods=["POST"])
def quiz():

    data = request.json
    topic = data["topic"]

    prompt = f"Generate 5 quiz questions with answers on {topic}"

    response = ask_ai(prompt)

    return jsonify({"quiz": response})


# Document Chat
@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["file"]

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    file.save(filepath)

    extracted_text = ""

    if filename.endswith(".pdf"):
        extracted_text = extract_pdf(filepath)

    elif filename.endswith(".docx"):
        extracted_text = extract_docx(filepath)

    question = request.form["question"]

    prompt = f"""
    Answer the question based on document.

    DOCUMENT:
    {extracted_text}

    QUESTION:
    {question}
    """

    response = ask_ai(prompt)

    return jsonify({"answer": response})


# Logout
@app.route("/logout")
def logout():

    session.pop("user", None)
    return redirect("/")

# Main
if __name__ == "__main__":
    app.run(debug=True , threaded=True)
