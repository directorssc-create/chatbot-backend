# IGNOU Student Support - FAQ Chatbot

A production-ready, Render Free Tier compatible AI Chatbot designed for IGNOU students. It answers queries about admissions, assignments, examinations, results, and grievances using a lightweight text-matching algorithm.

## Features
* **Bilingual Support:** Handles English, Hindi, and Hinglish naturally.
* **Lightweight Backend:** Built with Flask and RapidFuzz; requires no GPU, databases, or heavy LLMs.
* **Confidence System:** Detects edge cases and provides safe fallbacks instead of hallucinating answers.
* **Embeddable Frontend:** A standalone, responsive HTML file that can be embedded into Google Sites via `<iframe>`.

## Local Setup & Testing
1. Clone the repository: `git clone <repo-url> && cd ignou-chatbot`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment (Windows: `venv\Scripts\activate` / Mac/Linux: `source venv/bin/activate`).
4. Install dependencies: `pip install -r requirements.txt`
5. Run the server: `python main.py`
6. Open `frontend/index.html` in your browser.

## Deployment Instructions

### 1. GitHub Setup
Push the `main.py` and `requirements.txt` to your GitHub repository.

### 2. Render Deployment (Backend)
1. Go to [Render](https://render.com) and click **New -> Web Service**.
2. Connect your GitHub repository.
3. Configure the service:
   * **Language:** Python 3
   * **Build Command:** `pip install -r requirements.txt`
   * **Start Command:** `gunicorn main:app`
4. Set Environment Variables:
   * `PYTHON_VERSION` : `3.10.0` (Recommended)
5. Deploy. Wait for the service to go live and note your actual `onrender.com` URL.

### 3. Google Sites Embedding (Frontend)
1. Open `frontend/index.html` in a text editor.
2. Update the `API_URL` constant on line 125 to point to your new Render deployment (e.g., `https://your-app.onrender.com/chat`).
3. In Google Sites, go to **Insert -> Embed -> Embed Code**.
4. Paste the entire code of `index.html` into the box and click Next -> Insert.

## Troubleshooting
* **Long First Request Time:** Render Free Tier sleeps after 15 mins of inactivity. The frontend is coded to catch timeouts and display a "waking up" message.
* **Updating FAQs:** Open `main.py` and append new dictionary objects to the `RAW_FAQS` list.