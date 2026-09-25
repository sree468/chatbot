# 🤖 Multilingual AI Assistant Chatbot

An intelligent, context-aware chatbot built with **Streamlit** and Google's advanced Gemini model. It features live Google Search grounding, multilingual voice readout, PDF report generation, and context-driven visual reference retrieval.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg)
![Gemini API](https://img.shields.io/badge/AI-Gemini-4285F4.svg)

---

## ✨ Features

* **Multilingual Answering & Audio:** Responds in and reads aloud answers in **English, Telugu, Hindi, and Kannada** using Google Text-to-Speech (`gTTS`).
* **Contextual Visual References:** Automatically extracts the core entity from your conversation history (resolving pronouns like *"show me an image of it"*) and displays relevant thumbnail images in the sidebar.
* **Live Search Grounding:** Toggleable Google Search tool integration to retrieve up-to-date web information.
* **PDF Export:** Generates downloadable summaries of any conversation turn with a single click.
* **Chat Memory:** Retains prior context across turns to answer follow-up queries naturally.

---

## 📂 Project Structure

```text
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
