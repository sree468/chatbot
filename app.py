import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

from utils.image_service import fetch_related_image
from utils.voice_service import generate_speech
from utils.pdf_service import create_pdf

# 1. Environment & API Setup
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY is missing from your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)

# 2. UI Configuration & Styling
st.set_page_config(page_title="Multilingual AI Assistant", page_icon="🌐", layout="wide")

st.markdown("""
<style>
    div.stButton > button:first-child, div.stDownloadButton > button:first-child {
        background-color: #2b2f3a;
        color: #f1f3f5;
        border: 1px solid #4a4f5d;
        border-radius: 8px;
        padding: 0.4rem 0.85rem;
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button:first-child:hover, div.stDownloadButton > button:first-child:hover {
        background-color: #3b4050;
        border-color: #636b7f;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌐 Hi How can I help you?")
st.caption("Answers in English, Telugu, Hindi, or Kannada with voice, PDF export, and reference images.")

# 3. Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "audio_cache" not in st.session_state:
    st.session_state.audio_cache = {}
if "sidebar_image" not in st.session_state:
    st.session_state.sidebar_image = None

# 4. Left Sidebar Display
with st.sidebar:
    st.header("🖼️ Visual Reference")
    
    # Explicit "Sorry No Image" display condition
    if st.session_state.sidebar_image == "NO_IMAGE":
        st.warning("Sorry No Image")
    elif isinstance(st.session_state.sidebar_image, dict):
        img = st.session_state.sidebar_image
        st.image(img["url"], use_container_width=True)
        st.markdown(f"**{img['title']}**")
        if img.get("desc"):
            st.caption(img["desc"])
    else:
        st.info("Visual references related to your prompt will display here.")

    st.divider()
    st.header("⚙️ Language & Settings")
    selected_language = st.selectbox(
        "Response & Audio Language",
        options=["English", "Telugu", "Hindi", "Kannada"],
        index=0
    )
    enable_search = st.checkbox("Enable Google Search Grounding", value=False)
    st.caption("Keep unchecked to conserve API rate limits.")

# 5. Render Previous Chat Messages
for msg_idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
        if message["role"] == "assistant":
            col1, col2 = st.columns([1, 1])
            
            with col1:
                if msg_idx in st.session_state.audio_cache:
                    st.audio(st.session_state.audio_cache[msg_idx], format="audio/mp3")
                else:
                    msg_lang = message.get("language", selected_language)
                    if st.button(f"🔊 Listen ({msg_lang})", key=f"audio_btn_{msg_idx}"):
                        with st.spinner("Generating audio..."):
                            audio_bytes = generate_speech(message["content"], msg_lang)
                            st.session_state.audio_cache[msg_idx] = audio_bytes
                            st.rerun()
                            
            with col2:
                user_query = st.session_state.messages[msg_idx - 1]["content"] if msg_idx > 0 else "Query"
                msg_lang = message.get("language", selected_language)
                pdf_bytes = create_pdf(user_query, message["content"], msg_lang)
                st.download_button(
                    label="📄 Download PDF",
                    data=pdf_bytes,
                    file_name=f"report_{msg_idx}_{msg_lang}.pdf",
                    mime="application/pdf",
                    key=f"pdf_{msg_idx}"
                )

# 6. Chat Input & Processing
if prompt := st.chat_input("Ask a question in any language..."):
    # Grab prior message context before recording this new prompt
    prior_context = list(st.session_state.messages)

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # 1. Fetch related image using context to resolve "it", "this", etc.
    img_data = fetch_related_image(client, prompt, prior_context)
    if img_data:
        st.session_state.sidebar_image = img_data
    else:
        # If user explicitly asked for an image and none was found, trigger "Sorry No Image"
        if any(term in prompt.lower() for term in ["image", "photo", "picture", "it", "look"]):
            st.session_state.sidebar_image = "NO_IMAGE"

    # 2. Generate Assistant Answer with full context
    with st.chat_message("assistant"):
        with st.spinner(f"Thinking in {selected_language}..."):
            try:
                config = None
                if enable_search:
                    config = types.GenerateContentConfig(
                        tools=[types.Tool(google_search=types.GoogleSearch())]
                    )

                # Format conversation history so Gemini knows what "it" means
                history_text = "\n".join(
                    [f"{'User' if m['role']=='user' else 'Assistant'}: {m['content']}" for m in prior_context[-6:]]
                )
                
                system_instruction = (
                    f"You are a helpful assistant. Answer strictly in the {selected_language} language. "
                    f"Use the conversation history to understand context and pronouns like 'it', 'this', or 'that'. "
                    f"Never say you lack context if the subject was discussed in the history above."
                )
                
                full_query = (
                    f"{system_instruction}\n\n"
                    f"Conversation History:\n{history_text}\n\n"
                    f"User Question: {prompt}"
                )

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=full_query,
                    config=config
                )
                
                assistant_response = response.text or "No response generated."
                st.write(assistant_response)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_response,
                    "language": selected_language
                })
                st.rerun()

            except Exception as e:
                err_text = str(e)
                if "429" in err_text or "RESOURCE_EXHAUSTED" in err_text:
                    st.error("Rate limit reached. Please wait a minute or turn off Google Search Grounding in the sidebar.")
                else:
                    st.error(f"Error: {e}")