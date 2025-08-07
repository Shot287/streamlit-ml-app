import streamlit as st
import time

# --- セッション管理の初期化 ---
# 進行状況と選択された質問を管理
if "nlp_stage" not in st.session_state:
    st.session_state.nlp_stage = "selection"
if "selected_nlp_question_index" not in st.session_state:
    st.session_state.selected_nlp_question_index = 0

def go_to(page):
    # ページを移動する際に進行状況をリセット
    st.session_state.nlp_stage = "selection"
    st.session_state.page = page

def nlp_pages():
    # 1-1: 自然言語処理イントロ
    if st.session_state.page == "自然言語処理イントロ":
        st.header("自然言語処理とは？")
        st.write("""
        自然言語処理（NLP）は、人間の言葉（自然言語）をコンピュータが理解・分析するAI技術です。
        文章の意味を読み取ったり、要約や翻訳をしたりと、様々な場面で活躍しています。
        今回はAIアシスタントに質問をして、その技術の一端を体験してみましょう。
        """)
        st.button("体験スタート", on_click=go_to, args=("自然言語処理体験",))
        st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
        st.markdown("<div style='text-align:center;'>1-1</div>", unsafe_allow_html=True)

    # 1-2: 自然言語処理体験
    elif st.session_state.page == "自然言語処理体験":
        st.header("AIアシスタントへの質問")

        questions = [
            "最近、AI技術がどのように私たちの日常生活を変えているのか、具体的な例を交えて教えてください。",
            "AIと人間の違いやAIの強みについて、わかりやすく説明してください。",
            "AIにできること、できないことについて、具体例を交えて説明してください。",
            "AIに質問するとき、どんな聞き方をすると正確で分かりやすい答えが返ってきやすいですか？",
            "AIはどうやって人間の言葉を理解しているのか、その仕組みをできるだけ詳しく説明してください。",
            "AIはどうやって人間の言葉を理解しているのか、その仕組みをできるだけ詳しく説明してください。 "
        ]

        # --- ステージ1: 質問選択 ---
        if st.session_state.nlp_stage == "selection":
            st.write("こんにちは！ 私はAIアシスタントです。AIや言葉について、どんなことに興味がありますか？下のリストから質問を選んでください。")
            
            # st.radioの選択値をst.session_stateに直接保存するため、`key`を指定
            st.radio(
                "質問リスト:",
                range(len(questions)), # インデックスで選択を管理
                format_func=lambda i: questions[i], # 表示は質問文
                label_visibility="collapsed",
                key="selected_nlp_radio_index" # keyを追加
            )

            def decide_button_clicked():
                # st.session_stateから最新の選択値を取得
                st.session_state.selected_nlp_question_index = st.session_state.selected_nlp_radio_index
                st.session_state.nlp_stage = "animation"
            
            st.button("決定", on_click=decide_button_clicked)

        # --- ステージ2: アニメーション & ページ遷移 ---
        elif st.session_state.nlp_stage == "animation":
            st.info(f"**質問:**\n\n{questions[st.session_state.selected_nlp_question_index]}")
            st.write("---")
            
            with st.spinner("AIが回答を考えています..."):
                time.sleep(2)

            # 選択された質問のインデックス(0-5)に応じて、遷移先のページ名を決定
            next_page_index = st.session_state.selected_nlp_question_index + 1
            next_page = f"自然言語処理結果_{next_page_index}"
            
            # ページ遷移を実行
            go_to(next_page)
            st.experimental_rerun()

        st.divider()
        st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
        st.markdown("<div style='text-align:center;'>1-2</div>", unsafe_allow_html=True)

    # 「まとめ」のブロックをforループの前に移動
    # 1-4: 自然言語処理まとめ
    elif st.session_state.page == "自然言語処理まとめ":
        st.header("自然言語処理まとめ")
        st.success("体験お疲れ様でした！")
        st.write("（まとめページの内容）")
        st.button("もう一度体験する", on_click=go_to, args=("自然言語処理体験",))
        st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
        st.markdown("<div style='text-align:center;'>1-4</div>", unsafe_allow_html=True)

    # 1-3: 各結果ページの生成
    for i in range(1, 7):
        page_name = f"自然言語処理結果_{i}"
        if st.session_state.page == page_name:
            st.header(f"質問{i}への回答")
            
            # ここに、各ページの回答文章を後から記述できます
            st.info(f"（ここに、質問{i}に対する回答文章を実装します）")

            st.divider()
            st.button("もう一度質問を選ぶ", on_click=go_to, args=("自然言語処理体験",))
            st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
            st.markdown(f"<div style='text-align:center;'>1-3-{i}</div>", unsafe_allow_html=True)
            return # 該当ページを表示したら処理を終了