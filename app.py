"""
Dubai urban heat dashboard on Streamlit.

The dashboard is one HTML file (static/dashboard.html). Streamlit serves it as a normal
file and shows it full width. The open AI models (Qwen, Llama, Phi, Gemma ...) run inside
each visitor's own browser, so this app needs no GPU, no API key and almost no server memory.

To update the dashboard: replace static/dashboard.html (or static/dashboard.html.gz) in the
GitHub repository. Streamlit redeploys automatically.
"""
from __future__ import annotations

import gzip
import shutil
import urllib.request
from pathlib import Path

import streamlit as st

STATIC = Path(__file__).parent / "static"
PAGE = "dashboard.html"
URL = f"/app/static/{PAGE}"

st.set_page_config(page_title="Dubai urban heat hotspots", page_icon="🌡️", layout="wide",
                   initial_sidebar_state="collapsed")


@st.cache_resource
def prepare_dashboard() -> bool:
    """Make sure static/dashboard.html exists.

    GitHub's web upload refuses files over 25 MB, so the dashboard may be committed as
    dashboard.html.gz.part01, part02 ... (made by split_dashboard.py), as one
    dashboard.html.gz, or as the plain dashboard.html. Pieces are joined and unpacked here.
    """
    target, gz = STATIC / PAGE, STATIC / (PAGE + ".gz")
    if target.exists():
        return True
    parts = sorted(STATIC.glob(PAGE + ".gz.part*"))
    tmp = STATIC / "_dashboard.tmp"
    if parts:
        with open(tmp, "wb") as joined:
            for part in parts:
                with open(part, "rb") as f:
                    shutil.copyfileobj(f, joined)
        source = tmp
    elif gz.exists():
        source = gz
    else:
        return False
    with gzip.open(source, "rb") as src, open(STATIC / "_dashboard.html.tmp", "wb") as dst:
        shutil.copyfileobj(src, dst)
    (STATIC / "_dashboard.html.tmp").replace(target)
    tmp.unlink(missing_ok=True)
    return target.exists()


@st.cache_resource
def static_serves_html() -> bool | None:
    """Ask this app's own server whether /app/static/dashboard.html comes back as a web page.

    Streamlit's documentation lists only images, fonts, PDF, XML and JSON as served normally,
    so on some versions or hosts an .html file would arrive as plain text. Returns True/False,
    or None if the check itself could not be made.
    """
    port = st.get_option("server.port") or 8501
    base = (st.get_option("server.baseUrlPath") or "").strip("/")
    url = f"http://127.0.0.1:{port}/{base + '/' if base else ''}app/static/{PAGE}"
    try:
        with urllib.request.urlopen(url, timeout=5) as r:      # only the headers are read
            return r.headers.get("Content-Type", "").lower().startswith("text/html")
    except Exception:
        return None


st.markdown(
    """
    <style>
      header[data-testid="stHeader"] {display:none}
      .block-container {padding: .6rem .8rem 0 .8rem; max-width: 100%}
      footer {display:none}
      iframe {border: 0; border-radius: 8px}
    </style>
    """,
    unsafe_allow_html=True,
)

if not prepare_dashboard():
    st.error("No dashboard file found. Put it in the `static` folder as `dashboard.html`, "
             "`dashboard.html.gz`, or the `dashboard.html.gz.part01, part02 ...` pieces and redeploy.")
    st.stop()

compat_forced = st.query_params.get("mode") == "embedded"
with st.sidebar:
    st.header("Dubai urban heat dashboard")
    compat = st.toggle("Compatibility mode", value=compat_forced,
                       help="Use this if the dashboard area below stays blank or shows code. "
                            "It sends the page through the app itself: slower to open, but works everywhere.")
use_embedded = compat or compat_forced or static_serves_html() is False

if use_embedded:
    with st.sidebar:
        st.caption("Compatibility mode is on (the dashboard is sent through the app, so it opens more slowly).")
    st.iframe(STATIC / PAGE, height=1700)
else:
    with st.sidebar:
        st.markdown(f"[Open full screen in a new tab]({URL}) (best on phones and tablets)")
    st.iframe(URL, height=1700)

with st.sidebar:
    st.caption("The AI models run in your own browser: free, private, no API key. "
               "Use Chrome or Edge on a computer. If the model list is greyed out, "
               "choose “No AI: built-in rules”.")
