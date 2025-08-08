import streamlit as st
from nlp_route import nlp_pages
from image_route import image_pages

# ページ設定（タイトル・アイコン・横幅）
st.set_page_config(page_title="AIの裏側体験", page_icon="🧪", layout="wide")

# セッション管理の初期化
if "page" not in st.session_state:
    st.session_state.page = "タイトル"

def go_to(page):
    st.session_state.page = page

# ======================
# グローバルなスタイル調整
# ======================
# - 背景に淡いグラデーション
# - カード（コンテナ）にガラス風の半透明とぼかし
# - 丸みのある大きめボタンにシャドウ＆ホバー演出
st.markdown("""
<style>
/* 背景グラデーション */
.stApp {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 40%, #0b1020 100%);
}

/* メイン領域の幅とセンタリング */
.block-container {
  padding-top: 3rem !important;
  padding-bottom: 3rem !important;
  max-width: 1100px;
}

/* ガラスカード */
.glass {
  backdrop-filter: blur(10px);
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.35);
  padding: 2.2rem 2rem;
}

/* タイトル */
h1.title {
  color: #e5e7eb;
  font-weight: 800;
  letter-spacing: .02em;
  text-align: center;
  margin-bottom: .2rem;
}

/* サブタイトル */
p.subtitle {
  color: #cbd5e1;
  text-align: center;
  margin: 0 0 1.6rem 0;
}

/* 汎用ボタン（全ページ共通で良い感じに） */
.stButton > button {
  background: linear-gradient(135deg, #6366f1, #22d3ee);
  color: #0b1020;
  border: none;
  border-radius: 16px;
  padding: 0.9rem 1.2rem;
  font-weight: 700;
  font-size: 1.05rem;
  box-shadow: 0 8px 22px rgba(34,211,238,0.25);
  transition: transform .08s ease, box-shadow .2s ease, filter .2s ease;
}
.stButton > button:hover {
  transform: translateY(-1px);
  filter: brightness(1.05);
  box-shadow: 0 12px 26px rgba(34,211,238,0.35);
}
.stButton > button:active {
  transform: translateY(0);
}

/* セカンダリ（落ち着いた） */
.btn-secondary > button {
  background: linear-gradient(135deg, #94a3b8, #64748b) !important;
  color: #0b1020 !important;
}

/* スモールラベル */
.label-chip {
  display: inline-block;
  padding: .32rem .66rem;
  border-radius: 999px;
  background: rgba(148,163,184,0.18);
  color: #e2e8f0;
  font-size: .82rem;
  border: 1px solid rgba(226,232,240,0.12);
}

/* カード内の見出し */
.card-title {
  color: #e2e8f0;
  font-weight: 700;
  margin-bottom: .35rem;
}

/* カード内の本文 */
.card-text {
  color: #cbd5e1;
  font-size: 0.95rem;
  line-height: 1.5;
}

/* 区切りの薄い線 */
hr.soft-divider {
  border: none;
  border-top: 1px solid rgba(226,232,240,0.08);
  margin: 1.1rem 0 1.4rem 0;
}
</style>
""", unsafe_allow_html=True)

# --- ページルーティング ---
if st.session_state.page == "タイトル":
    # ヒーローセクション
    st.markdown('<h1 class="title">AIの裏側体験</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">高校生向けに、AIがどう考え・どう見ているのかを直感的に体験できます。</p>', unsafe_allow_html=True)

    # 概要カード
    with st.container():
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        col_a, col_b = st.columns([1, 1], gap="large")

        with col_a:
            st.markdown('<div class="label-chip">🧠 言葉を理解するAI</div>', unsafe_allow_html=True)
            st.markdown('<h3 class="card-title">自然言語処理（NLP）</h3>', unsafe_allow_html=True)
            st.markdown(
                '<p class="card-text">質問に答えたり要約したり。<br>AIが「言葉」をどう分解し、意味を推測しているのかを体験します。</p>',
                unsafe_allow_html=True,
            )
            c1 = st.container()
            with c1:
                st.button("🗣️  自然言語処理を体験する", on_click=go_to, args=("自然言語処理イントロ",), use_container_width=True)

        with col_b:
            st.markdown('<div class="label-chip">👀 画像を見るAI</div>', unsafe_allow_html=True)
            st.markdown('<h3 class="card-title">画像分類（Vision）</h3>', unsafe_allow_html=True)
            st.markdown(
                '<p class="card-text">犬の画像を素材に、AIが特徴を拾って判定する流れを体験。<br>途中の“考え方”も見ていきます。</p>',
                unsafe_allow_html=True,
            )
            c2 = st.container()
            with c2:
                # セカンダリは色味を少し落として差別化
                btn = st.container()
                with btn:
                    st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
                    st.button("📷  画像分類を体験する", on_click=go_to, args=("画像分類イントロ",), use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<hr class="soft-divider">', unsafe_allow_html=True)

        # 下段の補助ボックス
        col_c, col_d, col_e = st.columns([1, 1, 1], gap="large")
        with col_c:
            st.markdown('<div class="label-chip">⚡ 体験の流れ</div>', unsafe_allow_html=True)
            st.markdown('<p class="card-text">選ぶ → 待つ → 見る。<br>“裏側”は適宜スライドで解説。</p>', unsafe_allow_html=True)
        with col_d:
            st.markdown('<div class="label-chip">🧩 必要な準備</div>', unsafe_allow_html=True)
            st.markdown('<p class="card-text">ブラウザのみ。展示では固定画像を使用します。</p>', unsafe_allow_html=True)
        with col_e:
            st.markdown('<div class="label-chip">🎯 ねらい</div>', unsafe_allow_html=True)
            st.markdown('<p class="card-text">AIの強み/限界をイメージで掴むこと。</p>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)  # .glass end

elif st.session_state.page.startswith("自然言語処理"):
    nlp_pages()

# "画像分類"で始まるすべてのページをimage_pagesに集約
elif st.session_state.page.startswith("画像分類"):
    image_pages()

else:
    st.error(f"ページが見つかりません: {st.session_state.page}")
    st.button("タイトルへ戻る", on_click=go_to, args=("タイトル",))
