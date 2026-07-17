import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700;800;900&family=JetBrains+Mono:wght@600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background: #0E1A1F;
        }

        section[data-testid="stSidebar"] {
            background: #0A1418;
            border-right: 1px solid rgba(0, 172, 193, 0.15);
        }

        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span {
            color: #F5F7FA !important;
            font-weight: 600;
        }

        h1 {
            color: #F5F7FA !important;
            font-weight: 900 !important;
            font-size: 2.8rem !important;
            letter-spacing: -0.5px;
            text-shadow: 0 0 30px rgba(0, 172, 193, 0.25);
        }

        h2 {
            color: #F5F7FA !important;
            font-weight: 800 !important;
            border-left: 4px solid #00ACC1;
            padding-left: 14px;
            font-size: 1.6rem !important;
        }

        h3 {
            color: #B0BEC5 !important;
            font-weight: 700 !important;
        }

        p, li {
            color: #F5F7FA;
            font-weight: 500;
        }

        strong, b {
            color: #00ACC1;
            font-weight: 700;
        }

        div[data-testid="stMetric"] {
            background: rgba(20, 32, 36, 0.7);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(0, 172, 193, 0.25);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        }

        div[data-testid="stMetricValue"] {
            color: #F5F7FA !important;
            font-weight: 800 !important;
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.7rem !important;
        }

        div[data-testid="stMetricLabel"] {
            color: #00ACC1 !important;
            text-transform: uppercase;
            font-size: 0.75rem !important;
            font-weight: 700 !important;
            letter-spacing: 1.5px;
        }

        .stButton>button {
            background: linear-gradient(90deg, #00ACC1, #1E5AA8);
            color: #F5F7FA;
            border-radius: 8px;
            border: none;
            font-weight: 700;
        }

        div[data-testid="stAlert"] {
            border-radius: 10px;
            font-weight: 600;
            background: rgba(20, 32, 36, 0.7);
            backdrop-filter: blur(10px);
        }

        hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, #00ACC1, transparent);
            margin: 1.8rem 0;
        }

        .caption-text {
            color: #B0BEC5;
            font-size: 0.88rem;
            font-weight: 600;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            background: rgba(20, 32, 36, 0.7);
            border-radius: 8px 8px 0 0;
            color: #B0BEC5;
            font-weight: 700;
        }
        .stTabs [aria-selected="true"] {
            background: rgba(0, 172, 193, 0.2) !important;
            color: #00ACC1 !important;
            font-weight: 800;
        }

        .forensic-card {
            background: rgba(20, 32, 36, 0.7);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 14px;
            padding: 22px;
            border: 1px solid rgba(0, 172, 193, 0.25);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        }

        [data-testid="stExpander"] {
            background-color: rgba(20, 32, 36, 0.7) !important;
            border: 1px solid rgba(0, 172, 193, 0.25) !important;
            border-radius: 10px !important;
        }
        [data-testid="stExpander"] summary {
            background-color: rgba(20, 32, 36, 0.9) !important;
        }
        [data-testid="stExpander"] summary p {
            font-size: 1.05rem !important;
            font-weight: 700 !important;
            color: #F5F7FA !important;
        }
        [data-testid="stExpanderDetails"] {
            background-color: rgba(20, 32, 36, 0.5) !important;
        }
        [data-testid="stExpanderDetails"] p, [data-testid="stExpanderDetails"] li {
            color: #F5F7FA !important;
        }
        [data-testid="stExpander"] summary svg,
        [data-testid="stExpander"] svg,
        [data-testid="stExpanderToggleIcon"] {
            fill: #00ACC1 !important;
            stroke: #00ACC1 !important;
            color: #00ACC1 !important;
        }
        </style>
    """, unsafe_allow_html=True)


PALETTE = {
    "bg_main": "#0E1A1F",
    "bg_card": "#141A22",
    "bg_sidebar": "#0A1418",
    "water": "#1E5AA8",
    "vegetation": "#2E7D32",
    "damage": "#C62828",
    "warning": "#F57C00",
    "text_primary": "#F5F7FA",
    "text_secondary": "#B0BEC5",
    "accent": "#00ACC1",
}