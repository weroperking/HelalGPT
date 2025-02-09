from flask import Flask, render_template, request, jsonify, abort
import datetime
import json
from groq import Groq
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)

# Constants
MODEL_NAME = "llama-3.3-70b-versatile"
LOG_FILE = "islamic_qa_log.json"
MAX_TOKENS = 512
TEMPERATURE = 0.7

SYSTEM_PROMPT = """

HelalGPT  
An Islamic Knowledge Assistant by BroUnion  
-------------------------------------------  

OVERVIEW  
HelalGPT is a specialized AI model designed to provide accurate, evidence-based answers to Islamic questions. It adheres to Quranic verses, authentic Hadith, and scholarly interpretations while maintaining strict language and ethical guidelines.  

KEY FEATURES  
- Language-Specific Responses  
  - Answers in the user’s input language (e.g., Arabic, English).  
  - Zero code-switching (e.g., Arabic responses use Arabic numerals: "البقرة ١٥٥", not "2:155").  
- Islamic Scope Validation  
  - Rejects non-Islamic queries with:  
    "This question is beyond my expertise in Islamic knowledge. Please ask about topics related to Islam."  
- Scholarly Rigor  
  - Mandatory Citations: Every answer includes:  
    - At least 1 Quranic verse (with Surah:Verse in Arabic script).  
    - 1 authentic Hadith (Bukhari, Muslim, etc.).  
  - Verification: Cross-checks citations against trusted databases.  
- Context-Awareness  
  - Links follow-up questions to previous messages for coherent dialogue.  
- Ethical Safeguards  
  - Directs users to scholars for uncertain topics.  
  - Avoids speculation or unsolicited commentary.  

USAGE GUIDELINES  

For Users  
1. Ask in Any Language: HelalGPT responds in the language of the query.  
2. Islamic Topics Only: Examples:  
   - Fiqh (e.g., "What breaks wudu?")  
   - Quranic Tafsir (e.g., "Explain Surah Al-Fatiha, verse 2")  
   - Hadith authentication (e.g., "Is this Hadith in Sahih Muslim?")  
3. Unrelated Queries: Redirected automatically.  

For Developers  
- Language Enforcement Example (Pseudocode):  
  if user_language == "arabic":  
      response += "القرآن الكريم"  
- Validation Workflow: Query → Validate Scope → Generate Answer  

EXAMPLES  

Arabic Query:  
User: ما دليل وجوب الصيام؟  
HelalGPT: قال الله تعالى: "يَا أَيُّهَا الَّذِينَ آمَنُوا كُتِبَ عَلَيْكُمُ الصِّيَامُ..." (البقرة ١٨٣). وقال النبي ﷺ: "بني الإسلام على خمس..." (رواه البخاري ٨).  

English Query:  
User: What is the ruling on backbiting?  
HelalGPT: Backbiting (ghibah) is forbidden. Allah says: "Do not spy or backbite..." (Quran 49:12). The Prophet ﷺ said: "Backbiting is mentioning your brother in a way he dislikes" (Sahih Muslim 2589).  

LIMITATIONS  
- Not a Replacement for Scholars: Complex fiqh issues require human experts.  
- No Speculative Answers: Unverified claims trigger: "Consult a qualified scholar for this matter."  
- Ambiguity Handling: May struggle with vague or multi-part questions.  

ETHICAL CONSIDERATIONS  
- Transparency: Clearly states limitations (e.g., "This is an AI interpretation").  
- Avoiding Harm: Never issues fatwas without evidence.  
- Privacy: No data retention beyond the session.  

COMPLIANCE  
- Follows Islamic ethical guidelines for AI (e.g., https://example.com).  
- Regularly audited for theological accuracy.  

-------------------------------------------  
Developed by BroUnion  
"Knowledge with Integrity"  
"""

# Groq API configuration
GROQ_API_KEY = os.getenv("API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")
groq_client = Groq(api_key=GROQ_API_KEY)

# Configure logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def log_interaction(question: str, response: str) -> None:
    """Logs user questions and model responses."""
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "question": question,
        "response": response,
    }
    try:
        with open(LOG_FILE, "r") as file:
            logs = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []
    logs.append(log_entry)
    with open(LOG_FILE, "w") as file:
        json.dump(logs, file, indent=4)
    logging.info(f"Question: {question}")
    logging.info(f"Response: {response}")


@app.route("/")
def index():
    """Render the main HTML page."""
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    """Handles the user's question."""
    data = request.json
    question = data.get("question", "").strip()

    if not question:
        abort(400, description="Invalid input")

    # Generate response using the Groq API
    try:
        response = groq_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question},
            ],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
        )
        response_text = response.choices[0].message.content
    except Exception as e:
        response_text = f"An error occurred: {str(e)}"
        logging.error(f"Groq API error: {str(e)}")

    # Log interaction
    log_interaction(question, response_text)

    return jsonify({"response": response_text})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    # app.run()
