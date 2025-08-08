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
# スタイル（明るめ配色＋ボタン高さ完全統一／中央白四角削除）
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

/* glassカード削除 → 背景透明にして枠・影も消去 */
.glass {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  padding: 0 !important;
}

/* タイトル */
h1.title {
  color: #0f172a;
  font-weight: 800;
  letter-spacing: .02em;
  text-align: center;
  margin-bottom: .2rem;
}

/* サブタイトル */
p.subtitle {
  color: #334155;
  text-align: center;
  margin: 0 0 1.6rem 0;
  font-size: 1.05rem;
}

/* ボタン共通 */
.stButton > button {
  background: linear-gradient(135deg, #38bdf8, #0ea5e9);
  color: #ffffff;
  border: none;
  border-radius: 14px;
  font-weight: 700;
  font-size: 1rem;
  box-shadow: 0 4px 12px rgba(14,165,233,0.3);
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
  box-shadow: 0 6px 14px rgba(14,165,233,0.4);
}
.stButton > button:active {
  transform: translateY(0);
}

/* セカンダリ（右のボタン） */
.btn-secondary .stButton > button {
  background: linear-gradient(135deg, #94a3b8, #64748b) !important;
  color: #ffffff !important;
  height: 64px !important;
  min-height: 64px !important;
  max-height: 64px !important;
  padding: 0 1.2rem !important;
  line-height: 1 !important;
}

/* 同じ高さ揃え */
.btn-same-height .stButton > button {
  height: 64px !important;
  min-height: 64px !important;
  max-height: 64px !important;
  padding: 0 1.2rem !important;
  line-height: 1 !important;
}

/* ラベル */
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

/* カード内テキスト */
.card-title { color: #0f172a; font-weight: 700; margin-bottom: .3rem; }
.card-text  { color: #334155; font-size: 0.95rem; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

# --- ページルーティング ---
if st.session_state.page == "タイトル":
    st.markdown('<h1 class="title">AIの裏側体験</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">高校生向けに、AIがどう考え・どう見ているのかを直感的に体験できます。</p>', unsafe_allow_html=True)

    with st.container():
        col_a, col_b = st.columns([1, 1], gap="large")

        with col_a:
            st.markdown('<div class="label-chip">🧠 言葉を理解するAI</div>', unsafe_allow_html=True)
            st.markdown('<h3 class="card-title">自然言語処理（NLP）</h3>', unsafe_allow_html=True)
            st.markdown(
                '<p class="card-text">質問に答えたり要約したり。AIが「言葉」をどう分解し、意味を推測しているのかを体験します。</p>',
                unsafe_allow_html=True,
            )
            st.markdown('<div class="btn-same-height">', unsafe_allow_html=True)
            st.button("🗣️  自然言語処理を体験する", on_click=go_to, args=("自然言語処理イントロ",), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_b:
            st.markdown('<div class="label-chip">👀 画像を見るAI</div>', unsafe_allow_html=True)
            st.markdown('<h3 class="card-title">画像分類（Vision）</h3>', unsafe_allow_html=True)
            st.markdown(
                '<p class="card-text">犬の画像を素材に、AIが特徴を拾って判定する流れを体験。途中の“考え方”も見ていきます。</p>',
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
