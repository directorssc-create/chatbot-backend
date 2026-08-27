import os
import difflib
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for Google Sites / frontend integration

# Load FAQs dynamically from the Excel file on startup
EXCEL_FILE = "ignou_faqs.xlsx.xlsx"

def load_faqs():
    if not os.path.exists(EXCEL_FILE):
        print(f"Warning: {EXCEL_FILE} not found!")
        return []
    
    try:
        xls = pd.ExcelFile(EXCEL_FILE)
        df = pd.read_excel(EXCEL_FILE, sheet_name=xls.sheet_names[0])
        
        faqs_list = []
        for _, row in df.iterrows():
            keywords_raw = str(row.get('AI Chatbot Keywords', ''))
            keywords = [kw.strip().lower() for kw in keywords_raw.split(',') if kw.strip()]
            
            faq = {
                "id": str(row.get('FAQ ID', '')),
                "category": str(row.get('Category', '')),
                "keywords": keywords,
                "question": str(row.get('Student Question', '')),
                "answer": str(row.get('Official Answer', '')),
                "resolution_steps": str(row.get('Resolution Steps', '')),
                "required_docs": str(row.get('Required Documents / Information', ''))
            }
            faqs_list.append(faq)
            
        print(f"Successfully loaded {len(faqs_list)} IGNOU FAQs from Excel.")
        return faqs_list
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return []

# Load FAQs into memory on startup
FAQS = load_faqs()

@app.route("/")
def home():
    return f"IGNOU Chatbot Backend is running smoothly! Loaded {len(FAQS)} FAQs with Fuzzy Matching enabled."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    user_message = data.get("message", "").strip().lower()

    if not user_message:
        return jsonify({"response": "Please type a question!"})

    matched_faq = None

    # Step 1: Direct Substring / Keyword Matching (Fast & Precise)
    for faq in FAQS:
        if any(keyword in user_message for keyword in faq["keywords"]):
            matched_faq = faq
            break

    # Step 2: Fuzzy Matching Fallback (Handles Typos if no direct match)
    if not matched_faq and FAQS:
        keyword_map = {}
        all_search_terms = []
        
        for faq in FAQS:
            for kw in faq["keywords"]:
                keyword_map[kw] = faq
                all_search_terms.append(kw)
            # Include original questions for deeper matching context
            q_text = faq["question"].lower()
            keyword_map[q_text] = faq
            all_search_terms.append(q_text)

        # Find close matches using standard library difflib (cutoff=0.45 can be adjusted)
        close_matches = difflib.get_close_matches(user_message, all_search_terms, n=1, cutoff=0.45)
        if close_matches:
            matched_faq = keyword_map[close_matches[0]]

    # Step 3: Format Response
    if matched_faq:
        response_text = f"💡 **{matched_faq['question']}**\n\n"
        response_text += f"{matched_faq['answer']}\n\n"
        
        if matched_faq['resolution_steps'] and matched_faq['resolution_steps'] != 'nan':
            response_text += f"🛠️ **Resolution Steps:**\n{matched_faq['resolution_steps']}\n\n"
            
        if matched_faq['required_docs'] and matched_faq['required_docs'] != 'nan':
            response_text += f"📄 **Required Documents:** {matched_faq['required_docs']}"
    else:
        response_text = (
            "I couldn't find a matching answer in the IGNOU database. "
            "Please try asking about 'admission', 'assignment', 'examination', 'iGRAM', or 'grade card'."
        )
        
    return jsonify({"response": response_text})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)