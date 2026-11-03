from flask import Flask,render_template,request,jsonify
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types



app = Flask(__name__)
load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")

client=genai.Client(api_key=api_key)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/ask",methods=["POST"])
def ask():
    questions=request.form.get("question")

    response=client.models.generate_content(
        model="gemini-3.5-flash",
        contents=questions,
        config=types.GenerateContentConfig(
            system_instruction="you are my personal ai assistant",
            temperature=0.6
        )
    )
    answer=response.text
    return jsonify({"response":answer}),200

@app.route("/summarize",methods=["POST"])
def summarize():
    email_text = request.form.get("email")
    prompt = f"""
    Summarize the following email in 2-3 sentences:
    {email_text}
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction="Act like an expert email assistant.",
            temperature=0.3
        )
    )
    
    summary=response.text
    return jsonify({"response":summary}),200

if __name__=="__main__":
    app.run(debug=True)