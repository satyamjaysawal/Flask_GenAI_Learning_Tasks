
import openai  # OpenAI se interaction karne ke liye
import os  # Operating system ke functionalities ke liye
from dotenv import load_dotenv  # Environment variables load karne ke liye
from flask import Flask, request, jsonify, render_template  # Flask ke required classes import karna

# Load environment variables from .env file
load_dotenv()  # .env file se environment variables load karna
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # OpenAI API key ko environment se lena

openai.api_key = OPENAI_API_KEY  # OpenAI ke liye API key set karna

app = Flask(__name__)  # Flask app create karna
app.config["UPLOAD_FOLDER"] = "static"  # Uploaded files ka folder define karna

@app.route('/', methods=['GET', 'POST'])  # Route define karna
def main():
    if request.method == "POST":  # Agar request POST hai
        language = request.form["language"]  # User se selected language lena
        file = request.files["file"]  # User se file lena
        
        if file:  # Agar file upload kiya gaya hai
            filename = file.filename  # Filename lena
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # Full path create karna
            file.save(file_path)  # File ko save karna

            try:
                with open(file_path, "rb") as audio_file:  # Audio file ko read mode mein open karna
                    # Transcribing the audio using Whisper
                    transcript = openai.Audio.translate("whisper-1", audio_file)  # Whisper se transcription lena
                    
                # Creating a request to ChatGPT for translation
                response = openai.ChatCompletion.create(
                    model="gpt-4",  # GPT-4 model use karna
                    messages=[
                        {"role": "system", "content": f"You will be provided with a sentence in English, and your task is to translate it into {language}"},
                        {"role": "user", "content": transcript.text}  # Transcription text ko user message ke roop mein dena
                    ],
                    temperature=0,  # Response randomness ko control karne ke liye
                    max_tokens=256  # Max tokens limit set karna
                )
                
                # Returning the response as JSON
                return jsonify(response['choices'][0]['message']['content'])  # JSON response return karna
            
            except Exception as e:  # Agar koi error aaye
                return jsonify({"error": str(e)}), 500  # Error message return karna

    return render_template("index.html")  # GET request ke liye HTML template return karna

if __name__ == "__main__":  # Agar yeh script main hai
    app.run(host="0.0.0.0", debug=True, port=8080)  # Flask app ko run karna
