from flask import Flask, render_template, request
import os
import google.generativeai as genai

# Load environment variables securely using a library like `python-dotenv`
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')  # Use the "gemini-pro" model

app = Flask(__name__)

@app.route('/')
def cover_letter_form():
    return render_template('cover_letter.html', cover_letter=None)

@app.route('/generate', methods=['POST'])
def generate_cover_letter():
    # Extract project details from the form submission
    project_title = request.form.get('project_title')
    project_description = request.form.get('project_description')
    relevant_skills = request.form.get('relevant_skills')

    # Get user's name and information from uploaded text file
    user_info = request.files['user_info']
    user_name = request.form.get('user_name')
    user_info_text = user_info.read().decode('utf-8')

    # Structure the prompt for the Gemini API
    prompt = f"""
{user_info_text}

Compose a properly structured cover letter tailored to a job posting on Upwork.

**Project Title:** {project_title}
**Project Description:** {project_description}

Emphasize {user_name}'s qualifications and expertise relevant to the project title and description.

Ensure correct formatting and spacing in the cover letter, and refrain from mentioning "On Upwork."

"Dear Hiring Manager,

<cover letter content>

Sincerely,
{user_name}"
"""

    # Generate cover letter using the Gemini API
    response = model.generate_content(prompt)
    cover_letter_text = response.text.strip()  # Extract the generated text

    return render_template('cover_letter.html', cover_letter=cover_letter_text)

if __name__ == '__main__':
    app.run(debug=True)  # Set debug=False for production
