import streamlit as st
import requests
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, KeepTogether
from reportlab.lib.styles import ParagraphStyle

# ══════════════════════════════════════════════════════════════════════════════
# THEMES
# ══════════════════════════════════════════════════════════════════════════════
THEMES = {
    "light": {
        "bg":           "#F7F8FC",
        "bg2":          "#FFFFFF",
        "bg3":          "#EEF0F6",
        "border":       "#E2E4EE",
        "border2":      "#CDD0E0",
        "text":         "#0D0D1A",
        "muted":        "#4A4A66",
        "label":        "#9090AA",
        "label2":       "#6B6B88",
        "accent":       "#1A1A2E",
        "accent_bg":    "rgba(26,26,46,0.06)",
        "accent_brd":   "rgba(26,26,46,0.15)",
        "accent_hov":   "#2A2A4E",
        "btn_text":     "#FFFFFF",
        "error_bg":     "#FFF0F0",
        "error_brd":    "#FFCCCC",
        "error_text":   "#CC2222",
        "card_text":    "#2A2A3E",
        "scrollbar":    "#CDD0E0",
        "hero_title":   "#0D0D1A",
        "hero_accent":  "#1A1A2E",
        "hero_sub":     "#6B6B88",
        "eyebrow":      "#6B6B88",
        "divider":      "#E2E4EE",
        "toggle_icon":  "🌙",
        "shadow":       "0 1px 3px rgba(0,0,0,0.08)",
    },
    "dark": {
        "bg":           "#0A0A0F",
        "bg2":          "#0E0E16",
        "bg3":          "#141420",
        "border":       "#1E1E28",
        "border2":      "#2A2A38",
        "text":         "#E8E6E0",
        "muted":        "#8888A0",
        "label":        "#444458",
        "label2":       "#666672",
        "accent":       "#C8F04B",
        "accent_bg":    "rgba(200,240,75,0.07)",
        "accent_brd":   "rgba(200,240,75,0.18)",
        "accent_hov":   "#D4F562",
        "btn_text":     "#0A0A0F",
        "error_bg":     "rgba(255,75,75,0.07)",
        "error_brd":    "rgba(255,75,75,0.18)",
        "error_text":   "#FF8888",
        "card_text":    "#AAAAB8",
        "scrollbar":    "#2A2A38",
        "hero_title":   "#E8E6E0",
        "hero_accent":  "#C8F04B",
        "hero_sub":     "#8888A0",
        "eyebrow":      "#C8F04B",
        "divider":      "#1E1E28",
        "toggle_icon":  "☀️",
        "shadow":       "none",
    },
}

def get_css(t):
    return f"""<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {{
    background-color: {t["bg"]} !important;
    color: {t["text"]} !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}}
#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] {{ display: none !important; }}
.block-container {{ padding: 0 !important; max-width: 100% !important; }}
.doclens-logo {{ font-weight: 800; font-size: 22px; color: {t["text"]}; }}
.doclens-logo span {{ color: {t["accent"]}; }}

/* ── Inputs ── */
[data-testid="stTextInput"] input {{
    background: {t["bg2"]} !important;
    border: 1.5px solid {t["border"]} !important;
    border-radius: 8px !important;
    color: {t["text"]} !important;
    font-size: 14px !important;
    padding: 12px 16px !important;
    box-shadow: {t["shadow"]} !important;
}}
[data-testid="stTextInput"] input:focus {{
    border-color: {t["accent"]} !important;
    box-shadow: 0 0 0 3px {t["accent_bg"]} !important;
}}
[data-testid="stTextInput"] input::placeholder {{ color: {t["label"]} !important; }}
[data-testid="stTextInput"] label {{
    color: {t["label2"]} !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
}}

/* ── Primary button ── */
[data-testid="stButton"] button[kind="primary"] {{
    background: {t["accent"]} !important;
    color: {t["btn_text"]} !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    padding: 13px 28px !important;
    width: 100% !important;
    transition: background 0.15s !important;
}}
[data-testid="stButton"] button[kind="primary"]:hover {{
    background: {t["accent_hov"]} !important;
}}

/* ── Secondary button ── */
[data-testid="stButton"] button[kind="secondary"] {{
    background: {t["bg2"]} !important;
    color: {t["muted"]} !important;
    border: 1.5px solid {t["border"]} !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    padding: 10px 16px !important;
    width: 100% !important;
    box-shadow: {t["shadow"]} !important;
}}
[data-testid="stButton"] button[kind="secondary"]:hover {{
    border-color: {t["accent"]} !important;
    color: {t["text"]} !important;
}}

/* ── File uploader ── */
[data-testid="stFileUploaderDropzone"] {{
    background: {t["bg2"]} !important;
    border: 2px dashed {t["border2"]} !important;
    border-radius: 12px !important;
    padding: 32px 24px !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    gap: 12px !important;
    box-shadow: {t["shadow"]} !important;
}}
[data-testid="stFileUploaderDropzone"]:hover {{ border-color: {t["accent"]} !important; }}
[data-testid="stFileUploaderDropzoneInstructions"] {{
    color: {t["muted"]} !important;
    font-size: 13.5px !important;
    text-align: center !important;
    pointer-events: none !important;
}}
[data-testid="stFileUploaderDropzoneInstructions"] span {{ color: {t["muted"]} !important; }}
[data-testid="stFileUploaderDropzone"] button {{
    background: {t["accent"]} !important;
    color: {t["btn_text"]} !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    padding: 8px 20px !important;
    position: static !important;
    display: block !important;
    width: auto !important;
}}

/* ── Radio ── */
[data-testid="stRadio"] > div {{
    gap: 8px !important;
}}
[data-testid="stRadio"] label {{
    background: {t["bg2"]} !important;
    border: 1.5px solid {t["border"]} !important;
    border-radius: 8px !important;
    padding: 8px 18px !important;
    color: {t["text"]} !important;
    font-size: 13px !important;
    cursor: pointer !important;
    box-shadow: {t["shadow"]} !important;
}}
[data-testid="stRadio"] label:has(input:checked) {{
    border-color: {t["accent"]} !important;
    background: {t["accent_bg"]} !important;
    color: {t["accent"]} !important;
}}
[data-testid="stRadio"] [data-testid="stMarkdownContainer"] p {{
    color: {t["text"]} !important;
    font-size: 13px !important;
}}
[data-testid="stRadio"] [data-testid="stMarkdownContainer"] {{
    color: {t["text"]} !important;
}}
[data-testid="stRadio"] span {{
    color: {t["text"]} !important;
}}
[data-testid="stRadio"] [data-baseweb="radio"] > div:first-child {{
    display: none !important;
}}

/* ── Download button ── */
[data-testid="stDownloadButton"] button {{
    background: {t["bg2"]} !important;
    color: {t["accent"]} !important;
    border: 1.5px solid {t["accent_brd"]} !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    width: 100% !important;
    box-shadow: {t["shadow"]} !important;
}}
[data-testid="stDownloadButton"] button:hover {{
    background: {t["accent_bg"]} !important;
    border-color: {t["accent"]} !important;
}}

/* ── Cards ── */
.output-card {{
    background: {t["bg2"]}; border: 1.5px solid {t["border"]};
    border-radius: 12px; padding: 24px 28px; margin-bottom: 14px;
    box-shadow: {t["shadow"]};
}}
.output-card-label {{
    font-size: 10px; font-weight: 700; letter-spacing: 2.5px;
    text-transform: uppercase; color: {t["accent"]}; margin-bottom: 12px;
}}
.output-body {{ font-size: 15px; line-height: 1.7; color: {t["card_text"]}; }}
.bullet-item {{
    display: flex; gap: 12px; padding: 9px 0;
    border-bottom: 1px solid {t["border"]}; align-items: flex-start;
}}
.bullet-item:last-child {{ border-bottom: none; }}
.bullet-dot {{ width: 6px; height: 6px; border-radius: 50%; background: {t["accent"]}; flex-shrink: 0; margin-top: 8px; }}
.bullet-text {{ font-size: 14px; line-height: 1.6; color: {t["card_text"]}; }}
.meta-row {{ display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 24px; }}
.meta-pill {{ font-size: 12px; color: {t["label2"]}; background: {t["bg3"]}; border: 1px solid {t["border"]}; border-radius: 20px; padding: 4px 13px; }}
.meta-pill.accent {{ color: {t["accent"]}; background: {t["accent_bg"]}; border-color: {t["accent_brd"]}; }}
.empty-state {{
    background: {t["bg2"]}; border: 1.5px dashed {t["border2"]};
    border-radius: 12px; padding: 60px 32px; text-align: center;
}}
.empty-icon {{ font-size: 36px; margin-bottom: 16px; opacity: 0.25; }}
.empty-title {{ font-weight: 700; font-size: 16px; color: {t["label2"]}; margin-bottom: 8px; }}
.empty-sub {{ font-size: 13px; color: {t["label"]}; }}
.panel-label {{
    font-size: 10px; font-weight: 700; letter-spacing: 2px;
    text-transform: uppercase; color: {t["label"]}; margin-bottom: 16px;
}}
.selected-cat-label {{ font-size: 12.5px; color: {t["accent"]}; margin-bottom: 6px; font-weight: 500; }}
.section-divider {{ height: 1px; background: {t["divider"]}; margin: 0 56px 48px; }}
.stat-card {{
    background: {t["bg2"]}; border: 1.5px solid {t["border"]};
    border-radius: 12px; padding: 20px 24px; box-shadow: {t["shadow"]};
}}
.stat-number {{ font-weight: 800; font-size: 36px; color: {t["accent"]}; line-height: 1; }}
.stat-label {{ font-size: 11px; color: {t["label"]}; margin-top: 6px; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }}
.history-row {{
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 20px; background: {t["bg2"]};
    border: 1px solid {t["border"]}; border-radius: 10px; margin-bottom: 8px;
    box-shadow: {t["shadow"]};
}}
.history-filename {{ font-size: 14px; color: {t["text"]}; font-weight: 500; }}
.history-meta {{ font-size: 12px; color: {t["label"]}; margin-top: 3px; }}
.history-badge {{ font-size: 11px; color: {t["accent"]}; background: {t["accent_bg"]}; border: 1px solid {t["accent_brd"]}; border-radius: 20px; padding: 3px 10px; font-weight: 600; }}
.auth-card {{
    background: {t["bg2"]}; border: 1.5px solid {t["border"]};
    border-radius: 16px; padding: 40px 40px 36px; box-shadow: {t["shadow"]};
}}
.auth-title {{ font-weight: 800; font-size: 26px; letter-spacing: -0.5px; color: {t["text"]}; margin-bottom: 6px; }}
.auth-sub {{ font-size: 14px; color: {t["label2"]}; margin-bottom: 28px; line-height: 1.5; }}
.auth-divider {{ display: flex; align-items: center; gap: 12px; margin: 20px 0; color: {t["label"]}; font-size: 12px; }}
.auth-divider::before, .auth-divider::after {{ content: ''; flex: 1; height: 1px; background: {t["border"]}; }}
.error-msg {{ background: {t["error_bg"]}; border: 1px solid {t["error_brd"]}; border-radius: 8px; padding: 10px 14px; font-size: 13px; color: {t["error_text"]}; margin-bottom: 12px; }}
.success-msg {{ background: {t["accent_bg"]}; border: 1px solid {t["accent_brd"]}; border-radius: 8px; padding: 10px 14px; font-size: 13px; color: {t["accent"]}; margin-bottom: 12px; }}

::-webkit-scrollbar {{ width: 4px; }}
::-webkit-scrollbar-track {{ background: {t["bg"]}; }}
::-webkit-scrollbar-thumb {{ background: {t["scrollbar"]}; border-radius: 4px; }}
</style>"""


# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="DocLens",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
defaults = {
    "page":               "login",
    "user":               None,
    "selected_category":  None,
    "selected_detail":    "Detailed",
    "result":             None,
    "history":            [],
    "auth_error":         "",
    "auth_success":       "",
    "theme":              "light",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Inject CSS based on current theme
t = THEMES[st.session_state.theme]
st.markdown(get_css(t), unsafe_allow_html=True)

BASE_URL = "http://127.0.0.1:8000"
if "http_session" not in st.session_state:
    st.session_state.http_session = requests.Session()


# ══════════════════════════════════════════════════════════════════════════════
# PDF GENERATOR
# ══════════════════════════════════════════════════════════════════════════════
def generate_pdf_report(r: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm, topMargin=18*mm, bottomMargin=18*mm)

    INK        = colors.HexColor("#111118")
    SUBTEXT    = colors.HexColor("#555566")
    LIME_DARK  = colors.HexColor("#4A7C00")
    LIME_BG    = colors.HexColor("#F2FAD8")
    BLUE_DARK  = colors.HexColor("#2D3A8C")
    BLUE_BG    = colors.HexColor("#EEF0FA")
    AMBER_DARK = colors.HexColor("#7A4A00")
    AMBER_BG   = colors.HexColor("#FDF3E3")
    RULE       = colors.HexColor("#DDDDEE")
    HEADER_BG  = colors.HexColor("#111118")
    page_w     = A4[0] - 40*mm

    logo_s        = ParagraphStyle("logo",     fontName="Helvetica-Bold", fontSize=17, textColor=colors.white)
    badge_s       = ParagraphStyle("badge",    fontName="Helvetica", fontSize=7, textColor=colors.HexColor("#AAAACC"), alignment=2, leading=10)
    eyebrow_s     = ParagraphStyle("eyebrow",  fontName="Helvetica", fontSize=7.5, textColor=LIME_DARK, spaceAfter=5, letterSpacing=1.5)
    title_s       = ParagraphStyle("title",    fontName="Helvetica-Bold", fontSize=22, textColor=INK, spaceAfter=5, leading=28)
    meta_s        = ParagraphStyle("meta",     fontName="Helvetica", fontSize=8, textColor=SUBTEXT, spaceAfter=0)
    card_lbl_lime = ParagraphStyle("cl_lime",  fontName="Helvetica-Bold", fontSize=7.5, textColor=LIME_DARK,  spaceAfter=7, letterSpacing=1.5)
    card_lbl_blue = ParagraphStyle("cl_blue",  fontName="Helvetica-Bold", fontSize=7.5, textColor=BLUE_DARK,  spaceAfter=7, letterSpacing=1.5)
    card_lbl_amb  = ParagraphStyle("cl_amber", fontName="Helvetica-Bold", fontSize=7.5, textColor=AMBER_DARK, spaceAfter=7, letterSpacing=1.5)
    body_s        = ParagraphStyle("body",     fontName="Helvetica", fontSize=10, textColor=INK, leading=16, spaceAfter=0)
    bullet_s      = ParagraphStyle("bullet",   fontName="Helvetica", fontSize=10, textColor=INK, leading=15, spaceAfter=4, leftIndent=10)
    footer_s      = ParagraphStyle("footer",   fontName="Helvetica", fontSize=7, textColor=SUBTEXT, alignment=1)

    story = []
    hdr = Table([[Paragraph("DocLens", logo_s), Paragraph("AI DOCUMENT INTELLIGENCE<br/>Smart Summarization Report", badge_s)]], colWidths=[page_w*0.55, page_w*0.45])
    hdr.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),HEADER_BG),("TOPPADDING",(0,0),(-1,-1),12),("BOTTOMPADDING",(0,0),(-1,-1),12),("LEFTPADDING",(0,0),(0,-1),14),("RIGHTPADDING",(-1,0),(-1,-1),14),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    story += [hdr, Spacer(1,8*mm), Paragraph("ANALYSIS REPORT  -  SMART SUMMARIZATION", eyebrow_s), Paragraph(f"Summary of {r['file_name']}", title_s), Paragraph(f"Domain: {r['category']}    Style: {r['detail_level']}", meta_s), Spacer(1,4*mm), HRFlowable(width="100%", thickness=0.75, color=RULE, spaceAfter=6*mm)]

    story.append(KeepTogether([Paragraph("EXECUTIVE SUMMARY", card_lbl_lime), Table([[Paragraph(r["executive_summary"], body_s)]], colWidths=[page_w], style=TableStyle([("BACKGROUND",(0,0),(-1,-1),LIME_BG),("LEFTPADDING",(0,0),(-1,-1),14),("RIGHTPADDING",(0,0),(-1,-1),14),("TOPPADDING",(0,0),(-1,-1),12),("BOTTOMPADDING",(0,0),(-1,-1),12),("LINEBELOW",(0,0),(-1,-1),2,LIME_DARK)])), Spacer(1,5*mm)]))
    kp_paras = [Paragraph(f"- {pt}", bullet_s) for pt in r["key_points"]]
    story.append(KeepTogether([Paragraph("KEY POINTS", card_lbl_lime), Table([[kp_paras]], colWidths=[page_w], style=TableStyle([("BACKGROUND",(0,0),(-1,-1),LIME_BG),("LEFTPADDING",(0,0),(-1,-1),14),("RIGHTPADDING",(0,0),(-1,-1),14),("TOPPADDING",(0,0),(-1,-1),12),("BOTTOMPADDING",(0,0),(-1,-1),12),("LINEBELOW",(0,0),(-1,-1),2,LIME_DARK)])), Spacer(1,5*mm)]))
    col_w = (page_w - 5*mm) / 2
    ai_p = [Paragraph("ACTION ITEMS", card_lbl_blue)] + [Paragraph(f"- {a}", bullet_s) for a in r["action_items"]]
    dh_p = [Paragraph("DATA HIGHLIGHTS", card_lbl_amb)] + [Paragraph(f"- {d}", bullet_s) for d in r["data_highlights"]]
    side = Table([[ai_p, dh_p]], colWidths=[col_w, col_w])
    side.setStyle(TableStyle([("BACKGROUND",(0,0),(0,-1),BLUE_BG),("BACKGROUND",(1,0),(1,-1),AMBER_BG),("LEFTPADDING",(0,0),(-1,-1),14),("RIGHTPADDING",(0,0),(-1,-1),14),("TOPPADDING",(0,0),(-1,-1),12),("BOTTOMPADDING",(0,0),(-1,-1),12),("LINEBELOW",(0,0),(0,-1),2,BLUE_DARK),("LINEBELOW",(1,0),(1,-1),2,AMBER_DARK)]))
    story += [side, Spacer(1,10*mm), HRFlowable(width="100%", thickness=0.5, color=RULE, spaceAfter=3*mm), Paragraph("Generated by DocLens  -  AI Document Intelligence", footer_s)]
    doc.build(story)
    buffer.seek(0)
    return buffer.read()


# ══════════════════════════════════════════════════════════════════════════════
# API FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════
def api_login(email, password):
    if not email or not password:
        raise ValueError("Please fill in all fields.")
    r = st.session_state.http_session.post(f"{BASE_URL}/api/users/login/", json={"email": email, "password": password})
    data = r.json()
    if r.status_code == 200:
        name = f"{data.get('first_name','')} {data.get('last_name','')}".strip() or data.get('user_name', email.split('@')[0])
        return {"name": name, "email": data.get("email_id", email)}
    raise ValueError(data.get("detail", "Login failed."))

def api_signup(name, email, password, confirm):
    if not name or not email or not password or not confirm:
        raise ValueError("Please fill in all fields.")
    if len(password) < 6:
        raise ValueError("Password must be at least 6 characters.")
    if password != confirm:
        raise ValueError("Passwords do not match.")
    parts = name.strip().split(" ", 1)
    r = st.session_state.http_session.post(f"{BASE_URL}/api/users/register/", json={"first_name": parts[0], "last_name": parts[1] if len(parts)>1 else parts[0], "user_name": email.split("@")[0].replace(".","_").lower(), "email_id": email, "password": password})
    data = r.json()
    if r.status_code == 201:
        return {"name": name, "email": email}
    messages = []
    for field, errors in data.items() if isinstance(data, dict) else []:
        messages.append(errors[0] if isinstance(errors, list) else str(errors))
    raise ValueError(" ".join(messages) or "Registration failed.")

def api_summarize(file_name, category, detail_level, uploaded_file):
    csrf = st.session_state.http_session.cookies.get("csrftoken", "")
    uploaded_file.seek(0)
    resp = st.session_state.http_session.post(f"{BASE_URL}/api/documents/upload/", files={"file": (uploaded_file.name, uploaded_file, "application/octet-stream")}, headers={"X-CSRFToken": csrf, "Referer": BASE_URL})
    if resp.status_code != 201:
        raise ValueError(resp.json().get("detail", "Upload failed."))
    doc = resp.json()
    if doc.get("parse_status") == "failed":
        raise ValueError(f"Parsing failed: {doc.get('parse_error','Unknown error')}")
    lines = [l.strip() for l in doc.get("parsed_text","").splitlines() if l.strip()]
    key_points = [l[:120] for l in lines if len(l) > 30][:5] or ["Document parsed successfully."]
    return {
        "executive_summary": f"This {category.lower()} document was parsed and contains {len(lines)} lines of content. Analysis at '{detail_level}' depth. Full AI summarization available once Ollama is connected.",
        "key_points": key_points,
        "action_items": ["Review the parsed content for accuracy", "Connect Ollama to enable full AI summarization"],
        "data_highlights": [f"Lines extracted: {len(lines)}", f"File type: {doc.get('file_type','unknown').upper()}", f"File size: {round(doc.get('file_size',0)/1024,1)} KB", f"Doc ID: {str(doc.get('document_id',''))[:8]}..."],
        "category": category, "detail_level": detail_level, "file_name": file_name,
    }


# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
def render_header(show_nav=True):
    th = THEMES[st.session_state.theme]
    if show_nav and st.session_state.user:
        h1, h2 = st.columns([1,1])
        with h1:
            st.markdown(f"""<div style="padding:22px 0 18px 56px;border-bottom:1px solid {th['divider']};">
                <span class="doclens-logo">Doc<span>Lens</span></span></div>""", unsafe_allow_html=True)
        with h2:
            st.markdown(f"""<div style="padding:22px 56px 18px 0;border-bottom:1px solid {th['divider']};
                display:flex;align-items:center;justify-content:flex-end;gap:10px;">
                <span style="font-size:13px;color:{th['label2']};">{st.session_state.user['name']}</span>
                </div>""", unsafe_allow_html=True)
        n1, n2, n3, n4, n5 = st.columns([2.5, 1, 1, 0.5, 1])
        with n2:
            if st.button("Dashboard", key="nav_dash", use_container_width=True): st.session_state.page="dashboard"; st.rerun()
        with n3:
            if st.button("Analyser", key="nav_analyser", use_container_width=True): st.session_state.page="analyser"; st.rerun()
        with n4:
            if st.button(th["toggle_icon"], key="theme_toggle", use_container_width=True):
                st.session_state.theme = "dark" if st.session_state.theme=="light" else "light"; st.rerun()
        with n5:
            if st.button("Sign Out", key="nav_signout", use_container_width=True):
                for k in list(st.session_state.keys()): del st.session_state[k]
                st.rerun()
    else:
        h1, h2, h3 = st.columns([3, 2, 0.4])
        with h1:
            st.markdown(f"""<div style="padding:22px 0 18px 56px;border-bottom:1px solid {th['divider']};">
                <span class="doclens-logo">Doc<span>Lens</span></span></div>""", unsafe_allow_html=True)
        with h2:
            st.markdown(f"""<div style="padding:22px 0 18px;border-bottom:1px solid {th['divider']};
                display:flex;align-items:center;justify-content:flex-end;">
                <span style="font-size:11px;font-weight:500;letter-spacing:1.5px;text-transform:uppercase;
                color:{th['label']};border:1px solid {th['border']};padding:5px 12px;border-radius:20px;">
                AI Document Intelligence</span></div>""", unsafe_allow_html=True)
        with h3:
            st.markdown(f'<div style="padding:16px 0 12px;border-bottom:1px solid {th["divider"]};"></div>', unsafe_allow_html=True)
            if st.button(th["toggle_icon"], key="theme_toggle_auth", use_container_width=True):
                st.session_state.theme = "dark" if st.session_state.theme=="light" else "light"; st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════════════════════════════
def page_login():
    render_header(show_nav=False)
    _, mid, _ = st.columns([1, 1.1, 1])
    with mid:
        st.markdown("<div style='height:52px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="auth-card"><div class="auth-title">Welcome back</div><div class="auth-sub">Sign in to access your documents and summaries.</div></div>', unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.session_state.auth_error:
            st.markdown(f'<div class="error-msg">&#x26A0; {st.session_state.auth_error}</div>', unsafe_allow_html=True)
        if st.session_state.auth_success:
            st.markdown(f'<div class="success-msg">&#x2713; {st.session_state.auth_success}</div>', unsafe_allow_html=True)
        email    = st.text_input("Email", placeholder="you@example.com", key="login_email")
        password = st.text_input("Password", placeholder="Enter your password", type="password", key="login_password")
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        if st.button("Sign In", type="primary", key="login_btn", use_container_width=True):
            try:
                user = api_login(email, password)
                st.session_state.user = user; st.session_state.auth_error = ""; st.session_state.page = "dashboard"; st.rerun()
            except Exception as e:
                st.session_state.auth_error = str(e); st.rerun()
        st.markdown('<div class="auth-divider">or</div>', unsafe_allow_html=True)
        if st.button("Create an account", key="goto_signup", use_container_width=True):
            st.session_state.auth_error = ""; st.session_state.page = "signup"; st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# SIGNUP
# ══════════════════════════════════════════════════════════════════════════════
def page_signup():
    render_header(show_nav=False)
    _, mid, _ = st.columns([1, 1.1, 1])
    with mid:
        st.markdown("<div style='height:52px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="auth-card"><div class="auth-title">Create account</div><div class="auth-sub">Join DocLens. Your documents stay private to you.</div></div>', unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.session_state.auth_error:
            st.markdown(f'<div class="error-msg">&#x26A0; {st.session_state.auth_error}</div>', unsafe_allow_html=True)
        name     = st.text_input("Full Name", placeholder="Dev Aggarwal", key="signup_name")
        email    = st.text_input("Email", placeholder="you@example.com", key="signup_email")
        password = st.text_input("Password", placeholder="Min. 6 characters", type="password", key="signup_password")
        confirm  = st.text_input("Confirm Password", placeholder="Repeat password", type="password", key="signup_confirm")
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        if st.button("Create Account", type="primary", key="signup_btn", use_container_width=True):
            try:
                user = api_signup(name, email, password, confirm)
                st.session_state.user = user; st.session_state.auth_error = ""; st.session_state.page = "dashboard"; st.rerun()
            except Exception as e:
                st.session_state.auth_error = str(e); st.rerun()
        st.markdown('<div class="auth-divider">or</div>', unsafe_allow_html=True)
        if st.button("Already have an account? Sign in", key="goto_login", use_container_width=True):
            st.session_state.auth_error = ""; st.session_state.page = "login"; st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
def page_dashboard():
    th = THEMES[st.session_state.theme]
    render_header(show_nav=True)
    st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)
    st.markdown(f"""<div style="padding:0 56px 40px;">
        <div style="font-size:11px;letter-spacing:2.5px;text-transform:uppercase;color:{th['eyebrow']};margin-bottom:12px;font-weight:600;">◈ Your Dashboard</div>
        <div style="font-weight:800;font-size:36px;letter-spacing:-1px;color:{th['text']};margin-bottom:8px;">Hello, {st.session_state.user['name'].split()[0]}</div>
        <div style="font-size:15px;color:{th['muted']};">Here is an overview of your document activity.</div></div>""", unsafe_allow_html=True)

    history = st.session_state.history
    cats = list(set(h["category"] for h in history)) if history else []
    s1, s2, s3, s4 = st.columns(4)
    stats = [(str(len(history)),"Documents Analysed"),(str(len(cats)),"Domains Used"),(history[-1]["category"] if history else "—","Last Domain"),(history[-1]["file_name"][:14]+"…" if history and len(history[-1]["file_name"])>14 else (history[-1]["file_name"] if history else "—"),"Last File")]
    for col,(num,label) in zip([s1,s2,s3,s4],stats):
        with col:
            st.markdown(f'<div class="stat-card" style="margin:0 8px;"><div class="stat-number">{num}</div><div class="stat-label">{label}</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
    st.markdown(f'<div style="height:1px;background:{th["divider"]};margin:0 56px 40px;"></div>', unsafe_allow_html=True)

    h_col, a_col = st.columns([1.6,1], gap="large")
    with h_col:
        st.markdown('<div style="padding-left:56px">', unsafe_allow_html=True)
        st.markdown('<div class="panel-label">Recent Documents</div>', unsafe_allow_html=True)
        if not history:
            st.markdown('<div class="empty-state"><div class="empty-icon">◈</div><div class="empty-title">No documents yet</div><div class="empty-sub">Head to the Analyser to process your first document</div></div>', unsafe_allow_html=True)
        else:
            for item in reversed(history[-8:]):
                st.markdown(f'<div class="history-row"><div><div class="history-filename">{item["file_name"]}</div><div class="history-meta">{item["detail_level"]} summary</div></div><div class="history-badge">{item["category"]}</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with a_col:
        st.markdown('<div style="padding-right:56px">', unsafe_allow_html=True)
        st.markdown('<div class="panel-label">Quick Actions</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="background:{th["bg2"]};border:1.5px solid {th["border"]};border-radius:12px;padding:24px 24px 20px;margin-bottom:14px;box-shadow:{th["shadow"]};"><div style="font-weight:700;font-size:15px;color:{th["text"]};margin-bottom:6px;">Analyse a new document</div><div style="font-size:13px;color:{th["label"]};line-height:1.6;">Upload a file and get an AI summary instantly.</div></div>', unsafe_allow_html=True)
        if st.button("◈  Go to Analyser", type="primary", key="dash_to_analyser", use_container_width=True):
            st.session_state.page = "analyser"; st.rerun()
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        st.markdown(f'<div style="background:{th["bg2"]};border:1.5px solid {th["border"]};border-radius:12px;padding:20px 24px;box-shadow:{th["shadow"]};"><div style="font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:{th["label"]};margin-bottom:10px;font-weight:700;">Account</div><div style="font-size:14px;color:{th["text"]};margin-bottom:4px;font-weight:500;">{st.session_state.user["name"]}</div><div style="font-size:12px;color:{th["label"]};">{st.session_state.user["email"]}</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ANALYSER
# ══════════════════════════════════════════════════════════════════════════════
def page_analyser():
    th = THEMES[st.session_state.theme]
    render_header(show_nav=True)
    st.markdown(f"""<div style="padding:56px 56px 40px;max-width:860px;">
        <div style="font-size:11px;letter-spacing:2.5px;text-transform:uppercase;color:{th['eyebrow']};margin-bottom:16px;font-weight:600;">◈ Smart Summarization</div>
        <h1 style="font-weight:800;font-size:52px;line-height:1.05;letter-spacing:-2px;color:{th['hero_title']};margin-bottom:18px;">
            Turn any document<br>into <span style="color:{th['hero_accent']}">clear insight</span></h1>
        <p style="font-size:16px;line-height:1.65;color:{th['hero_sub']};max-width:520px;">
            Upload a file, pick a domain, and get a structured AI summary in seconds.</p></div>""", unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    left_col, right_col = st.columns([1, 1.15], gap="large")
    with left_col:
        st.markdown('<div style="padding-left:56px">', unsafe_allow_html=True)
        st.markdown('<div class="panel-label">01 — Upload Document</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload", type=["pdf","docx","csv","txt"], label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="panel-label">02 — Select Domain</div>', unsafe_allow_html=True)
        if st.session_state.selected_category:
            st.markdown(f'<div class="selected-cat-label">✓ Selected: {st.session_state.selected_category}</div>', unsafe_allow_html=True)
        categories = [("💼","Sales"),("📚","Education"),("⚙️","Technology"),("⚕️","Healthcare"),("⚖️","Legal"),("📊","Finance"),("🏗️","Operations"),("🎯","Marketing"),("🔬","Research")]
        for i in range(0, len(categories), 3):
            row = categories[i:i+3]
            cols = st.columns(3)
            for col,(icon,label) in zip(cols,row):
                with col:
                    if st.button(f"{icon}  {label}", key=f"cat_{label}", use_container_width=True):
                        st.session_state.selected_category = label; st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="panel-label">03 — Summary Style</div>', unsafe_allow_html=True)
        opts = ["Brief","Detailed","Bullet-only"]
        sel = st.radio("Style", options=opts, index=opts.index(st.session_state.selected_detail), horizontal=True, label_visibility="collapsed")
        st.session_state.selected_detail = sel
        st.markdown("<br>", unsafe_allow_html=True)
        can_submit = uploaded_file is not None and st.session_state.selected_category is not None
        if not can_submit:
            missing = (["a file"] if not uploaded_file else []) + (["a domain"] if not st.session_state.selected_category else [])
            st.markdown(f'<p style="font-size:12px;color:{th["label"]};margin-bottom:10px;">Still need: {", ".join(missing)}</p>', unsafe_allow_html=True)
        if st.button("◈  Analyse Document", disabled=not can_submit, use_container_width=True, type="primary", key="analyse_btn"):
            with st.spinner("Uploading and analysing…"):
                try:
                    result = api_summarize(uploaded_file.name, st.session_state.selected_category, st.session_state.selected_detail, uploaded_file)
                    st.session_state.result = result
                    st.session_state.history.append({"file_name": uploaded_file.name, "category": st.session_state.selected_category, "detail_level": st.session_state.selected_detail})
                except Exception as e:
                    st.error(str(e))
        st.markdown('</div>', unsafe_allow_html=True)

    with right_col:
        st.markdown('<div style="padding-right:56px">', unsafe_allow_html=True)
        st.markdown('<div class="panel-label">Output</div>', unsafe_allow_html=True)
        if st.session_state.result is None:
            st.markdown('<div class="empty-state"><div class="empty-icon">◈</div><div class="empty-title">No document analysed yet</div><div class="empty-sub">Upload a file, select a domain, and hit Analyse</div></div>', unsafe_allow_html=True)
        else:
            r = st.session_state.result
            st.markdown(f'<div class="meta-row"><div class="meta-pill accent">◈ {r["category"]}</div><div class="meta-pill">{r["file_name"]}</div><div class="meta-pill">{r["detail_level"]}</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="output-card"><div class="output-card-label">Executive Summary</div><div class="output-body">{r["executive_summary"]}</div></div>', unsafe_allow_html=True)
            bullets = "".join([f'<div class="bullet-item"><div class="bullet-dot"></div><div class="bullet-text">{p}</div></div>' for p in r["key_points"]])
            st.markdown(f'<div class="output-card"><div class="output-card-label">Key Points</div>{bullets}</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                ah = "".join([f'<div class="bullet-item"><div class="bullet-dot" style="background:#7B8CFF"></div><div class="bullet-text">{a}</div></div>' for a in r["action_items"]])
                st.markdown(f'<div class="output-card"><div class="output-card-label" style="color:#7B8CFF">Action Items</div>{ah}</div>', unsafe_allow_html=True)
            with c2:
                dh = "".join([f'<div class="bullet-item"><div class="bullet-dot" style="background:#F0A04B"></div><div class="bullet-text">{d}</div></div>' for d in r["data_highlights"]])
                st.markdown(f'<div class="output-card"><div class="output-card-label" style="color:#F0A04B">Data Highlights</div>{dh}</div>', unsafe_allow_html=True)
            pdf = generate_pdf_report(r)
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(label="↓  Download Report (.pdf)", data=pdf, file_name=f"doclens_{r['file_name'].split('.')[0]}_summary.pdf", mime="application/pdf", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.user is None:
    if st.session_state.page == "signup":
        page_signup()
    else:
        page_login()
else:
    if st.session_state.page == "analyser":
        page_analyser()
    else:
        page_dashboard()
