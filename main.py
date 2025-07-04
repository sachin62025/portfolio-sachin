from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mail import Mail, Message
from forms import ContactForm
import os
import logging
import requests
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("API Key is missing! Please set GEMINI_API_KEY in the .env file.")

# Gemini API URL
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

# Load personal information from the text file
with open("some_information.txt", "r", encoding="utf-8") as file:
    personal_info = file.read()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key-for-development")

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@example.com')
mail = Mail(app)

# Function to check if the user's question is relevant
def is_relevant(question, info):
    question_words = set(question.lower().split())
    info_words = set(info.lower().split())
    common_words = question_words.intersection(info_words)
    return len(common_words) > 0

@app.route('/')
def index():
    return render_template('index.html', active='home')

@app.route('/projects')
def projects():
    return render_template('projects.html', active='projects')

@app.route('/skills')
def skills():
    return render_template('skills.html', active='skills')

@app.route('/education')
def education():
    return render_template('education.html', active='education')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            msg = Message(
                subject=f"Portfolio Contact: {form.subject.data}",
                recipients=["sachinkumar18449@gmail.com"],
                body=f"Name: {form.name.data}\nEmail: {form.email.data}\nMessage: {form.message.data}"
            )
            mail.send(msg)
            flash('Your message has been sent successfully!', 'success')
            return redirect(url_for('contact'))
        except Exception as e:
            app.logger.error(f"Error sending email: {e}")
            flash('Sorry, there was an error sending your message. Please try again later.', 'danger')
    
    return render_template('contact.html', form=form, active='contact')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'response': 'Please enter a message.'})
        
        # Check if question is relevant
        if not is_relevant(user_message, personal_info):
            return jsonify({'response': 'Sorry, this is not related to my information. Please ask something about me.'})
        
        # Prepare request for Gemini API
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{
                "parts": [{
                    "text": f"Based on the following personal information, answer the question:\n\n{personal_info}\n\nUser Question: {user_message}"
                }]
            }]
        }
        
        # Send request to Gemini API
        response = requests.post(URL, headers=headers, json=data)
        
        if response.status_code == 200:
            response_data = response.json()
            try:
                answer = response_data["candidates"][0]["content"]["parts"][0]["text"]
                return jsonify({'response': answer})
            except KeyError:
                return jsonify({'response': 'Sorry, I couldn\'t generate a response.'})
        else:
            return jsonify({'response': 'Error! Please try again later.'})
            
    except Exception as e:
        app.logger.error(f"Chat error: {e}")
        return jsonify({'response': 'Sorry, an error occurred. Please try again later.'})

# Custom error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

# if __name__ == '__main__':
#     app.run(debug=True)



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Get port from environment (Render sets this)
    app.run(host="0.0.0.0", port=port, debug=True)  # Bind to 0.0.0.0