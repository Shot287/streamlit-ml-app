import streamlit as st
import time

# --- セッション管理の初期化 ---
if "nlp_stage" not in st.session_state:
    st.session_state.nlp_stage = "selection"
if "selected_nlp_question" not in st.session_state:
    st.session_state.selected_nlp_question = ""

def go_to(page):
    st.session_state.nlp_stage = "selection"
    st.session_state.selected_nlp_question = ""
    st.session_state.page = page

def nlp_pages():
    # ▼▼▼ 目印 ▼▼▼
    # この文字がアプリに表示されれば、ファイル更新は成功です。
    st.title("★ファイル更新テスト★")
    # ▲▲▲ 目印 ▲▲▲

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

        if st.session_state.nlp_stage == "selection":
            st.write("こんにちは！ 私はAIアシスタントです。AIや言葉について、どんなことに興味がありますか？下のリストから質問を選んでください。")
            selected = st.radio("質問リスト:", questions, label_visibility="collapsed")
            def decide_button_clicked():
                st.session_state.selected_nlp_question = selected
                st.session_state.nlp_stage = "animation"
            st.button("決定", on_click=decide_button_clicked)

        elif st.session_state.nlp_stage == "animation":
            st.info(f"**質問:**\n\n{st.session_state.selected_nlp_question}")
            st.write("---")
            with st.spinner("AIが回答を考えています..."):
                time.sleep(2)
            st.session_state.nlp_stage = "show_button"
            st.experimental_rerun()

        elif st.session_state.nlp_stage == "show_button":
            st.info(f"**質問:**\n\n{st.session_state.selected_nlp_question}")
            st.write("---")
            st.success("回答の準備ができました！")
            def show_result_button_clicked():
                st.session_state.nlp_stage = "display_answer"
            st.button("結果を見る", on_click=show_result_button_clicked)

        elif st.session_state.nlp_stage == "display_answer":
            st.info(f"**質問:**\n\n{st.session_state.selected_nlp_question}")
            st.write("---")
            answers = {
                questions[0]: "例えば、スマートフォンの音声アシスタントや、動画サイトのおすすめ機能、お店の自動翻訳機など、多くの場所でAI技術が使われ、私たちの生活を便利にしています。",
                questions[1]: "人間は感情や経験から柔軟に考えられますが、AIは大量のデータを正確に高速で処理するのが得意です。疲れを知らない点もAIの強みと言えます。",
                questions[2]: "AIは、ルールが明確な計算やデータ分析は得意ですが、人の気持ちを完全に理解したり、全く新しいものをゼロから創造したりすることはまだ難しいとされています。",
                questions[3]: "AIに質問する時は、「何について」「どんな情報が欲しいか」を具体的に、そして明確な言葉で聞くと、より的確な答えが返ってきやすいです。背景情報も加えるとさらに良いでしょう。",
                questions[4]: "AIは、たくさんの文章データを読んで、「この単語の後にはこの単語が来やすい」といった言葉のパターンを統計的に学習します。それによって、文の意味を予測したり、文章を生成したりしています。",
                questions[5]: "より詳しく言うと、AIは単語を「ベクトル」という数字の集まりに変換します。似た意味の単語は近い数字のベクトルになり、AIはこの数字の関係性から文全体の意味を計算します。この技術を「単語埋め込み」と呼び、自然言語処理の基礎となっています。"
            }
            st.success("回答:")
            st.info(answers.get(st.session_state.selected_nlp_question, "エラー：回答が見つかりません。"))

        st.divider()
        st.button("体験を終えて、まとめへ進む", on_click=go_to, args=("自然言語処理まとめ",), use_container_width=True)
        st.markdown("<div style='text-align:center;'>1-2</div>", unsafe_allow_html=True)

    # 1-3: 自然言語処理まとめ
    elif st.session_state.page == "自然言語処理まとめ":
        st.header("自然言語処理まとめ")
        st.success("体験お疲れ様でした！")
        st.write("""
        今回は、AIとの質疑応答を通して、AIがどのように言葉を扱っているかの一端を体験しました。
        AIは単語や文を**データとして処理**し、膨大な知識の中から最も関連性の高い答えを探し出しています。

        私たちが普段何気なく使っているスマートフォンの検索や翻訳アプリも、このような自然言語処理技術の応用例です。
        AIへの質問の仕方を工夫することで、この強力なツールをより上手に活用することができます。
        """)
        st.button("もう一度体験する", on_click=go_to, args=("自然言語処理体験",))
        st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
        st.markdown("<div style='text-align:center;'>1-3</div>", unsafe_allow_html=True)