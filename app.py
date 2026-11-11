import streamlit as st
from evaluation.evaluate import build_engine

st.set_page_config(
    page_title="ShopSense | Blue Orchid",
    page_icon="🪻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Blue Orchid palette: rich orchid text, pale lavender surfaces, accessible contrast.
st.markdown(
    """
    <style>
    :root {
        color-scheme: light;
        --orchid-950: #2d1747;
        --orchid-900: #3b205c;
        --orchid-800: #512b78;
        --orchid-700: #693b91;
        --orchid-600: #8054a8;
        --orchid-200: #d9c9ee;
        --lavender-100: #f7f3fc;
        --lavender-150: #f2ebfa;
        --lavender-200: #e9def5;
        --white: #ffffff;
    }

    html, body, [class*="stApp"] {
        color: var(--orchid-950);
        background: #f4effa;
    }
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(145deg, #fbf9fe 0%, #f3eef9 54%, #ece7f8 100%);
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stMain"] { color: var(--orchid-950); }
    .block-container { max-width: 1180px; padding-top: 1.8rem; padding-bottom: 3rem; }

    /* Hero */
    .hero {
        background: linear-gradient(118deg, #382052 0%, #5b347b 58%, #79559b 100%);
        border: 1px solid rgba(255,255,255,.22);
        border-radius: 24px;
        box-shadow: 0 14px 34px rgba(57,31,83,.16);
        margin: 0 0 1.6rem;
        padding: clamp(1.4rem, 4vw, 2.5rem);
        color: #fff;
    }
    .hero h1 { color: #fff !important; font-size: clamp(2rem, 4vw, 2.7rem); font-weight: 780; margin: 0 0 .35rem; }
    .hero p { color: #f3eafa !important; font-size: 1.04rem; margin: 0; }

    /* Consistent text contrast across normal Streamlit content. */
    [data-testid="stMain"] h1, [data-testid="stMain"] h2,
    [data-testid="stMain"] h3, [data-testid="stMain"] h4,
    [data-testid="stMain"] p, [data-testid="stMain"] li,
    [data-testid="stMain"] label, [data-testid="stMain"] small,
    [data-testid="stMain"] [data-testid="stCaptionContainer"] {
        color: var(--orchid-950);
    }
    [data-testid="stMain"] h1, [data-testid="stMain"] h2,
    [data-testid="stMain"] h3 { letter-spacing: -.02em; }

    /* Chat bubbles also serve as product detail cards. */
    [data-testid="stChatMessage"] {
        background: rgba(255,255,255,.96);
        border: 1px solid #dfd2ee;
        border-radius: 18px;
        box-shadow: 0 5px 18px rgba(55,31,82,.07);
        margin: .55rem 0 .85rem;
        padding: 1rem 1.15rem;
    }
    [data-testid="stChatMessage"] * { color: var(--orchid-950) !important; }
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p { line-height: 1.62; }
    [data-testid="stChatMessage"] strong { color: var(--orchid-800) !important; font-weight: 750; }

    /* Input and placeholder */
    [data-testid="stChatInput"] {
        background: #fff;
        border: 1.5px solid #b99bd5;
        border-radius: 16px;
        box-shadow: 0 5px 18px rgba(55,31,82,.08);
    }
    [data-testid="stChatInput"]:focus-within { border-color: var(--orchid-700); box-shadow: 0 0 0 3px rgba(105,59,145,.16); }
    [data-testid="stChatInput"] textarea,
    [data-testid="stChatInput"] textarea:focus {
        background: #fff !important;
        color: var(--orchid-950) !important;
        caret-color: var(--orchid-800);
        -webkit-text-fill-color: var(--orchid-950) !important;
    }
    [data-testid="stChatInput"] textarea::placeholder,
    [data-testid="stChatInput"] textarea::-webkit-input-placeholder {
        color: #705986 !important;
        -webkit-text-fill-color: #705986 !important;
        opacity: 1 !important;
    }

    /* Light sidebar with dark, legible text. */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f0e8f8 0%, #e9def4 100%);
        border-right: 1px solid #d8c7e8;
    }
    [data-testid="stSidebar"] * { color: var(--orchid-950); }
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] { color: #614c75 !important; }

    /* System status alerts use explicit card wrappers so these white-text
       rules override the general lavender-sidebar and alert text colors. */
    .system-status-heading { color: #512b78 !important; font-weight: 750 !important; }
    [data-testid="stSidebar"] .st-key-catalog-status-card [data-testid="stAlert"],
    [data-testid="stSidebar"] .st-key-retrieval-status-card [data-testid="stAlert"] {
        border: 1px solid rgba(255,255,255,.22);
        border-radius: 12px;
        padding: .2rem .25rem;
        overflow-wrap: anywhere;
    }
    [data-testid="stSidebar"] .st-key-catalog-status-card [data-testid="stAlert"],
    [data-testid="stSidebar"] .st-key-catalog-status-card [data-testid="stAlert"] [data-baseweb="notification"] {
        background: #28734e !important;
    }
    [data-testid="stSidebar"] .st-key-retrieval-status-card [data-testid="stAlert"],
    [data-testid="stSidebar"] .st-key-retrieval-status-card [data-testid="stAlert"] [data-baseweb="notification"] {
        background: #202044 !important;
    }
    [data-testid="stSidebar"] .st-key-catalog-status-card [data-testid="stAlert"] *,
    [data-testid="stSidebar"] .st-key-retrieval-status-card [data-testid="stAlert"] *,
    [data-testid="stSidebar"] .st-key-catalog-status-card [data-testid="stAlert"] [data-baseweb="notification"] *,
    [data-testid="stSidebar"] .st-key-retrieval-status-card [data-testid="stAlert"] [data-baseweb="notification"] * {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
        font-weight: 650 !important;
    }

    /* Buttons */
    .stButton > button, [data-testid="stBaseButton-primary"] {
        background: linear-gradient(120deg, #603482, #8054a8);
        border: 1px solid #603482;
        border-radius: 12px;
        color: #fff !important;
        font-weight: 650;
        min-height: 2.7rem;
        transition: transform .15s ease, box-shadow .15s ease, background .15s ease;
    }
    .stButton > button *, [data-testid="stBaseButton-primary"] * { color: #fff !important; }
    .stButton > button:hover, [data-testid="stBaseButton-primary"]:hover {
        background: #492663;
        border-color: #492663;
        box-shadow: 0 5px 14px rgba(60,32,88,.2);
        transform: translateY(-1px);
    }
    .stButton > button:focus-visible { outline: 3px solid #b694d4; outline-offset: 2px; }

    /* Evidence, expanders, alerts, and form controls */
    [data-testid="stExpander"] {
        background: #fff;
        border: 1px solid #dfd2ee;
        border-radius: 14px;
        overflow: hidden;
    }
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary * { color: var(--orchid-800) !important; font-weight: 650; }
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] { background: #fff; color: var(--orchid-950); }
    [data-testid="stExpander"] [data-testid="stMarkdownContainer"] p { color: var(--orchid-950) !important; overflow-wrap: anywhere; }
    [data-testid="stAlert"] { border-radius: 12px; }
    [data-testid="stAlert"] p { color: var(--orchid-950) !important; }
    [data-testid="stStatusWidget"] { color: var(--orchid-950); }
    hr { border-color: #d8c7e8; }
    .footer { color: #665276; text-align: center; padding: 1.5rem .5rem; font-size: .88rem; }

    @media (max-width: 700px) {
        .block-container { padding: 1rem .8rem 2rem; }
        .hero { border-radius: 18px; }
        [data-testid="stChatMessage"] { padding: .85rem; }
    }
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after { transition-duration: .01ms !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="hero">
      <h1>🪻 ShopSense</h1>
      <p>Discover smarter. Shop better. Your product discovery and store policy assistant.</p>
    </section>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner="Loading catalog and policy…")
def engine():
    return build_engine()


try:
    bot = engine()
except Exception as exc:
    st.error("Unable to initialize ShopSense. Check the project environment, catalog, and policy PDF.")
    st.exception(exc)
    st.stop()

with st.sidebar:
    st.markdown("## 🪻 ShopSense")
    st.caption("Your intelligent shopping companion")
    st.divider()
    st.markdown('<h3 class="system-status-heading">System status</h3>', unsafe_allow_html=True)
    with st.container(key="catalog-status-card"):
        st.success(f"Catalog and policy loaded · {len(bot.catalog)} products")
    with st.container(key="retrieval-status-card"):
        st.info(f"Retrieval backend: {bot.hybrid.index.backend}")
    st.divider()
    st.markdown("### What can I help with?")
    st.markdown(
        "- 🛍️ Product discovery\n"
        "- 💰 Budget-based search\n"
        "- 📦 Stock availability\n"
        "- 💻 Product specifications\n"
        "- 📄 Store policies"
    )
    st.divider()
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("### ✨ Start exploring")
suggestions = [
    "Find a laptop under ₹70,000 with 16GB RAM",
    "Suggest a 27-inch monitor under ₹15,000",
    "Can I return an opened headset?",
]
for col, suggestion in zip(st.columns(3), suggestions):
    with col:
        if st.button(suggestion, use_container_width=True):
            st.session_state.pending_question = suggestion


def render_sources(sources):
    if sources:
        with st.expander("📚 Supporting evidence", expanded=False):
            for source in sources:
                st.write(source)


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        render_sources(message.get("sources", []))

question = st.chat_input("Ask about products, prices, stock, specifications, or policies…")
if not question and "pending_question" in st.session_state:
    question = st.session_state.pop("pending_question")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("🪻 Searching products and policy documents…"):
            try:
                result = bot.answer(question)
                answer = result.get("answer", "I couldn't generate an answer. Please try again.")
                sources = result.get("sources", [])
                st.markdown(answer)
                render_sources(sources)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                })
            except Exception as exc:
                st.error("Something went wrong while processing your query. Please try again.")
                st.exception(exc)

st.markdown(
    '<div class="footer">🪻 ShopSense · Powered by hybrid retrieval<br>Discover smarter. Shop better.</div>',
    unsafe_allow_html=True,
)
