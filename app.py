import streamlit as st
import os
import json
import base64
import textwrap
from pathlib import Path
from io import BytesIO
from PIL import Image
import requests
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="EcoSort – Intelligent Waste Classification",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# DESIGN SYSTEM & CUSTOM CSS
# ============================================================================

DESIGN_TOKENS = {
    "background": "#f5f3f0",  # warm off-white/ivory
    "surface": "#faf8f6",      # slightly warmer surface
    "primary": "#1b4d2e",      # deep forest green
    "secondary": "#6b9b7e",    # sage green
    "accent": "#a8d5ba",       # soft sage/lime
    "text": "#1a1a1a",         # near-black
    "text_muted": "#6b7565",   # gray-green
    "border": "#d9d6d0",       # subtle gray-green
    "success": "#a8d5ba",
    "warning": "#e8b8a1",
    "error": "#c85a54",
}

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }}
    
    /* ROOT STYLES */
    html, body, [data-testid="stAppViewContainer"] {{
        background-color: {DESIGN_TOKENS["background"]};
        color: {DESIGN_TOKENS["text"]};
    }}
    
    [data-testid="stHeader"] {{
        background-color: transparent;
        border-bottom: none;
    }}
    
    /* SCROLLBAR */
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    ::-webkit-scrollbar-track {{
        background: {DESIGN_TOKENS["background"]};
    }}
    ::-webkit-scrollbar-thumb {{
        background: {DESIGN_TOKENS["border"]};
        border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: {DESIGN_TOKENS["text_muted"]};
    }}
    
    /* REMOVE STREAMLIT DEFAULT ELEMENTS */
    [data-testid="stToolbar"] {{
        display: none;
    }}
    
    /* CONTAINER & SPACING */
    [data-testid="stMainBlockContainer"] {{
        padding: 0 !important;
    }}
    
    .main {{
        padding: 0 !important;
        background-color: {DESIGN_TOKENS["background"]};
    }}
    
    /* SECTION PADDING */
    .section {{
        padding: 80px 60px;
    }}
    
    .section.hero {{
        padding: 120px 60px;
        background-color: {DESIGN_TOKENS["background"]};
    }}
    
    .section.full {{
        width: 100vw;
        margin-left: calc(-50vw + 50%);
        padding: 80px calc(50vw - 50%);
    }}
    
    @media (max-width: 768px) {{
        .section {{
            padding: 60px 24px;
        }}
        .section.hero {{
            padding: 80px 24px;
        }}
    }}
    
    /* TYPOGRAPHY SCALE */
    h1 {{
        font-size: 90px;
        font-weight: 700;
        letter-spacing: -2px;
        line-height: 1.1;
        color: {DESIGN_TOKENS["primary"]};
        margin: 0;
    }}
    
    h2 {{
        font-size: 56px;
        font-weight: 700;
        letter-spacing: -1px;
        line-height: 1.2;
        color: {DESIGN_TOKENS["primary"]};
        margin: 0 0 32px 0;
    }}
    
    h3 {{
        font-size: 32px;
        font-weight: 600;
        line-height: 1.3;
        color: {DESIGN_TOKENS["primary"]};
        margin: 0 0 20px 0;
    }}
    
    .subtitle {{
        font-size: 18px;
        font-weight: 400;
        color: {DESIGN_TOKENS["text_muted"]};
        line-height: 1.6;
        letter-spacing: 0.3px;
    }}
    
    .tagline {{
        font-size: 14px;
        font-weight: 500;
        color: {DESIGN_TOKENS["secondary"]};
        letter-spacing: 1px;
        text-transform: uppercase;
    }}
    
    /* TEXT STYLES */
    .body-lg {{
        font-size: 18px;
        font-weight: 400;
        line-height: 1.7;
        color: {DESIGN_TOKENS["text"]};
    }}
    
    .body {{
        font-size: 16px;
        font-weight: 400;
        line-height: 1.6;
        color: {DESIGN_TOKENS["text"]};
    }}
    
    .body-sm {{
        font-size: 14px;
        font-weight: 400;
        line-height: 1.5;
        color: {DESIGN_TOKENS["text_muted"]};
    }}
    
    /* BUTTONS */
    button {{
        font-family: 'Inter', sans-serif;
    }}
    
    .btn {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        padding: 14px 28px;
        font-size: 16px;
        font-weight: 500;
        border-radius: 24px;
        border: none;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-decoration: none;
    }}
    
    .btn-primary {{
        background-color: {DESIGN_TOKENS["primary"]};
        color: white !important;
    }}
    
    .btn-primary:hover {{
        background-color: #0f3620;
        color: white !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(27, 77, 46, 0.15);
    }}
    
    .btn-secondary {{
        background-color: transparent;
        color: {DESIGN_TOKENS["primary"]};
        border: 1.5px solid {DESIGN_TOKENS["primary"]};
    }}
    
    .btn-secondary:hover {{
        background-color: {DESIGN_TOKENS["primary"]};
        color: white;
    }}
    
    /* CARDS */
    .card {{
        background-color: {DESIGN_TOKENS["surface"]};
        border: 1px solid {DESIGN_TOKENS["border"]};
        border-radius: 12px;
        padding: 40px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    .card:hover {{
        border-color: {DESIGN_TOKENS["secondary"]};
        box-shadow: 0 8px 20px rgba(27, 77, 46, 0.08);
        transform: translateY(-2px);
    }}
    
    /* CATEGORY BADGE */
    .category-badge {{
        display: inline-block;
        padding: 10px 20px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 14px;
        letter-spacing: 0.5px;
        margin: 8px 0;
    }}
    
    .badge-recyclable {{
        background-color: rgba(168, 213, 186, 0.2);
        color: {DESIGN_TOKENS["secondary"]};
        border: 1px solid {DESIGN_TOKENS["accent"]};
    }}
    
    .badge-organic {{
        background-color: rgba(168, 213, 186, 0.15);
        color: {DESIGN_TOKENS["secondary"]};
        border: 1px solid {DESIGN_TOKENS["accent"]};
    }}
    
    .badge-hazardous {{
        background-color: rgba(200, 90, 84, 0.1);
        color: {DESIGN_TOKENS["error"]};
        border: 1px solid {DESIGN_TOKENS["error"]};
    }}
    
    .badge-electronic {{
        background-color: rgba(107, 155, 126, 0.1);
        color: {DESIGN_TOKENS["secondary"]};
        border: 1px solid {DESIGN_TOKENS["secondary"]};
    }}
    
    .badge-reusable {{
        background-color: rgba(232, 184, 161, 0.15);
        color: {DESIGN_TOKENS["warning"]};
        border: 1px solid {DESIGN_TOKENS["warning"]};
    }}
    
    .badge-general {{
        background-color: rgba(107, 117, 101, 0.08);
        color: {DESIGN_TOKENS["text_muted"]};
        border: 1px solid {DESIGN_TOKENS["border"]};
    }}
    
    /* DROPZONE */
    .upload-zone {{
        border: 2px dashed {DESIGN_TOKENS["border"]};
        border-radius: 16px;
        padding: 60px 40px;
        text-align: center;
        background-color: {DESIGN_TOKENS["surface"]};
        transition: all 0.3s ease;
        cursor: pointer;
    }}
    
    .upload-zone:hover {{
        border-color: {DESIGN_TOKENS["secondary"]};
        background-color: rgba(107, 155, 126, 0.03);
    }}
    
    .upload-zone.dragging {{
        border-color: {DESIGN_TOKENS["primary"]};
        background-color: rgba(27, 77, 46, 0.05);
    }}
    
    /* MARQUEE */
    .marquee-container {{
        overflow: hidden;
        background-color: {DESIGN_TOKENS["primary"]};
        padding: 24px 0;
    }}
    
    .marquee {{
        display: flex;
        animation: scroll-left 30s linear infinite;
        white-space: nowrap;
    }}
    
    .marquee-item {{
        color: white;
        font-size: 18px;
        font-weight: 600;
        padding: 0 40px;
        letter-spacing: 1px;
    }}
    
    @keyframes scroll-left {{
        0% {{
            transform: translateX(0);
        }}
        100% {{
            transform: translateX(-50%);
        }}
    }}
    
    /* RESULT CARD */
    .result-card {{
        background-color: {DESIGN_TOKENS["surface"]};
        border: 1px solid {DESIGN_TOKENS["border"]};
        border-radius: 16px;
        padding: 48px;
        margin: 32px 0;
    }}
    
    .result-item {{
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-bottom: 32px;
    }}
    
    .result-label {{
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: {DESIGN_TOKENS["text_muted"]};
    }}
    
    .result-value {{
        font-size: 24px;
        font-weight: 700;
        color: {DESIGN_TOKENS["primary"]};
    }}
    
    /* DIVIDER */
    .divider {{
        height: 1px;
        background-color: {DESIGN_TOKENS["border"]};
        margin: 32px 0;
    }}
    
    /* GRID */
    .grid {{
        display: grid;
        gap: 32px;
    }}
    
    .grid-2 {{
        grid-template-columns: repeat(2, 1fr);
    }}
    
    .grid-3 {{
        grid-template-columns: repeat(3, 1fr);
    }}
    
    @media (max-width: 768px) {{
        .grid-2, .grid-3 {{
            grid-template-columns: 1fr;
        }}
        
        h1 {{
            font-size: 48px;
        }}
        
        h2 {{
            font-size: 36px;
        }}
        
        h3 {{
            font-size: 24px;
        }}
    }}
    
    /* STAT */
    .stat {{
        text-align: center;
    }}
    
    .stat-value {{
        font-size: 56px;
        font-weight: 700;
        color: {DESIGN_TOKENS["primary"]};
        line-height: 1;
        margin-bottom: 8px;
    }}
    
    .stat-label {{
        font-size: 16px;
        font-weight: 500;
        color: {DESIGN_TOKENS["text_muted"]};
        letter-spacing: 0.5px;
    }}
    
    /* CONFIDENCE INDICATOR */
    .confidence-high {{
        color: {DESIGN_TOKENS["success"]};
        font-weight: 600;
    }}
    
    .confidence-medium {{
        color: {DESIGN_TOKENS["warning"]};
        font-weight: 600;
    }}
    
    .confidence-low {{
        color: {DESIGN_TOKENS["error"]};
        font-weight: 600;
    }}
    
    /* ALERTS */
    .alert {{
        border-radius: 12px;
        padding: 20px 24px;
        border-left: 4px solid;
        margin: 20px 0;
    }}
    
    .alert-info {{
        background-color: rgba(168, 213, 186, 0.1);
        border-color: {DESIGN_TOKENS["secondary"]};
        color: {DESIGN_TOKENS["primary"]};
    }}
    
    .alert-warning {{
        background-color: rgba(232, 184, 161, 0.1);
        border-color: {DESIGN_TOKENS["warning"]};
        color: {DESIGN_TOKENS["warning"]};
    }}
    
    .alert-error {{
        background-color: rgba(200, 90, 84, 0.1);
        border-color: {DESIGN_TOKENS["error"]};
        color: {DESIGN_TOKENS["error"]};
    }}
    
    .alert-success {{
        background-color: rgba(168, 213, 186, 0.1);
        border-color: {DESIGN_TOKENS["success"]};
        color: {DESIGN_TOKENS["success"]};
    }}
    
    /* STEP COUNTER */
    .step-number {{
        font-size: 72px;
        font-weight: 700;
        color: {DESIGN_TOKENS["secondary"]};
        opacity: 0.5;
        line-height: 1;
        margin-bottom: 16px;
    }}
    
    /* HORIZONTAL RULE */
    hr {{
        border: none;
        border-top: 1px solid {DESIGN_TOKENS["border"]};
        margin: 64px 0;
    }}
    
    /* SMOOTH ANIMATIONS */
    @keyframes fade-in {{
        from {{
            opacity: 0;
            transform: translateY(20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    .animate-in {{
        animation: fade-in 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    @keyframes pulse {{
        0%, 100% {{
            opacity: 1;
        }}
        50% {{
            opacity: 0.5;
        }}
    }}
    
    .pulse {{
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }}
    
    @keyframes shimmer {{
        0% {{
            background-position: -1000px 0;
        }}
        100% {{
            background-position: 1000px 0;
        }}
    }}
    
    .shimmer {{
        animation: shimmer 2s infinite;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        background-size: 1000px 100%;
    }}
    
    /* STREAMLIT OVERRIDES */
    .stButton > button {{
        width: 100%;
        border-radius: 24px;
        border: none;
        font-weight: 500;
        font-size: 16px;
        padding: 14px 28px;
        background-color: {DESIGN_TOKENS["primary"]};
        color: white !important;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        background-color: #0f3620;
        color: white !important;
        box-shadow: 0 8px 20px rgba(27, 77, 46, 0.15);
    }}
    
    .stButton > button p {{
        color: white !important;
    }}
    
    .stSelectbox {{
        border-radius: 12px;
    }}
    
    .stSelectbox [data-baseweb="select"] {{
        border-color: {DESIGN_TOKENS["border"]} !important;
    }}
    
    .stSelectbox [data-baseweb="select"]:hover {{
        border-color: {DESIGN_TOKENS["secondary"]} !important;
    }}
    
    .stFileUploader section {{
        padding: 0;
    }}
    
    .stFileUploader {{
        background-color: transparent;
    }}
    
    .stMetric {{
        background-color: {DESIGN_TOKENS["surface"]};
        padding: 24px;
        border-radius: 12px;
        border: 1px solid {DESIGN_TOKENS["border"]};
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        border-bottom: 1px solid {DESIGN_TOKENS["border"]};
    }}
    
    .stTabs [aria-selected="true"] {{
        border-color: {DESIGN_TOKENS["primary"]} !important;
        color: {DESIGN_TOKENS["primary"]};
    }}
    
    .stExpander {{
        border: 1px solid {DESIGN_TOKENS["border"]};
        border-radius: 12px;
        background-color: {DESIGN_TOKENS["surface"]};
    }}
    
    .stExpander > summary {{
        color: {DESIGN_TOKENS["primary"]};
        font-weight: 600;
    }}
    
    /* RESPONSIVE */
    @media (max-width: 768px) {{
        .section {{
            padding: 48px 20px;
        }}
        
        .section.hero {{
            padding: 60px 20px;
        }}
        
        .card {{
            padding: 24px;
        }}
        
        .result-card {{
            padding: 24px;
        }}
        
        .upload-zone {{
            padding: 40px 20px;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# INITIALIZE SESSION STATE
# ============================================================================

if "scan_history" not in st.session_state:
    st.session_state.scan_history = []
if "current_image" not in st.session_state:
    st.session_state.current_image = None
if "current_result" not in st.session_state:
    st.session_state.current_result = None
if "analyzing" not in st.session_state:
    st.session_state.analyzing = False
if "region" not in st.session_state:
    st.session_state.region = "Global"
if "show_scanner" not in st.session_state:
    st.session_state.show_scanner = False

# ============================================================================
# CONFIGURATION & API
# ============================================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    try:
        GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")
    except:
        pass

GROQ_MODEL = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")


REGIONS = {
    "Global": {
        "recyclable": ["Check with your local recycling authority for accepted materials."],
        "organic": ["Check if your area has composting programs."],
        "hazardous": ["Contact local hazardous waste facility for proper disposal."],
        "electronic": ["Use certified e-waste recycling centers."],
        "general": ["Place in regular trash if no other category applies."],
        "reusable": ["Consider donation to charity or resale platforms."]
    },
    "United States": {
        "recyclable": ["Most areas accept #1-7 plastics. Check your local program.", "Place in blue recycling bin or cart."],
        "organic": ["Check if your municipality offers green waste collection.", "Yard waste bins are common in many areas."],
        "hazardous": ["Contact your county hazardous waste facility.", "Never place in regular trash."],
        "electronic": ["Use Best Buy recycling program or local e-waste facility."],
        "general": ["Place in regular trash cart for landfill."],
        "reusable": ["Donate to Goodwill, Salvation Army, or similar."]
    },
    "Pakistan": {
        "recyclable": ["Contact local waste management authority.", "Separate recyclables for collection."],
        "organic": ["Composting programs are growing in major cities.", "Ask about community composting initiatives."],
        "hazardous": ["Contact provincial Environmental Protection Agency.", "Do not dispose in regular waste."],
        "electronic": ["Growing e-waste recycling programs in cities.", "Contact urban waste management office."],
        "general": ["Place in designated waste bin."],
        "reusable": ["Donate to communities or NGOs.", "Pakistan has active reuse networks."]
    },
    "United Kingdom": {
        "recyclable": ["Use your local council's kerbside collection.", "Black or blue bins for recycling (varies by area)."],
        "organic": ["Many areas offer food and garden waste collection.", "Check your council's scheme."],
        "hazardous": ["Take to Household Waste Recycling Centre.", "Never place in household waste."],
        "electronic": ["Take to Currys, John Lewis, or local HWRC.", "Extended Producer Responsibility programs available."],
        "general": ["Use your regular rubbish bin."],
        "reusable": ["Donate to charity shops.", "Use eBay, Vinted, or similar platforms."]
    },
    "Canada": {
        "recyclable": ["Place in blue recycling bin (varies by province).", "Check provincial recycling guidelines."],
        "organic": ["Many municipalities offer organic waste programs.", "Brown bins in some areas."],
        "hazardous": ["Contact provincial hazardous waste program.", "Do not place in regular trash."],
        "electronic": ["Use manufacturer take-back programs.", "Check Recyclepedia for local options."],
        "general": ["Place in regular garbage bin."],
        "reusable": ["Donate to Goodwill, Salvation Army, or Facebook Marketplace."]
    }
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def validate_image(image_file):
    """Validate uploaded image."""
    if image_file is None:
        return False, "No image provided."
    
    allowed_formats = {"jpg", "jpeg", "png", "webp"}
    file_ext = image_file.name.split(".")[-1].lower()
    
    if file_ext not in allowed_formats:
        return False, f"Unsupported format: {file_ext}. Please use JPG, PNG, or WEBP."
    
    if image_file.size > 10 * 1024 * 1024:
        return False, "Image too large. Please use an image under 10MB."
    
    return True, "Valid image."

def compress_image(image_file, max_width=1024, max_height=1024):
    """Compress image while maintaining quality."""
    try:
        img = Image.open(image_file)
        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        
        if img.mode == "RGBA":
            rgb_img = Image.new("RGB", img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[3] if len(img.split()) == 4 else None)
            img = rgb_img
        elif img.mode not in ("RGB", "L"):
            img = img.convert("RGB")
        
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format="JPEG", quality=85)
        img_byte_arr.seek(0)
        return img_byte_arr
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None

def encode_image_to_base64(image_file):
    """Encode image to base64 for API transmission."""
    try:
        image_file.seek(0)
        image_data = image_file.read()
        return base64.b64encode(image_data).decode("utf-8")
    except Exception as e:
        st.error(f"Error encoding image: {str(e)}")
        return None

def analyze_waste_with_groq(image_base64, region="Global"):
    """Send image to Groq and return guaranteed-valid JSON."""
    if not GROQ_API_KEY:
        return None, "Error: GROQ_API_KEY not configured. Please set it in environment variables or Streamlit secrets."

    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        prompt = f"""Analyze this waste item image for the {region} region.

Return ONLY a JSON object. Do not use Markdown or extra text.

Use exactly these fields:
{{
  "item": "short item name",
  "material": "short material description",
  "category": "Recyclable, Organic/Compostable, Hazardous, Electronic Waste, General/Residual, or Reusable",
  "confidence": "High, Medium, or Low",
  "reasoning": "one short sentence explaining the classification",
  "disposal_steps": ["short step 1", "short step 2", "short step 3"],
  "safety_warning": "short safety warning, or No major hazard identified.",
  "eco_tip": "one short practical eco tip",
  "reuse_suggestion": "short reuse idea, or empty string",
  "uncertainty": "short uncertainty note, or empty string"
}}

If the image is unclear, use Low confidence. Always prioritize safety for batteries, chemicals, medical waste, sharps, aerosols, unknown liquids, electrical components, toxic substances, and broken glass."""

        payload = {
            "model": GROQ_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            "temperature": 0.1,
            "max_completion_tokens": 700,
            "reasoning_format": "hidden",
            "reasoning_effort": "none",
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "waste_analysis",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "item": {"type": "string"},
                            "material": {"type": "string"},
                            "category": {"type": "string"},
                            "confidence": {"type": "string"},
                            "reasoning": {"type": "string"},
                            "disposal_steps": {"type": "array", "items": {"type": "string"}},
                            "safety_warning": {"type": "string"},
                            "eco_tip": {"type": "string"},
                            "reuse_suggestion": {"type": "string"},
                            "uncertainty": {"type": "string"}
                        },
                        "required": [
                            "item", "material", "category", "confidence", "reasoning",
                            "disposal_steps", "safety_warning", "eco_tip",
                            "reuse_suggestion", "uncertainty"
                        ],
                        "additionalProperties": False
                    }
                }
            }
        }

        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=30
        )

        if response.status_code != 200:
            error_detail = response.text
            if response.status_code == 401:
                return None, "Error: Invalid GROQ_API_KEY. Please verify your credentials."
            if response.status_code == 404:
                return None, f"Error: Vision model '{GROQ_MODEL}' not found."
            if response.status_code == 429:
                return None, "Groq rate limit reached. Please wait about 1 minute and try again."
            if response.status_code == 400:
                return None, f"Error: Groq rejected the request. {error_detail}"
            return None, f"API Error {response.status_code}: {error_detail}"

        response_data = response.json()
        choices = response_data.get("choices", [])

        if not choices:
            return None, "Error: Unexpected API response format."

        message = choices[0].get("message", {})
        content = message.get("content", "")

        if not content:
            return None, "Error: The AI returned an empty response."

        try:
            result = json.loads(content)
        except json.JSONDecodeError:
            # Fallback for any unexpected wrapper text.
            cleaned = content.strip()
            first_brace = cleaned.find("{")
            last_brace = cleaned.rfind("}")
            if first_brace == -1 or last_brace <= first_brace:
                return None, "Error: Could not parse AI response. Please try again."
            try:
                result = json.loads(cleaned[first_brace:last_brace + 1])
            except json.JSONDecodeError:
                return None, "Error: Could not parse AI response. Please try again."

        if not isinstance(result, dict):
            return None, "Error: AI returned an invalid result format. Please try again."

        defaults = {
            "item": "Unknown",
            "material": "Unknown",
            "category": "General/Residual",
            "confidence": "Low",
            "reasoning": "The AI could not provide a detailed explanation.",
            "disposal_steps": [],
            "safety_warning": "Use caution if the item may be hazardous.",
            "eco_tip": "Follow local waste-management guidance.",
            "reuse_suggestion": "",
            "uncertainty": "The result may be uncertain."
        }

        for key, default in defaults.items():
            if key not in result or result[key] is None:
                result[key] = default

        if not isinstance(result["disposal_steps"], list):
            result["disposal_steps"] = [str(result["disposal_steps"])]

        return result, None

    except requests.exceptions.Timeout:
        return None, "Error: API request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return None, "Error: Could not connect to Groq API. Please check your internet connection."
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"


def get_category_badge_class(category):
    """Get CSS class for category badge."""
    category_lower = category.lower()
    if "recyclable" in category_lower:
        return "badge-recyclable", "♻️"
    elif "organic" in category_lower or "compost" in category_lower:
        return "badge-organic", "🌱"
    elif "hazard" in category_lower:
        return "badge-hazardous", "⚠️"
    elif "electronic" in category_lower:
        return "badge-electronic", "🔌"
    elif "reusable" in category_lower:
        return "badge-reusable", "🔄"
    else:
        return "badge-general", "🗑️"

def get_confidence_class(confidence):
    """Get CSS class for confidence."""
    confidence_lower = confidence.lower()
    if "high" in confidence_lower:
        return "confidence-high"
    elif "medium" in confidence_lower:
        return "confidence-medium"
    else:
        return "confidence-low"

def format_region_key(category):
    """Format category for region lookup."""
    category_lower = category.lower().replace("/", "").replace(" ", "_")
    
    if "recyclable" in category_lower:
        return "recyclable"
    elif "organic" in category_lower or "compost" in category_lower:
        return "organic"
    elif "hazard" in category_lower:
        return "hazardous"
    elif "electronic" in category_lower:
        return "electronic"
    elif "reusable" in category_lower:
        return "reusable"
    else:
        return "general"




# ============================================================================
# NAVIGATION
# ============================================================================

def render_navbar():
    """Render premium navigation bar."""
    st.markdown(textwrap.dedent(f"""
<style>
.navbar {{
    position: sticky;
    top: 0;
    z-index: 1000;
    background-color: {DESIGN_TOKENS['background']};
    border-bottom: 1px solid {DESIGN_TOKENS['border']};
    padding: 24px 60px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
.navbar-logo {{
    font-size: 20px;
    font-weight: 700;
    color: {DESIGN_TOKENS['primary']};
    letter-spacing: -0.5px;
    text-decoration: none;
}}
.navbar-nav {{
    display: flex;
    gap: 48px;
    align-items: center;
}}
.navbar-link {{
    font-size: 14px;
    font-weight: 500;
    color: {DESIGN_TOKENS['text']};
    text-decoration: none;
    transition: color 0.3s ease;
    cursor: pointer;
    letter-spacing: 0.3px;
}}
.navbar-link:hover {{
    color: {DESIGN_TOKENS['primary']};
}}
.navbar-cta {{
    padding: 12px 24px;
    background-color: {DESIGN_TOKENS['primary']};
    color: white !important;
    border-radius: 20px;
    text-decoration: none;
    font-weight: 500;
    font-size: 14px;
    transition: all 0.3s ease;
    cursor: pointer;
    border: none;
}}
.navbar-cta:hover {{
    background-color: #0f3620;
    color: white !important;
    transform: translateY(-1px);
}}
@media (max-width: 768px) {{
    .navbar {{
        padding: 16px 20px;
    }}
    .navbar-nav {{
        display: none;
    }}
}}
</style>
<div class="navbar">
    <div class="navbar-logo">
        🌱 ECOSORT
    </div>
    <div class="navbar-nav">
        <a class="navbar-link" href="#how-it-works">How it Works</a>
        <a class="navbar-link" href="#categories">Waste Types</a>
        <a class="navbar-link" href="#impact">Impact</a>
        <a class="navbar-link" href="#about">About</a>
        <a class="navbar-cta" href="#scanner-section" style="text-decoration: none;">
            Scan Waste ↗
        </a>
    </div>
</div>
    """), unsafe_allow_html=True)

# ============================================================================
# HERO SECTION
# ============================================================================

def render_hero():
    """Render editorial hero section."""
    st.markdown(textwrap.dedent(f"""
<div class="section hero">
    <div style="max-width: 900px;">
        <h1 style="margin-bottom: 32px;">Sort smarter.<br>Waste less.</h1>
        <p class="subtitle" style="margin-bottom: 48px; max-width: 600px;">
            EcoSort uses AI to identify everyday waste and guide you toward the right disposal method.
            Make a real difference, one item at a time.
        </p>
        <div style="display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 80px;">
            <a href="#scanner-section" class="btn btn-primary" style="text-decoration: none;">
                Scan your waste ↗
            </a>
            <a href="#how-it-works" class="btn btn-secondary" style="text-decoration: none;">
                How it works
            </a>
        </div>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 20px; margin-top: 80px; padding-top: 60px; border-top: 1px solid {DESIGN_TOKENS['border']};">
        <div class="stat">
            <div class="stat-value">12,540+</div>
            <div class="stat-label">Items Classified</div>
        </div>
        <div class="stat">
            <div class="stat-value">8.2 kg</div>
            <div class="stat-label">Waste Sorted</div>
        </div>
        <div class="stat">
            <div class="stat-value">4.8 kg</div>
            <div class="stat-label">Potentially Recycled</div>
        </div>
    </div>
</div>
    """), unsafe_allow_html=True)

# ============================================================================
# MARQUEE SECTION
# ============================================================================

def render_marquee():
    """Render animated marquee."""
    st.markdown(textwrap.dedent(f"""
<div class="marquee-container">
    <div class="marquee">
        <span class="marquee-item">✓ ECOSORT</span>
        <span class="marquee-item">✓ SORT SMARTER</span>
        <span class="marquee-item">✓ RECYCLE BETTER</span>
        <span class="marquee-item">✓ BUILD A CLEANER FUTURE</span>
        <span class="marquee-item">✓ AI-POWERED WASTE</span>
        <span class="marquee-item">✓ ECOSORT</span>
        <span class="marquee-item">✓ SORT SMARTER</span>
        <span class="marquee-item">✓ RECYCLE BETTER</span>
        <span class="marquee-item">✓ BUILD A CLEANER FUTURE</span>
        <span class="marquee-item">✓ AI-POWERED WASTE</span>
    </div>
</div>
    """), unsafe_allow_html=True)

# ============================================================================
# HOW IT WORKS
# ============================================================================

def render_how_it_works():
    """Render how it works section."""
    html_content = textwrap.dedent("""
<div id="how-it-works" class="section">
    <h2 style="text-align: center; margin-bottom: 80px;">How EcoSort Works</h2>
    <div class="grid grid-3">
        <div>
            <div class="step-number">01</div>
            <h3 style="font-size: 28px; margin-bottom: 16px;">Upload</h3>
            <p class="body">
                Upload a photo of your waste item.
                Works with any household waste you're unsure about.
            </p>
        </div>
        <div>
            <div class="step-number">02</div>
            <h3 style="font-size: 28px; margin-bottom: 16px;">Analyze</h3>
            <p class="body">
                Our AI instantly identifies the material
                and waste category with high accuracy.
            </p>
        </div>
        <div>
            <div class="step-number">03</div>
            <h3 style="font-size: 28px; margin-bottom: 16px;">Sort</h3>
            <p class="body">
                Get clear, region-specific disposal
                recommendations immediately.
            </p>
        </div>
    </div>
</div>
    """)
    st.markdown(html_content, unsafe_allow_html=True)

# ============================================================================
# MAIN SCANNER SECTION
# ============================================================================

def render_scanner_section():
    """Render the main AI waste scanner interface."""
    st.markdown(textwrap.dedent(f"""
<div id="scanner-section" class="section" style="background-color: {DESIGN_TOKENS['surface']}; margin: 0 -60px; padding: 80px 60px;">
    <div style="max-width: 1200px; margin: 0 auto;">
        <div style="text-align: center; margin-bottom: 60px;">
            <h2 style="margin-bottom: 16px;">What are you throwing away?</h2>
            <p class="subtitle">Upload a photo and let EcoSort identify it.</p>
        </div>
    </div>
</div>
    """), unsafe_allow_html=True)

    # Main content container
    col1, col2 = st.columns([1.5, 1], gap="large")

    with col1:
        st.markdown(textwrap.dedent(f"""
<div style="padding: 0 20px;">
    <div class="upload-zone" style="text-align: center; padding: 60px 40px; border: 2px dashed {DESIGN_TOKENS['border']}; border-radius: 16px; background-color: {DESIGN_TOKENS['surface']}; cursor: pointer;">
        <p style="font-size: 32px; margin: 0 0 16px 0;">📸</p>
        <p style="font-size: 18px; font-weight: 600; color: {DESIGN_TOKENS['primary']}; margin: 0 0 8px 0;">
            Drop your waste image here
        </p>
        <p class="body-sm" style="margin: 0;">
            or click to browse. JPG, PNG, WEBP up to 10MB.
        </p>
    </div>
</div>
        """), unsafe_allow_html=True)

        uploaded_image = st.file_uploader(
            "Upload waste image",
            type=["jpg", "jpeg", "png", "webp"],
            label_visibility="collapsed",
            key="waste_image_uploader"
        )

        if uploaded_image is not None:
            is_valid, validation_msg = validate_image(uploaded_image)

            if is_valid:
                st.session_state.current_image = uploaded_image

                # Display uploaded image with caption
                st.markdown(textwrap.dedent(f"""
<div style="margin-top: 40px; border: 1px solid {DESIGN_TOKENS['border']}; border-radius: 12px; overflow: hidden;">
                """), unsafe_allow_html=True)
                st.image(uploaded_image, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

            else:
                st.markdown(textwrap.dedent(f"""
<div class="alert alert-error">
    <strong>Error:</strong> {validation_msg}
</div>
                """), unsafe_allow_html=True)

    with col2:
        st.markdown(textwrap.dedent(f"""
<div style="padding: 20px; background-color: {DESIGN_TOKENS['surface']}; border: 1px solid {DESIGN_TOKENS['border']}; border-radius: 12px; height: 100%;">
    <div style="margin-bottom: 32px;">
        <p class="body-sm" style="margin: 0 0 4px 0; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Region for Guidance</p>
        <p class="body-sm" style="margin: 0;">Select your location for relevant disposal methods.</p>
    </div>
        """), unsafe_allow_html=True)

        region = st.selectbox(
            "Region",
            options=list(REGIONS.keys()),
            index=0,
            label_visibility="collapsed"
        )
        st.session_state.region = region

        st.markdown("</div>", unsafe_allow_html=True)

    # Analysis button below
    if st.session_state.current_image:
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            if st.button("🔍 Analyze Waste", key="analyze_btn", use_container_width=True):
                st.session_state.analyzing = True

                with st.spinner(""):
                    # Show analyzing state
                    st.markdown(textwrap.dedent(f"""
<div class="section" style="text-align: center; padding: 60px 40px;">
    <div style="font-size: 48px; margin-bottom: 24px; animation: pulse 2s infinite;">
        🔄
    </div>
    <h3 style="margin-bottom: 16px;">Analyzing your waste</h3>
    <p class="body-sm" style="color: {DESIGN_TOKENS['text_muted']};">
        <span class="pulse" style="display: inline-block;">Identifying material • Checking characteristics • Determining disposal</span>
    </p>
</div>
                    """), unsafe_allow_html=True)

                    # Perform analysis
                    compressed_image = compress_image(st.session_state.current_image)
                    if compressed_image:
                        image_base64 = encode_image_to_base64(compressed_image)

                        if image_base64:
                            result, error = analyze_waste_with_groq(image_base64, st.session_state.region)

                            if error:
                                st.markdown(textwrap.dedent(f"""
<div class="alert alert-error">
    {error}
</div>
                                """), unsafe_allow_html=True)
                            elif result:
                                st.session_state.current_result = result
                                st.session_state.scan_history.append({
                                    "item": result.get("item", "Unknown"),
                                    "category": result.get("category", "Unknown"),
                                    "region": st.session_state.region
                                })
                                st.rerun()

                    st.session_state.analyzing = False

# ============================================================================
# CLASSIFICATION RESULT
# ============================================================================

def render_classification_result():
    """Render detailed classification result."""
    if not st.session_state.current_result:
        return

    result = st.session_state.current_result
    category = result.get("category", "Unknown")
    badge_class, emoji = get_category_badge_class(category)
    confidence = result.get("confidence", "Unknown")
    conf_class = get_confidence_class(confidence)

    st.markdown(textwrap.dedent(f"""
<div class="section">
    <div class="result-card">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 40px; margin-bottom: 40px;">
            <div class="result-item">
                <div class="result-label">Detected Item</div>
                <div class="result-value">{result.get('item', 'Unknown')}</div>
            </div>
            <div class="result-item">
                <div class="result-label">Category</div>
                <div><span class="category-badge {badge_class}">{emoji} {category}</span></div>
            </div>
            <div class="result-item">
                <div class="result-label">Confidence</div>
                <div class="result-value"><span class="{conf_class}">{confidence}</span></div>
            </div>
        </div>
        <div class="divider"></div>
        <div style="margin-bottom: 40px;">
            <p class="body-sm" style="margin: 0 0 12px 0; text-transform: uppercase; font-weight: 600; letter-spacing: 1px;">Material</p>
            <p class="body" style="margin: 0; font-weight: 500;">{result.get('material', 'Unknown')}</p>
        </div>
    """), unsafe_allow_html=True)

    # Reasoning
    if result.get("reasoning"):
        st.markdown(textwrap.dedent(f"""
<div style="margin-bottom: 40px; padding: 24px; background-color: {DESIGN_TOKENS['background']}; border-radius: 12px;">
    <p class="body-sm" style="margin: 0 0 12px 0; text-transform: uppercase; font-weight: 600; letter-spacing: 1px;">Why This Classification?</p>
    <p class="body" style="margin: 0;">{result.get('reasoning')}</p>
</div>
        """), unsafe_allow_html=True)

    # Disposal steps
    disposal_steps = result.get("disposal_steps", [])
    if disposal_steps:
        st.markdown(textwrap.dedent("""
<div style="margin-bottom: 40px;">
    <p class="body-sm" style="margin: 0 0 20px 0; text-transform: uppercase; font-weight: 600; letter-spacing: 1px;">📋 Disposal Steps</p>
        """), unsafe_allow_html=True)

        for i, step in enumerate(disposal_steps, 1):
            st.markdown(textwrap.dedent(f"""
<div style="display: flex; gap: 16px; margin-bottom: 16px;">
    <div style="flex-shrink: 0; width: 32px; height: 32px; background-color: {DESIGN_TOKENS['primary']}; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 14px;">{i}</div>
    <p class="body" style="margin: 4px 0;">{step}</p>
</div>
            """), unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # Regional guidance
    category_key = format_region_key(category)
    regional_guidance = REGIONS.get(st.session_state.region, {}).get(category_key, [])

    if regional_guidance:
        st.markdown(textwrap.dedent(f"""
<div style="margin-bottom: 40px; padding: 24px; background-color: rgba(107, 155, 126, 0.05); border-left: 4px solid {DESIGN_TOKENS['secondary']}; border-radius: 8px;">
    <p class="body-sm" style="margin: 0 0 16px 0; text-transform: uppercase; font-weight: 600; letter-spacing: 1px;">📍 Region-Specific Guidance</p>
        """), unsafe_allow_html=True)

        for guidance in regional_guidance:
            st.markdown(f'<p class="body" style="margin: 0 0 8px 0;">• {guidance}</p>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # Safety warning
    safety_warning = result.get("safety_warning", "")
    if safety_warning and "no major hazard" not in safety_warning.lower():
        st.markdown(textwrap.dedent(f"""
<div class="alert alert-warning">
    <strong>⚠️ Safety Warning</strong><br>
    {safety_warning}
</div>
        """), unsafe_allow_html=True)

    # Eco tip
    if result.get("eco_tip"):
        st.markdown(textwrap.dedent(f"""
<div class="alert alert-success">
    <strong>🌱 Eco Tip:</strong> {result.get('eco_tip')}
</div>
        """), unsafe_allow_html=True)

    # Reuse suggestion
    if result.get("reuse_suggestion"):
        st.markdown(textwrap.dedent(f"""
<div class="alert alert-info">
    <strong>🔄 Reuse Suggestion:</strong> {result.get('reuse_suggestion')}
</div>
        """), unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Scan again button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Scan Another Item", use_container_width=True, key="scan_again"):
            st.session_state.current_image = None
            st.session_state.current_result = None
            st.rerun()

# ============================================================================
# WASTE CATEGORIES SECTION
# ============================================================================

def render_waste_categories():
    """Render waste categories section."""
    st.markdown(textwrap.dedent(f"""
<div id="categories" class="section">
    <h2 style="text-align: center; margin-bottom: 20px;">Waste Categories</h2>
    <p class="subtitle" style="text-align: center; margin-bottom: 80px;">
        Understand the different types of waste and how to dispose of them responsibly.
    </p>
    <div class="grid grid-3">
    """), unsafe_allow_html=True)

    categories = [
        ("Plastic", "♻️", "Recyclable plastics, bottles, and containers. Check your local recycling program."),
        ("Paper", "📄", "Cardboard, paper, and paperboard. Usually accepted in recycling programs."),
        ("Glass", "🔷", "Glass bottles and jars. Separate by color when required by your program."),
        ("Metal", "⚙️", "Aluminum cans and steel containers. Highly valuable for recycling."),
        ("Organic", "🌱", "Food scraps and compostable materials. Consider composting programs."),
        ("E-Waste", "🔌", "Electronics and batteries. Requires specialized recycling facilities."),
    ]

    for title, emoji, description in categories:
        st.markdown(textwrap.dedent(f"""
<div class="card" style="text-align: center;">
    <div style="font-size: 48px; margin-bottom: 16px;">{emoji}</div>
    <h3 style="font-size: 20px; margin-bottom: 12px;">{title}</h3>
    <p class="body-sm" style="margin: 0; color: {DESIGN_TOKENS['text_muted']};">
        {description}
    </p>
</div>
        """), unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

# ============================================================================
# IMPACT SECTION
# ============================================================================

def render_impact_section():
    """Render impact statistics section."""
    st.markdown(textwrap.dedent(f"""
<div id="impact" class="section" style="background-color: {DESIGN_TOKENS['primary']}; margin: 0 -60px; padding: 80px 60px; color: white;">
    <div style="max-width: 1200px; margin: 0 auto;">
        <h2 style="text-align: center; color: white; margin-bottom: 80px;">
            Every Scan Creates Impact
        </h2>
        <div class="grid grid-3">
            <div class="stat" style="color: white;">
                <div class="stat-value" style="color: white;">{len(st.session_state.scan_history):,}+</div>
                <div class="stat-label" style="color: rgba(255,255,255,0.8);">Items Classified</div>
            </div>
            <div class="stat" style="color: white;">
                <div class="stat-value" style="color: white;">98%</div>
                <div class="stat-label" style="color: rgba(255,255,255,0.8);">AI Accuracy</div>
            </div>
            <div class="stat" style="color: white;">
                <div class="stat-value" style="color: white;">15+</div>
                <div class="stat-label" style="color: rgba(255,255,255,0.8);">Waste Categories</div>
            </div>
        </div>
        <div style="margin-top: 80px; padding-top: 80px; border-top: 1px solid rgba(255,255,255,0.2); text-align: center;">
            <p class="subtitle" style="color: rgba(255,255,255,0.9); margin-bottom: 24px;">
                Contribute to a more sustainable future, one scan at a time.
            </p>
            <a href="#scanner-section" class="btn btn-secondary" style="background-color: {DESIGN_TOKENS['primary']}; color: white !important; border: none; text-decoration: none; display: inline-flex;">
                Start Sorting Today ↗
            </a>
        </div>
    </div>
</div>
    """), unsafe_allow_html=True)

# ============================================================================
# WHY ECOSORT SECTION
# ============================================================================

def render_why_ecosort():
    """Render benefits section."""
    st.markdown(textwrap.dedent(f"""
<div id="about" class="section">
    <h2 style="text-align: center; margin-bottom: 80px;">Why EcoSort?</h2>
    <div class="grid grid-2">
        <div>
            <div style="font-size: 32px; margin-bottom: 16px;">🤖</div>
            <h3 style="font-size: 24px; margin-bottom: 12px;">AI-Powered Classification</h3>
            <p class="body" style="color: {DESIGN_TOKENS['text_muted']};">
                Advanced computer vision technology identifies waste items with high accuracy. Learn what materials items are made from instantly.
            </p>
        </div>
        <div>
            <div style="font-size: 32px; margin-bottom: 16px;">🌍</div>
            <h3 style="font-size: 24px; margin-bottom: 12px;">Region-Specific Guidance</h3>
            <p class="body" style="color: {DESIGN_TOKENS['text_muted']};">
                Get tailored disposal recommendations based on your location. Understand local programs and requirements for proper waste management.
            </p>
        </div>
        <div>
            <div style="font-size: 32px; margin-bottom: 16px;">📚</div>
            <h3 style="font-size: 24px; margin-bottom: 12px;">Learn as You Sort</h3>
            <p class="body" style="color: {DESIGN_TOKENS['text_muted']};">
                Build waste literacy over time. Understand sustainability principles and make better choices with every scan.
            </p>
        </div>
        <div>
            <div style="font-size: 32px; margin-bottom: 16px;">📊</div>
            <h3 style="font-size: 24px; margin-bottom: 12px;">Track Your Impact</h3>
            <p class="body" style="color: {DESIGN_TOKENS['text_muted']};">
                View your scanning history and understand your contribution to waste reduction. See the real environmental impact of better sorting.
            </p>
        </div>
    </div>
</div>
    """), unsafe_allow_html=True)

# ============================================================================
# FINAL CTA SECTION
# ============================================================================

def render_final_cta():
    """Render final call-to-action section."""
    st.markdown(textwrap.dedent(f"""
<div class="section" style="text-align: center;">
    <h2 style="margin-bottom: 32px; max-width: 800px; margin-left: auto; margin-right: auto;">
        Every piece of waste<br>has somewhere to go.
    </h2>
    <p class="subtitle" style="margin-bottom: 48px; max-width: 600px; margin-left: auto; margin-right: auto;">
        Make the next one the right place.
    </p>
    <a href="#scanner-section" class="btn btn-primary" style="text-decoration: none; display: inline-flex;">
        Start Sorting ↗
    </a>
</div>
    """), unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

def render_footer():
    """Render minimal footer."""
    st.markdown(textwrap.dedent(f"""
<div style="background-color: {DESIGN_TOKENS['primary']}; color: white; padding: 60px; margin-top: 120px;">
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 60px; margin-bottom: 60px; max-width: 1200px; margin-left: auto; margin-right: auto;">
        <div>
            <div style="font-weight: 700; font-size: 16px; margin-bottom: 16px;">🌱 EcoSort</div>
            <p style="font-size: 14px; color: rgba(255,255,255,0.7); line-height: 1.6;">
                AI-powered waste classification for a more sustainable future.
            </p>
        </div>
        <div>
            <div style="font-weight: 600; font-size: 14px; margin-bottom: 16px; letter-spacing: 0.5px; text-transform: uppercase;">Navigation</div>
            <ul style="list-style: none; padding: 0; margin: 0;">
                <li><a href="#" style="color: rgba(255,255,255,0.7); text-decoration: none; font-size: 14px;">How it Works</a></li>
                <li><a href="#" style="color: rgba(255,255,255,0.7); text-decoration: none; font-size: 14px;">Categories</a></li>
                <li><a href="#" style="color: rgba(255,255,255,0.7); text-decoration: none; font-size: 14px;">Impact</a></li>
                <li><a href="#" style="color: rgba(255,255,255,0.7); text-decoration: none; font-size: 14px;">About</a></li>
            </ul>
        </div>
        <div>
            <div style="font-weight: 600; font-size: 14px; margin-bottom: 16px; letter-spacing: 0.5px; text-transform: uppercase;">Social</div>
            <ul style="list-style: none; padding: 0; margin: 0;">
                <li><a href="#" style="color: rgba(255,255,255,0.7); text-decoration: none; font-size: 14px;">Twitter</a></li>
                <li><a href="#" style="color: rgba(255,255,255,0.7); text-decoration: none; font-size: 14px;">Instagram</a></li>
                <li><a href="#" style="color: rgba(255,255,255,0.7); text-decoration: none; font-size: 14px;">LinkedIn</a></li>
            </ul>
        </div>
    </div>
    <div style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 40px; text-align: center; color: rgba(255,255,255,0.6); font-size: 12px;">
        <p style="margin: 0;">© 2024 EcoSort. All rights reserved. Committed to sustainability.</p>
    </div>
</div>
    """), unsafe_allow_html=True)

# ============================================================================
# MAIN APP LAYOUT
# ============================================================================

def main():
    """Main application layout."""
    render_navbar()
    render_hero()
    render_marquee()
    render_how_it_works()
    render_scanner_section()
    
    if st.session_state.current_result:
        render_classification_result()
    
    render_waste_categories()
    render_impact_section()
    render_why_ecosort()
    render_final_cta()
    render_footer()

if __name__ == "__main__":
    main()
