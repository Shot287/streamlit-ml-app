import streamlit as st

def go_to(page):
    st.session_state.page = page

def nlp_pages():
    # 1-1
    if st.session_state.page == "自然言語処理イントロ":
        st.header("自然言語処理とは？")
        st.write("""
自然言語処理（NLP）は、人間の言葉をコンピュータが理解・分析するAI技術です。
文章から意味を読み取る、感情分析、要約、翻訳もNLPの応用例です。
""")
        st.button("体験スタート", on_click=go_to, args=("自然言語処理体験",))
        st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
        st.markdown("<div style='text-align:center;'>1-1</div>", unsafe_allow_html=True)
    # 1-2
    elif st.session_state.page == "自然言語処理体験":
        st.header("自然言語処理体験")
        st.write("（ここに自然言語処理体験の内容を実装できます）")
        st.button("前のページへ戻る", on_click=go_to, args=("自然言語処理イントロ",))
        st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
        st.markdown("<div style='text-align:center;'>1-2</div>", unsafe_allow_html=True)
    # 1-3
    elif st.session_state.page == "自然言語処理まとめ":
        st.header("自然言語処理まとめ")
        st.write("（まとめページ）")
        st.button("前のページへ戻る", on_click=go_to, args=("自然言語処理体験",))
        st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
        st.markdown("<div style='text-align:center;'>1-3</div>", unsafe_allow_html=True)
