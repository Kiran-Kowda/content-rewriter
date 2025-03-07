import streamlit as st
from google.generativeai import GenerativeModel, configure
import time
from datetime import datetime, timedelta

# Initialize session state
if 'last_request_time' not in st.session_state:
    st.session_state.last_request_time = datetime.min
if 'request_count' not in st.session_state:
    st.session_state.request_count = 0

# Page configuration
st.set_page_config(
    page_title="✨ Content Rewriter",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e7eb 100%);
    }
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: white;
        border-radius: 15px;
        border: 2px solid #e4e7eb;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 25px;
        padding: 10px 30px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    .stSelectbox > div > div {
        background-color: white;
        border-radius: 15px;
        border: 2px solid #e4e7eb;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("✨ Content Rewriter")
st.subheader("Transform your text with AI-powered language and tone adjustment")

# Sidebar
with st.sidebar:
    st.markdown("### Configuration")
    api_key = st.text_input("Enter your Gemini API key:", type="password")
    
    # Language options
    languages = {
        "English (US)": "American English",
        "English (UK)": "British English",
        "Spanish": "Spanish",
        "French": "French",
        "German": "German",
        "Italian": "Italian",
        "Portuguese": "Portuguese",
        "Japanese": "Japanese",
        "Chinese": "Simplified Chinese",
        "Hindi": "Hindi"
    }
    
    # Tone options
    tones = {
        "Professional": "Formal and business-like",
        "Casual": "Relaxed and informal",
        "Friendly": "Warm and approachable",
        "Academic": "Scholarly and research-oriented",
        "Technical": "Precise and technical",
        "Persuasive": "Convincing and influential",
        "Enthusiastic": "Energetic and positive",
        "Formal": "Official and ceremonial",
        "Humorous": "Light-hearted and funny",
        "Empathetic": "Understanding and compassionate",
        "Conversational": "Natural dialogue-like style",
        "Gen-Z": "Modern youth culture style"
    }
    
    target_language = st.selectbox("Select Target Language", list(languages.keys()))
    target_tone = st.selectbox("Select Desired Tone", list(tones.keys()))

# Main content
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Original Text")
    input_text = st.text_area("Enter your text:", height=300)
    word_count = len(input_text.split())
    st.caption(f"Word count: {word_count}")

with col2:
    st.markdown("### Rewritten Text")
    if st.button("✨ Rewrite", disabled=not (api_key and input_text)):
        current_time = datetime.now()
        time_diff = current_time - st.session_state.last_request_time
        
        if time_diff.total_seconds() < 2:
            st.warning("⏳ Please wait a moment before trying again...")
        elif st.session_state.request_count >= 60:
            wait_time = 60 - time_diff.total_seconds()
            st.warning(f"⚠️ Rate limit reached. Please wait {int(wait_time)} seconds.")
        else:
            try:
                with st.spinner("✨ Transforming your text..."):
                    configure(api_key=api_key)
                    model = GenerativeModel(model_name="gemini-2.0-pro-exp-02-05")
                    
                    prompt_context = f"""
                    Rewrite the following text in {languages[target_language]} with a {target_tone.lower()} tone.
                    Maintain the original meaning but adapt the language and style accordingly.
                    
                    Original text: "{input_text}"
                    
                    Provide only the rewritten text without any explanations or additional comments.
                    """
                    
                    response = model.generate_content(prompt_context)
                    rewritten_text = response.text
                    st.text_area("", value=rewritten_text, height=300, disabled=True)
                    
                    # Update rate limiting
                    st.session_state.last_request_time = current_time
                    st.session_state.request_count += 1
                    
                    if time_diff.total_seconds() >= 60:
                        st.session_state.request_count = 0
                    
                    # Show word count comparison
                    new_word_count = len(rewritten_text.split())
                    st.caption(f"Word count: {new_word_count} ({new_word_count - word_count:+d} words)")
                    
            except Exception as e:
                st.error("🎭 Oops! Something went wrong. Please check your API key and try again.")
                st.exception(e)

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; padding: 20px;'>✨ Crafted with AI Magic by Karthik ✨</div>", unsafe_allow_html=True)