import streamlit as st
import pandas as pd
import smtplib
from email.message import EmailMessage
import os
import random

# --- CONFIGURATION ---
st.set_page_config(page_title="Blood Donation Portal", layout="wide")

# --- UI STYLES (EXACTLY AS YOURS) ---
UI_STYLES = """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
<style>
    :root {
        --accent-red: #ff3131;
        --glass-panel: rgba(255, 255, 255, 0.03);
        --glass-border: rgba(255, 255, 255, 0.1);
    }
    /* Force Streamlit to use your background */
    .stApp {
        background: radial-gradient(circle at center, #1a1a1a 0%, #000 100%) !important;
    }
    .main-container {
        background: var(--glass-panel);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 32px;
        padding: 60px 40px;
        margin: auto;
        max-width: 950px;
        text-align: center;
        box-shadow: 0 40px 100px rgba(0,0,0,0.8);
        animation: fadeInDown 0.8s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .heart {
        font-size: 60px;
        filter: drop-shadow(0 0 15px var(--accent-red));
        animation: heartbeat 1.2s infinite;
        margin-bottom: 20px;
        display: inline-block;
    }
    @keyframes heartbeat {
        0% { transform: scale(1); }
        15% { transform: scale(1.25); }
        30% { transform: scale(1); }
    }
    .title { font-size: 3.2rem; font-weight: 900; color: white; text-transform: uppercase; }
    .accent { color: var(--accent-red); }
    .signature { position: fixed; bottom: 20px; left: 20px; font-size: 0.8rem; color: #555; letter-spacing: 2px; }
    
    /* Buttons Styling */
    .stButton>button {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid var(--glass-border) !important;
        color: white !important;
        border-radius: 20px !important;
        padding: 20px !important;
        transition: 0.4s !important;
    }
    .stButton>button:hover {
        border-color: var(--accent-red) !important;
        transform: translateY(-5px);
    }
</style>
<div class="signature">MADE BY JIDON</div>
"""
st.markdown(UI_STYLES, unsafe_allow_html=True)

# --- DATA LOGIC ---
CSV_FILE = "Untitled spreadsheet - Sheet1.csv"

def load_data():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE, encoding='utf-8-sig')
        df.columns = [c.strip() for c in df.columns]
        return df
    return pd.DataFrame(columns=['donar name', 'Blood Group', 'Email'])

df = load_data()

# --- EMAIL ENGINE ---
def send_email(to_email, donor_name, blood_group):
    msg = EmailMessage()
    msg.set_content(f"Hello {donor_name}, urgent {blood_group} blood requested.")
    msg['Subject'] = 'URGENT: Blood Donation'
    msg['From'] = 'funfacts765@gmail.com'
    msg['To'] = to_email
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            # USE YOUR 16-CHAR APP PASSWORD
            server.login('funfacts765@gmail.com', 'mohu xeye wxlk tbps')
            server.send_message(msg)
        return True
    except:
        return False

# --- UI LAYOUT ---
st.markdown(f"""
<div class="main-container">
    <div class="heart">❤️</div>
    <h1 class="title">BLOOD DONATION <span class="accent">PORTAL</span></h1>
    <p style="color: #666;">DONORS: {len(df)} | CENTERS: 7</p>
</div>
""", unsafe_allow_html=True)

st.write("---")

tab1, tab2 = st.tabs(["🔍 Search", "💉 Register"])

with tab1:
    search_bg = st.text_input("Enter Blood Group (e.g., A2B1+)")
    if search_bg:
        results = df[df['Blood Group'].str.upper() == search_bg.upper()]
        if not results.empty:
            for index, row in results.iterrows():
                col1, col2, col3 = st.columns([2, 1, 1])
                col1.write(row['donar name'])
                col2.write(row['Blood Group'])
                if col3.button(f"Email {row['donar name']}", key=index):
                    if send_email(row['Email'], row['donar name'], row['Blood Group']):
                        st.success(f"Sent to {row['donar name']}!")
                    else:
                        st.error("Email failed. Check App Password.")
        else:
            st.warning("No donors found.")

with tab2:
    with st.form("reg_form"):
        new_name = st.text_input("Name")
        new_bg = st.text_input("Blood Group")
        new_email = st.text_input("Email")
        if st.form_submit_button("Submit"):
            st.success(f"Donor {new_name} added locally!")
