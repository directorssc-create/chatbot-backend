import os
import re
import random
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from deep_translator import GoogleTranslator

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend/Google Sites

# Translator initialize karein (Auto-detect to English for bilingual support)
try:
    query_translator = GoogleTranslator(source='auto', target='en')
except Exception as e:
    query_translator = None

def translate_to_english(text):
    if not text or not str(text).strip():
        return text
    if query_translator:
        try:
            return query_translator.translate(str(text))
        except Exception:
            return text
    return text

# IGNOU FAQs stored safely inside the code (Excel ki koi zaroorat nahi)
FAQS = [
    {
        "keywords": ['new admission', 'ignou admission process', 'apply online', 'admission form', 'registration', 'naya admission', 'admission kaise karein'],
        "question": 'Sir, mujhe IGNOU me naya admission lena hai. Admission kaise karu?',
        "answer": 'IGNOU admission process is conducted through the official admission portal. Students need to register online, select the desired programme, fill the application form, upload required documents, pay the prescribed fee and submit the application. Students should check the latest admission notification before applying.',
        "category": 'Admission'
    },
    {
        "keywords": ['ignou registration', 'create account', 'new user registration', 'account banana'],
        "question": 'Mera IGNOU registration kaise hoga?',
        "answer": 'Registration is the first step for applying to an IGNOU programme. Students must create an account on the admission portal using a valid mobile number and email ID.',
        "category": 'Admission'
    },
    {
        "keywords": ['ignou eligibility', 'programme qualification', 'admission criteria', 'yogyata'],
        "question": 'Mera admission eligibility clear nahi hai. Main kaunsa programme le sakta hu?',
        "answer": 'Programme eligibility varies according to the programme. Students should check the official programme guide and eligibility criteria before applying.',
        "category": 'Admission'
    },
    {
        "keywords": ['programme change', 'wrong course selection', 'change programme', 'course badalna'],
        "question": 'Maine galat programme select kar liya hai. Kya programme change ho sakta hai?',
        "answer": 'Programme change after admission is allowed only according to IGNOU rules and within the prescribed period, if applicable. Students should submit a request through the prescribed process.',
        "category": 'Admission'
    },
    {
        "keywords": ['fee payment', 'admission fee', 'payment receipt', 'online payment', 'fees bharna'],
        "question": 'Admission fee payment kaise karni hai?',
        "answer": 'Admission fee can be paid through available online payment options provided on the official admission portal. Students should save the payment receipt after successful payment.',
        "category": 'Admission'
    },
    {
        "keywords": ['fee deducted', 'payment successful but admission pending', 'transaction issue', 'paisa kat gaya'],
        "question": 'Maine fees pay kar di hai lekin admission confirm nahi ho raha hai. Kya karu?',
        "answer": 'If the admission fee has been deducted but admission confirmation is not visible, students should wait for payment verification and check the admission portal status. In case of continued delay, submit the payment details through the official support mechanism.',
        "category": 'Admission'
    },
    {
        "keywords": ['re-registration', 'semester continuation', 'yearly registration', 're registration'],
        "question": 'Mera re-registration kaise hoga?',
        "answer": 'Existing IGNOU students who wish to continue their programme must complete re-registration through the official portal during the notified period.',
        "category": 'Admission'
    },
    {
        "keywords": ['study material', 'books delivery', 'ignou books', 'printed material', 'kitab kab milegi'],
        "question": 'IGNOU ka study material kab milega?',
        "answer": 'IGNOU dispatches printed study material to eligible learners after admission confirmation and completion of required processing. Dispatch timelines may vary depending on programme, availability and operational conditions. Students should also use digital resources available through official platforms.',
        "category": 'Study Material Services'
    },
    {
        "keywords": ['assignment download', 'assignment question paper', 'ignou assignment pdf', 'assignment kahan se milega'],
        "question": 'IGNOU assignment kahan se download kar sakte hain?',
        "answer": 'IGNOU assignments are made available through official IGNOU platforms. Students should download the latest assignment questions applicable to their programme and session.',
        "category": 'Assignment Services'
    },
    {
        "keywords": ['assignment last date', 'deadline', 'submission date', 'last date kya hai'],
        "question": 'Assignment submit karne ki last date kya hai?',
        "answer": 'Assignment submission deadlines are notified by IGNOU from time to time. Students should check the latest official notification for applicable dates.',
        "category": 'Assignment Services'
    },
    {
        "keywords": ['tee form', 'exam registration', 'term end examination', 'exam ka form kaise bhare'],
        "question": 'IGNOU Term End Examination (TEE) ke liye form kaise bharna hai?',
        "answer": 'Students must submit the Term End Examination form through the official IGNOU examination portal during the notified examination schedule. Students should ensure that they fulfil eligibility requirements before applying.',
        "category": 'Examination Services'
    },
    {
        "keywords": ['admit card', 'hall ticket', 'exam entry card', 'admit card download'],
        "question": 'IGNOU admit card kaise download karu?',
        "answer": 'IGNOU releases admit cards/hall tickets through the official examination portal before the Term End Examination. Students should download and verify all details.',
        "category": 'Examination Services'
    },
    {
        "keywords": ['ignou result', 'result date', 'tee result', 'result kab aayega'],
        "question": 'IGNOU result kab declare hoga?',
        "answer": 'IGNOU publishes Term End Examination results after completion of evaluation and data processing. Students should regularly check the official result portal and notifications.',
        "category": 'Result & Evaluation'
    },
    {
        "keywords": ['grade card', 'marksheet', 'academic record', 'grade card kaise check karein'],
        "question": 'Grade card kaise check karein?',
        "answer": 'Students can view their grade card through the official IGNOU grade card facility using enrollment details.',
        "category": 'Result & Evaluation'
    },
    {
        "keywords": ['degree certificate', 'final certificate', 'certificate issue', 'degree kab milegi'],
        "question": 'IGNOU degree certificate kab milegi?',
        "answer": 'Degree certificates are issued after successful completion of the programme and after completion of required academic verification processes. Students should check official notifications regarding certificate distribution/dispatch.',
        "category": 'Certificate & Convocation'
    },
    {
        "keywords": ['ignou complaint', 'grievance registration', 'student problem', 'shikayat kaise karein'],
        "question": 'IGNOU me complaint kaise register karein?',
        "answer": 'Students can register their complaints through the official IGNOU grievance redressal mechanism. Students should provide complete details so that the issue can be forwarded to the concerned section.',
        "category": 'Grievance Management'
    },
    {
        "keywords": ['regional centre', 'rc details', 'student centre', 'mera regional centre kaunsa hai'],
        "question": 'Mera Regional Centre kaunsa hai kaise pata chalega?',
        "answer": 'Regional Centre allocation is based on the details provided during admission and the learner’s selected area/location. Students can verify their Regional Centre through official student services.',
        "category": 'Regional Centre & Study Centre Support'
    },
    {
        "keywords": ['working professional', 'job ke saath padhai', 'odl learning', 'job ke sath padh sakte hain'],
        "question": 'Main job ke saath IGNOU se padhai kar sakta hu',
        "answer": 'IGNOU programmes are designed to support learners including working professionals. Students should select programmes according to eligibility and personal study requirements.',
        "category": 'Admission'
    }
]

def search_faq(user_query):
    if not user_query:
        return {
            "answer": "Please ask a question related to IGNOU admission, exams, assignments, or results.",
            "category": "General"
        }
    
    query_lower = user_query.lower().strip()
    # User query ko English me translate karte hain taaki Hindi/Hinglish queries bhi easily match ho sakein
    translated_query = translate_to_english(user_query).lower().strip()
    
    best_match = None
    max_score = 0
    
    for faq in FAQS:
        score = 0
        keywords = [kw.lower() for kw in faq.get("keywords", [])]
        hindi_q = faq.get("question", "").lower()
        english_a = faq.get("answer", "").lower()
        
        # Keyword matching check
        for kw in keywords:
            if kw in translated_query or kw in query_lower:
                score += 3
        
        # Direct word matching in Hindi question
        for word in query_lower.split():
            if len(word) > 2 and word in hindi_q:
                score += 1
                
        # Substring/word matching in answer
        for word in translated_query.split():
            if len(word) > 2 and word in english_a:
                score += 0.5
                
        if score > max_score:
            max_score = score
            best_match = faq
            
    if best_match and max_score > 0:
        return {
            "answer": best_match["answer"],
            "category": best_match["category"]
        }
    else:
        return {
            "answer": "I am sorry, I could not find an exact match for your query. Please visit the official IGNOU website or contact your Regional Centre for assistance.",
            "category": "General"
        }

# Built-in Web UI HTML Template for testing
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IGNOU AI Chatbot (Hindi & English)</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f7f6; margin: 0; padding: 20px; display: flex; justify-content: center; }
        .chat-container { width: 100%; max-width: 600px; background: white; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); overflow: hidden; display: flex; flex-direction: column; height: 80vh; }
        .chat-header { background: #002D62; color: white; padding: 15px; text-align: center; font-size: 18px; font-weight: bold; }
        .chat-messages { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }
        .message { padding: 10px 15px; border-radius: 6px; max-width: 80%; line-height: 1.4; }
        .user-message { background: #002D62; color: white; align-self: flex-end; }
        .bot-message { background: #e9ecef; color: #333; align-self: flex-start; }
        .chat-input-area { display: flex; border-top: 1px solid #ddd; padding: 10px; background: #fff; }
        .chat-input-area input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 4px; outline: none; }
        .chat-input-area button { background: #002D62; color: white; border: none; padding: 10px 20px; margin-left: 10px; border-radius: 4px; cursor: pointer; }
        .chat-input-area button:hover { background: #001f40; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">IGNOU Assistant (Hindi & English Support)</div>
        <div class="chat-messages" id="chatMessages">
            <div class="message bot-message">Hello! Aap IGNOU se juda koi bhi sawal Hindi ya English me pooch sakte hain. (e.g., "Admission kaise karein?" or "How to apply for exams?")</div>
        </div>
        <div class="chat-input-file chat-input-area">
            <input type="text" id="userInput" placeholder="Apna sawal yahan likhein..." onkeypress="if(event.key === 'Enter') sendMessage()">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>
    <script>
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const messages = document.getElementById('chatMessages');
            const text = input.value.trim();
            if(!text) return;
            
            messages.innerHTML += `<div class="message user-message">${text}</div>`;
            input.value = '';
            messages.scrollTop = messages.scrollHeight;
            
            try {
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: text})
                });
                const data = await response.json();
                messages.innerHTML += `<div class="message bot-message"><strong>[Category: ${data.category}]</strong><br>${data.answer}</div>`;
            } catch (err) {
                messages.innerHTML += `<div class="message bot-message">Error connecting to server.</div>`;
            }
            messages.scrollTop = messages.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json() or {}
    user_message = data.get('message', '')
    result = search_faq(user_message)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)