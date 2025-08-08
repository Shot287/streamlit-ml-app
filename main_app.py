import streamlit as st
from nlp_route import nlp_pages
from image_route import image_pages

# ページ設定
st.set_page_config(page_title="AIの裏側体験", page_icon="🧪", layout="wide")

# セッション管理の初期化
if "page" not in st.session_state:
    st.session_state.page = "タイトル"

def go_to(page):
    st.session_state.page = page

# ======================
# スタイル（背景＋新ボタン配色）
# ======================
st.markdown("""
<style>
/* 背景：明るいグラデーション */
.stApp {
  background: linear-gradient(135deg, #fefefe 0%, #e6f7ff 40%, #f0faff 100%);
}

/* メイン領域 */
.block-container {
  padding-top: 3rem !important;
  padding-bottom: 3rem !important;
  max-width: 1100px;
}

/* glassカード無効化（白帯削除） */
.glass { background: transparent !important; border: none !important; box-shadow: none !important; padding: 0 !important; }

/* タイトル・サブタイトル */
h1.title { color: #0f172a; font-weight: 800; letter-spacing: .02em; text-align: center; margin-bottom: .2rem; }
p.subtitle { color: #334155; text-align: center; margin: 0 0 1.6rem 0; font-size: 1.05rem; }

/* --- プライマリボタン（淡ティール系） --- */
.stButton > button {
  background: linear-gradient(135deg, #5eead4, #14b8a6);
  color: #ffffff;
  border: none;
  border-radius: 14px;
  font-weight: 700;
  font-size: 1rem;
  box-shadow: 0 4px 12px rgba(20,184,166,0.3);
  transition: all .15s ease;

  height: 64px !important;
  min-height: 64px !important;
  max-height: 64px !important;
  padding: 0 1.2rem !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  line-height: 1 !important;
  gap: .5rem !important;
}
.stButton > button:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 14px rgba(20,184,166,0.4);
}
.stButton > button:active { transform: translateY(0); }

/* --- セカンダリボタン（サーモンピンク系） --- */
.btn-secondary .stButton > button {
  background: linear-gradient(135deg, #fb7185, #f43f5e) !important;
  color: #ffffff !important;

  height: 64px !important;
  min-height: 64px !important;
  max-height: 64px !important;
  padding: 0 1.2rem !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  line-height: 1 !important;
  gap: .5rem !important;
}
.btn-secondary .stButton > button:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 14px rgba(244,63,94,0.4) !important;
}

/* ユーティリティ：同じ高さ揃え */
.btn-same-height .stButton > button {
  height: 64px !important;
  min-height: 64px !important;
  max-height: 64px !important;
  padding: 0 1.2rem !important;
  line-height: 1 !important;
}

/* ラベル＆テキスト */
.label-chip {
  display: inline-block;
  padding: .3rem .7rem;
  border-radius: 999px;
  background: rgba(56,189,248,0.15);
  color: #0369a1;
  font-size: .82rem;
  border: 1px solid rgba(56,189,248,0.25);
  margin-bottom: .3rem;
}
.card-title { color: #0f172a; font-weight: 700; margin-bottom: .3rem; }
.card-text  { color: #334155; font-size: 0.95rem; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

# --- ページルーティング ---
if st.session_state.page == "タイトル":
    st.markdown('<h1 class="title">AIの裏側体験</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AIがどう考え・どう見ているのかを直感的に体験できます。</p>', unsafe_allow_html=True)

    with st.container():
        col_a, col_b = st.columns([1, 1], gap="large")

        with col_a:
            st.markdown('<div class="label-chip">🧠 言葉を理解するAI</div>', unsafe_allow_html=True)
            st.markdown('<h3 class="card-title">自然言語処理（NLP）</h3>', unsafe_allow_html=True)
            st.markdown(
                '<p class="card-text">AIの文章生成の裏側の一部を体験できます。</p>',
                unsafe_allow_html=True,
            )
            st.markdown('<div class="btn-same-height">', unsafe_allow_html=True)
            st.button("🗣️  自然言語処理を体験する", on_click=go_to, args=("自然言語処理イントロ",), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_b:
            st.markdown('<div class="label-chip">👀 画像を見るAI</div>', unsafe_allow_html=True)
            st.markdown('<h3 class="card-title">画像分類（Vision）</h3>', unsafe_allow_html=True)
            st.markdown(
                '<p class="card-text">AIの犬種判別の裏側の一部を体験できます。</p>',
                unsafe_allow_html=True,
            )
            st.markdown('<div class="btn-secondary btn-same-height">', unsafe_allow_html=True)
            st.button("📷  画像分類を体験する", on_click=go_to, args=("画像分類イントロ",), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page.startswith("自然言語処理"):
    nlp_pages()

elif st.session_state.page.startswith("画像分類"):
    image_pages()

else:
    st.error(f"ページが見つかりません: {st.session_state.page}")
    st.button("タイトルへ戻る", on_click=go_to, args=("タイトル",))
