import streamlit as st
import time

# --- セッション管理の初期化 ---
# 表示する回答を保存する変数
if "nlp_answer" not in st.session_state:
    st.session_state.nlp_answer = ""

def go_to(page):
    # ページを移動する際に回答をリセット
    st.session_state.nlp_answer = ""
    st.session_state.page = page

def nlp_pages():
    # 1-1: 自然言語処理イントロ (変更なし)
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

    # 1-2: 自然言語処理体験（会話ページ）
    elif st.session_state.page == "自然言語処理体験":
        st.header("AIアシスタントに質問してみよう！")

        col1, col2 = st.columns([1, 2])

        with col1:
            # 簡単なAIアシスタントのイラスト
            st.markdown("""
            <div style="font-family: monospace; font-size: 8px; line-height: 1.2; text-align: center; margin-top: 20px;">
            <pre>
     .---.
    / o o \\
   |  ^  |
    \\ = /
     `---`
   /  |  \\
  |   |   |
  `-------`
            </pre>
            </div>
            """, unsafe_allow_html=True)
            st.caption("AIアシスタント")

        with col2:
            st.write("こんにちは！ 私はAIアシスタントです。AIや言葉について、どんなことに興味がありますか？下のリストから質問を選んでください。")

            questions = [
                "AI技術は日常生活をどう変えているの？",
                "AIと人間の違いやAIの強みは？",
                "AIにできること、できないことは？",
                "AIへの良い質問の仕方は？",
                "AIはどうやって言葉を理解しているの？(簡潔版)",
                "AIはどうやって言葉を理解しているの？(詳細版)"
            ]
            
            selected_question = st.radio(
                "質問リスト:",
                questions,
                label_visibility="collapsed" # ラベルを非表示にしてスッキリ見せる
            )

            # 「質問する」ボタンが押されたときの処理
            if st.button("この内容で質問する"):
                with st.spinner("AIが回答を考えています..."):
                    time.sleep(1.5)
                
                # 選ばれた質問に応じて回答を準備
                if selected_question == questions[0]:
                    st.session_state.nlp_answer = "例えば、スマートフォンの音声アシスタントや、動画サイトのおすすめ機能、お店の自動翻訳機など、多くの場所でAI技術が使われ、私たちの生活を便利にしています。"
                elif selected_question == questions[1]:
                    st.session_state.nlp_answer = "人間は感情や経験から柔軟に考えられますが、AIは大量のデータを正確に高速で処理するのが得意です。疲れを知らない点もAIの強みと言えます。"
                elif selected_question == questions[2]:
                    st.session_state.nlp_answer = "AIは、ルールが明確な計算やデータ分析は得意ですが、人の気持ちを完全に理解したり、全く新しいものをゼロから創造したりすることはまだ難しいとされています。"
                elif selected_question == questions[3]:
                    st.session_state.nlp_answer = "AIに質問する時は、「何について」「どんな情報が欲しいか」を具体的に、そして明確な言葉で聞くと、より的確な答えが返ってきやすいです。背景情報も加えるとさらに良いでしょう。"
                elif selected_question == questions[4]:
                    st.session_state.nlp_answer = "AIは、たくさんの文章データを読んで、「この単語の後にはこの単語が来やすい」といった言葉のパターンを統計的に学習します。それによって、文の意味を予測したり、文章を生成したりしています。"
                elif selected_question == questions[5]:
                    st.session_state.nlp_answer = "より詳しく言うと、AIは単語を「ベクトル」という数字の集まりに変換します。似た意味の単語は近い数字のベクトルになり、AIはこの数字の関係性から文全体の意味を計算します。この技術を「単語埋め込み」と呼び、自然言語処理の基礎となっています。"
            
            # 回答がセッション情報にあれば表示
            if st.session_state.nlp_answer:
                st.info(st.session_state.nlp_answer)

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