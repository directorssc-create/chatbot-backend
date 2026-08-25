import os
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for Google Sites

# Name of your uploaded Excel file
EXCEL_FILE = "ignou_faqs.xlsx"

# Load the Excel file into memory when the server starts
try:
    df = pd.read_excel(EXCEL_FILE)
    # Clean column names to remove accidental trailing spaces
    df.columns = df.columns.str.strip()
    print(f"Successfully loaded {len(df)} FAQs from Excel!")
except Exception as e:
    print(f"Error loading Excel file: {e}")
    df = pd.DataFrame()

@app.route("/")
def home():
    return f"Chatbot Backend is running! FAQs loaded: {len(df)}"

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip().lower()
    
    if not user_message:
        return jsonify({"response": "Please type a question!"})

    if df.empty:
        return jsonify({"response": "FAQ database is currently empty or failed to load."})

    # Search logic: Find the best matching row based on user message keywords
    best_match = None
    
    for _, row in df.iterrows():
        question = str(row.get("Student Question", ""))
        answer = str(row.get("Official Answer", ""))
        keywords = str(row.get("Keywords", ""))
        
        # Combine text to search against
        searchable_text = f"{question} {answer} {keywords}".lower()
        
        # Count how many words from the user message match the FAQ row
        user_words = user_message.split()
        matches = sum(1 for word in user_words if word in searchable_text)
        
        if matches > 0:
            if best_match is None or matches > best_match["score"]:
                best_match = {
                    "score": matches,
                    "question": question,
                    "answer": answer,
                    "steps": str(row.get("Resolution Steps", ""))
                }

    # Format the response if a match is found
    if best_match and best_match["score"] > 0:
        response_text = f"💡 **{best_match['question']}**\n\n{best_match['answer']}"
        
        # Add resolution steps if available in the Excel sheet
        steps = best_match["steps"]
        if steps and steps != "nan" and steps.strip() != "":
            clean_steps = steps.replace("<br>", "\n")
            response_text += f"\n\n**Resolution Steps:**\n{clean_steps}"
    else:
        response_text = "I couldn't find a matching answer in the FAQ database. Please try asking using different keywords."

    return jsonify({"response": response_text})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
