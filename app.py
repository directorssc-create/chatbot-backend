import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for Google Sites

# Your IGNOU FAQs stored safely inside the code
FAQS = [
    {
        "keywords": ["assignment", "jama", "submit", "kaise kare"],
        "question": "IGNOU assignment kaise jama karein?",
        "answer": "You can submit your assignments either online through your Regional Centre's official link/portal or offline by visiting your assigned Study Centre in person."
    },
    {
        "keywords": ["igram", "what is igram", "portal", "grievance"],
        "question": "iGRAM kya hai aur IGNOU mein yeh kis kaam aata hai?",
        "answer": "iGRAM (Integrated Grievance Redressal and Management System) is IGNOU's official online portal where students can lodge, track, and resolve academic and administrative complaints."
    },
    {
        "keywords": ["track", "status", "docket", "ticket"],
        "question": "Lodged iGRAM ticket ka status kaise track karein?",
        "answer": "You can track your grievance status on the iGRAM portal using your unique token/grievance number or enrolment ID."
    },
    {
        "keywords": ["admission", "status", "confirm"],
        "question": "IGNOU admission status kaise check karein?",
        "answer": "You can check your admission confirmation status by logging into the IGNOU admission portal (Samarth) using your registered username and password."
    }
]

@app.route("/")
def home():
    return "Chatbot Backend is running smoothly!"

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip().lower()
    
    if not user_message:
        return jsonify({"response": "Please type a question!"})

    # Search logic through the FAQ list
    response_text = None
    for faq in FAQS:
        if any(keyword in user_message for keyword in faq["keywords"]):
            response_text = f"💡 **{faq['question']}**\n\n{faq['answer']}"
            break
            
    if not response_text:
        response_text = "I couldn't find a matching answer. Please try asking about 'assignment', 'iGRAM', 'admission', or 'tracking tickets'."

    return jsonify({"response": response_text})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)