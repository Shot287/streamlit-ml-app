import streamlit as st
from nlp_route import nlp_pages
from image_route import image_pages

# セッション管理の初期化
if "page" not in st.session_state:
    st.session_state.page = "タイトル"

def go_to(page):
    st.session_state.page = page

# --- ページルーティング ---
if st.session_state.page == "タイトル":
    st.title("機械学習・AI体験")
    st.write("高校生向けのAI体験アプリです。")
    st.button("1. 自然言語処理を体験する", on_click=go_to, args=("自然言語処理イントロ",), use_container_width=True)
    st.button("2. 画像分類を体験する", on_click=go_to, args=("画像分類イントロ",), use_container_width=True)
    st.markdown("<div style='text-align:center;'>-</div>", unsafe_allow_html=True)

elif st.session_state.page.startswith("自然言語処理"):
    nlp_pages()

# "画像分類"で始まるすべてのページをimage_pagesに集約
elif st.session_state.page.startswith("画像分類"):
    image_pages()

else:
    st.error(f"ページが見つかりません: {st.session_state.page}")
    st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))