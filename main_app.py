import streamlit as st
from nlp_route import nlp_pages
from image_route import image_pages

if "page" not in st.session_state:
    st.session_state.page = "タイトル"

def go_to(page):
    st.session_state.page = page

# --- タイトル画面 ---
if st.session_state.page == "タイトル":
    st.title("機械学習・AI体験")
    st.button("自然言語処理", on_click=go_to, args=("自然言語処理イントロ",))
    st.button("画像分類", on_click=go_to, args=("画像分類イントロ",))
    st.markdown("<div style='text-align:center;'>-</div>", unsafe_allow_html=True)

# --- 各ルートへ分岐 ---
elif st.session_state.page.startswith("自然言語処理"):
    nlp_pages()
elif st.session_state.page.startswith("画像分類"):
    image_pages()
else:
    st.write(f"ページが見つかりません: {st.session_state.page}")
