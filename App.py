import streamlit as st
import os
from datetime import datetime
import pandas as pd
from data_cleaning import load_and_clean_data, clean_text
from openai import OpenAI

# Set page configuration
st.set_page_config(
    page_title="Saham Indo Chatbot",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .chat-container {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin-bottom: 10px;
    }
    .user-message {
        background-color: #d4e6f1;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        text-align: right;
    }
    .bot-message {
        background-color: #e8f5e9;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        text-align: left;
    }
    /* Custom input styling - remove red border on focus */
    input:focus {
        border-color: #1f77b4 !important;
        box-shadow: 0 0 0 0.2rem rgba(31, 119, 180, 0.25) !important;
    }
    input {
        border-color: #e0e0e0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Callback function untuk clear input
def clear_input():
    st.session_state.user_input = ""

# Load and cache data cleaning
@st.cache_resource
def get_cleaned_data():
    """Load and clean data from CSV file"""
    try:
        data = load_and_clean_data("data.csv")
        return data
    except Exception as e:
        st.warning(f"⚠️ Error loading data: {e}")
        return None

# Load data
cleaned_data = get_cleaned_data()

# OpenAI Configuration untuk Fine-tuned Model
OPENAI_API_KEY = os.getenv("OPEN_API_KEY")
FINE_TUNED_MODEL = os.getenv("FINE_TUNED_MODEL")

@st.cache_resource
def get_openai_client():
    """Initialize OpenAI client"""
    return OpenAI(api_key=OPENAI_API_KEY)

# Initialize OpenAI client
try:
    openai_client = get_openai_client()
    openai_available = True
except Exception as e:
    st.warning(f"⚠️ OpenAI client error: {e}")
    openai_available = False

# Simple bot response function (defined before use)
def get_bot_response(user_message):
    """
    Fungsi untuk menghasilkan respons chatbot dengan Fine-tuned GPT-4o Model
    """
    user_message_lower = user_message.lower()
    
    # Dictionary respons sederhana untuk keywords umum
    quick_responses = {
        "halo": "Halo! 👋 Selamat datang di Saham Indo Chatbot. Ada yang bisa saya bantu?",
        "bantuan": "Saya bisa membantu Anda dengan analisis sentimen pasar saham Indonesia. Silakan kirimkan teks atau berita tentang saham! 😊",
    }
    
    # Check quick responses dulu
    for keyword, response in quick_responses.items():
        if keyword in user_message_lower:
            return response
    
    # Gunakan fine-tuned model untuk analisis sentimen
    if openai_available and len(user_message) > 5:
        try:
            response = openai_client.chat.completions.create(
                model=FINE_TUNED_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "Kamu adalah model analisis sentimen saham Indonesia yang ahli. Analisis teks berikut dan berikan: 1) Sentimen Akhir (Positive/Negative/Neutral), 2) Analisis Detail dari analis. Format: Sentimen Akhir: [sentiment]\n\nAnalisis : [detail analysis]\n\n"
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            analysis_result = response.choices[0].message.content.strip()
            
            # Parse and format hasil
            if "Sentimen Akhir:" in analysis_result:
                # Formatting sudah dari model
                return f"📊 Hasil Analisis Sentimen:\n\n{analysis_result}"
            else:
                return f"📊 Hasil Analisis:\n\n{analysis_result}"
                
        except Exception as e:
            st.warning(f"⚠️ Model analysis error: {e}")
            # Fallback ke simple analysis
            return get_simple_analysis(user_message)
    else:
        # Fallback ke simple analysis jika model tidak available atau text terlalu pendek
        return get_simple_analysis(user_message)

def get_simple_analysis(user_message):
    """
    Fallback simple sentiment analysis menggunakan cleaned data
    """
    cleaned_user_input = clean_text(user_message)
    
    if cleaned_data is not None and cleaned_user_input:
        # Cek apakah ada similarity dengan data yang ada
        try:
            first_word = cleaned_user_input.split()[0]
            similar_records = cleaned_data[
                cleaned_data['cleaned_text'].str.contains(first_word, na=False)
            ]
            
            if len(similar_records) > 0:
                sentiments = similar_records['Sentiment'].value_counts()
                top_sentiment = sentiments.index[0]
                percentage = (sentiments.iloc[0] / len(similar_records)) * 100
                
                return f"""📊 Analisis Sentimen (Berdasarkan Data):

Sentimen Akhir: {top_sentiment}

Analisis: Berdasarkan {len(similar_records)} records serupa dalam dataset, topik ini dominan memiliki sentimen {top_sentiment.lower()} ({percentage:.1f}%)."""
        except:
            pass
    
    # Default response
    return f"""📊 Analisis Sentimen:

Silakan gunakan model fine-tuned untuk analisis detail. Teks Anda akan dianalisis oleh GPT-4o untuk memberikan:
- Sentimen Akhir (Positive/Negative/Neutral)
- Analisis detail dari perspektif analis pasar

Mohon upgrade koneksi OpenAI API jika belum tersedia."""

# Title and header
st.title("💬 Saham Indo Chatbot")
st.markdown("---")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Pengaturan")
    
    # Clear chat history
    if st.button("🔄 Bersihkan Riwayat Chat", use_container_width=True):
        st.session_state.messages = []
        st.success("Riwayat chat telah dihapus!")
        st.rerun()
    
    st.markdown("---")
    
    # Information section
    st.subheader("ℹ️ Informasi")
    st.info("""
    Chatbot ini dirancang untuk membantu Anda dengan:
    - Informasi saham Indonesia
    - Analisis pasar
    - Tips investasi
    - Pertanyaan umum
    """)
    
    
    # date info
    st.markdown("---")
    st.text(f"Dibuat pada: {datetime.now().strftime('%d-%m-%Y %H:%M')}")

# Display chat history
st.subheader("💭 Riwayat Percakapan")

# Chat display area
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message"><b>Anda:</b> {message["content"]}</div>', 
                       unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message"><b>Bot:</b> {message["content"]}</div>', 
                       unsafe_allow_html=True)

st.markdown("---")

# Input area
st.subheader("📝 Kirim Pesan")

# Use form for better input handling
with st.form(key="message_form", clear_on_submit=True):
    col1, col2 = st.columns([0.9, 0.1])
    
    with col1:
        user_input = st.text_input(
            "Ketik pesan Anda di sini...",
            placeholder="Misalnya: Apa itu saham?",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.form_submit_button("📤 Kirim", use_container_width=True)
    
    # Process user input
    if send_button and user_input:
        # Add user message to history
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Get bot response
        bot_response = get_bot_response(user_input)
        
        # Add bot message to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": bot_response
        })
        
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Made with ❤️ using Streamlit | Saham Indo Capstone</p>
</div>
""", unsafe_allow_html=True)