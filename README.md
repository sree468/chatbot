# 🤖 Multilingual How can I help you ?

An intelligent, context-aware chatbot built with **Streamlit** and Google's **Gemini 3.6 Flash** model. It features live Google Search grounding, multilingual voice readout, PDF report generation, and context-driven visual reference retrieval.

---

## ✨ Features

* **Multilingual Answering & Audio:** Responds in and reads aloud answers in **English, Telugu, Hindi, and Kannada** using Google Text-to-Speech (`gTTS`).
* **Contextual Visual References:** Automatically extracts the core entity from your conversation history (resolving pronouns like *"show me an image of it"*) and displays relevant thumbnail images in the sidebar. Displays an explicit *"Sorry No Image"* fallback when no visual exists.
* **Live Search Grounding:** Toggleable Google Search tool integration to retrieve up-to-date web information.
* **PDF Export:** Generates downloadable summaries of any conversation turn with a single click.
* **Chat Memory:** Retains prior context across turns to answer follow-up queries naturally.

---

## 🛠️ Project Structure


chatbot_project/
├── .env                  # API keys (ignored by git)
├── .gitignore            # Git exclusion rules
├── requirements.txt      # Python dependencies
├── app.py                # Main Streamlit interface & chat flow
└── utils/
    ├── __init__.py
    ├── gemini_service.py # Gemini API & language formatting
    ├── image_service.py  # Context-aware image lookups & Wikipedia API
    ├── voice_service.py  # Text cleanup & gTTS audio generation
    └── pdf_service.py    # FPDF2 document generation 


🚀 Getting Started
1. Prerequisites
Python 3.10 or higher

A Gemini API key from Google AI Studio

2. Clone the Repository
Bash
git clone [https://github.com/](https://github.com/)<YOUR-USERNAME>/<YOUR-REPO-NAME>.git
cd <YOUR-REPO-NAME>
3. Create and Activate a Virtual Environment
macOS / Linux:

Bash
python3 -m venv .venv
source .venv/bin/activate
Windows (PowerShell):

PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1
4. Install Dependencies
Bash
pip install -r requirements.txt
5. Configure Secrets
Create a .env file in the root folder:

Code snippet
GEMINI_API_KEY="your_actual_gemini_api_key_here"
6. Run the Application
Bash
streamlit run app.py
Open http://localhost:8501 in your browser.

☁️ Deployment (Streamlit Community Cloud)
Push your repository to GitHub (ensure .env is listed in your .gitignore).

Go to share.streamlit.io and log in with GitHub.

Select your repository, set the branch to main, and the entry point to app.py.

Under Advanced Settings > Secrets, add:

Ini, TOML
GEMINI_API_KEY = "your_actual_gemini_api_key_here"
Click Deploy.

📄 License
This project is licensed under the MIT License.

