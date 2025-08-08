import streamlit as st
import os
import time
from PIL import Image

# --- セッション管理の初期化 ---
if "nlp_stage" not in st.session_state:
    st.session_state.nlp_stage = "selection"
if "selected_nlp_question_index" not in st.session_state:
    st.session_state.selected_nlp_question_index = 0

def go_to(page):
    # ページを移動する際に進行状況をリセット
    if page == "自然言語処理体験":
        st.session_state.nlp_stage = "selection"
    st.session_state.page = page

def nlp_pages():
    # 質問と回答のリストを定義
    questions = [
        "最近、AI技術がどのように私たちの日常生活を変えているのか、具体的な例を交えて教えてください。",
        "AIと人間の違いやAIの強みについて、わかりやすく説明してください。",
        "AIにできること、できないことについて、具体例を交えて説明してください。",
        "AIに質問するとき、どんな聞き方をすると正確で分かりやすい答えが返ってきやすいですか？",
        "AIはどうやって人間の言葉を理解しているのか、その仕組みをできるだけ詳しく説明してください。",
        "AIと対話することで、どんなことが学べるのか、AIとの会話の活用例を教えてください。"
    ]
    answers = [
        "AI技術は、検索エンジンの精度向上やスマートスピーカーによる音声アシスタント、自動運転技術など、さまざまな場面で私たちの生活をより便利にしています。たとえば、AIはネットショッピングで好みを学習し、あなたに合った商品をおすすめしたり、スマートフォンで写真を自動的に分類する役割も担っています。こうした進化によって、日々の生活が効率化され、私たちがより快適に暮らせるようになっています。",
        "AIは大量のデータを短時間で処理し、パターンを見つけて正確に判断することが得意です。一方で、創造性や感情を持たず、自分で目的を考えることはできません。人間は経験や直感、感情に基づいた柔軟な判断ができますが、計算やデータ処理はAIのほうが圧倒的に速いです。AIの強みは、繰り返し作業や大量データの分析など、効率化できる分野に特に発揮されます。",
        "AIには画像認識や翻訳、ゲームの攻略、文章の要約など、さまざまなことができます。例えば、医療分野では画像から異常を発見したり、カメラで写した文字を読み取って翻訳したりします。しかし、完全な創造的活動や人の気持ちを正確に理解すること、未知の状況に自律的に適応することはまだ難しいです。AIはあくまで人間のサポート役として活用されています。",
        "AIに質問するときは、できるだけ具体的で短く、目的や条件をはっきり伝えると良いです。たとえば『ダイエットにおすすめの食事メニューを3つ教えてください』のように、具体的な数や条件があると正確に答えやすくなります。あいまいな質問よりも、明確なゴールを示すことで、AIはより適切な情報を返すことができます。",
        "AIは膨大なテキストデータからパターンを学習し、人間の言葉を統計的に処理しています。単語や文の意味、文脈を数値データとして捉え、ニューラルネットワークという技術を使って、あなたの質問の意図や意味を推測します。最近のAIは数百億の例文をもとに訓練されているので、多様な表現にも柔軟に対応できるようになっています。",
        "AIと対話することで、知識を調べたり、英語の練習をしたり、プログラミングのサポートを受けたりできます。自分の考えを言語化して整理したいときや、新しい発想がほしいときにもAIは役立ちます。また、趣味や興味に合わせて質問すれば、今まで知らなかった情報や学びに出会えるのも魅力のひとつです。"
    ]

    # 1-1: 自然言語処理イントロ（整形）
    if st.session_state.page == "自然言語処理イントロ":
        st.markdown('<div class="label-chip">🧠 言葉を理解するAI</div>', unsafe_allow_html=True)
        st.header("自然言語処理（NLP）とは？")

        st.markdown(
            """
<div class="card-text" style="font-size:1.05rem; line-height:1.9;">
自然言語処理（NLP）は、人間の言葉（自然言語）をコンピュータが理解・分析するAI技術です。  
文章の意味を読み取ったり、要約や翻訳をしたりと、さまざまな場面で活躍しています。
</div>
<br>
<div class="card-text" style="font-size:1.05rem; line-height:1.9;">
今回は AI アシスタントに質問をして、<b>AIがどのように言葉を捉えて答えを作るのか</b>を体験してみましょう。
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height:0.6rem;'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            st.button("▶  体験スタート", on_click=go_to, args=("自然言語処理体験",), use_container_width=True)
        with col2:
            st.button("←  タイトルに戻る", on_click=go_to, args=("タイトル",), use_container_width=True)

    # 1-2: 自然言語処理体験（選択画面をカード風に）
    elif st.session_state.page == "自然言語処理体験":
        st.header("AIアシスタントへの質問")

        # --- カード風ラジオのCSS ---
        st.markdown("""
        <style>
        div[role='radiogroup'] > label {
            background: white;
            border-radius: 12px;
            padding: 0.75rem 1rem;
            margin-bottom: 0.6rem;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            border: 2px solid transparent;
            transition: all 0.15s ease;
            cursor: pointer;
        }
        div[role='radiogroup'] > label:hover {
            border-color: #38bdf8;
            box-shadow: 0 4px 12px rgba(56,189,248,0.2);
            transform: translateY(-1px);
        }
        div[role='radiogroup'] > label[data-selected="true"] {
            border-color: #0ea5e9;
            background: #f0f9ff;
            box-shadow: 0 4px 14px rgba(14,165,233,0.25);
        }
        </style>
        """, unsafe_allow_html=True)

        if st.session_state.nlp_stage == "selection":
            st.write("こんにちは！ 私はAIアシスタントです。AIや言葉について、どんなことに興味がありますか？下のリストから質問を選んでください。")

            st.radio(
                "質問リスト:",
                range(len(questions)),
                format_func=lambda i: questions[i],
                label_visibility="collapsed",
                key="selected_nlp_radio_index"
            )

            def decide_button_clicked():
                st.session_state.selected_nlp_question_index = st.session_state.selected_nlp_radio_index
                st.session_state.nlp_stage = "animation"

            st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
            st.button("✅  この質問で決定", on_click=decide_button_clicked, use_container_width=True)

        elif st.session_state.nlp_stage == "animation":
            st.info(f"**質問:**\n\n{questions[st.session_state.selected_nlp_question_index]}")
            st.write("---")
            st.write("AIが回答を考えています...")
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.02)
                progress_bar.progress(i + 1)
            st.session_state.nlp_stage = "show_button"
            st.rerun()

        elif st.session_state.nlp_stage == "show_button":
            st.info(f"**質問:**\n\n{questions[st.session_state.selected_nlp_question_index]}")
            st.write("---")
            st.success("回答の準備ができました！")
            def navigate_to_result():
                next_page_index = st.session_state.selected_nlp_question_index + 1
                next_page = f"自然言語処理結果_{next_page_index}"
                go_to(next_page)
            st.button("結果を見る", on_click=navigate_to_result, use_container_width=True)

        st.divider()
        st.button("タイトルに戻る", on_click=go_to, args=("タイトル",), use_container_width=True)

    elif st.session_state.page == "自然言語処理まとめ":
        st.header("自然言語処理まとめ")
        st.success("体験お疲れ様でした！")
        st.write("（まとめページの内容）")
        st.button("もう一度体験する", on_click=go_to, args=("自然言語処理体験",), use_container_width=True)
        st.button("タイトルに戻る", on_click=go_to, args=("タイトル",), use_container_width=True)

    # 1-3: 各結果ページ
    for i in range(1, 7):
        page_name = f"自然言語処理結果_{i}"
        if st.session_state.page == page_name:
            st.header(f"質問{i}への回答")
            st.info(answers[i-1])
            st.divider()
            st.button("AIの裏側を見る。", on_click=go_to, args=(f"自然言語処理_裏側_{i}",), use_container_width=True)
            st.button("もう一度質問を選ぶ", on_click=go_to, args=("自然言語処理体験",), use_container_width=True)
            st.button("タイトルに戻る", on_click=go_to, args=("タイトル",), use_container_width=True)
            return

    # 1-5: 「裏側」ページ
    for i in range(1, 7):
        page_name = f"自然言語処理_裏側_{i}"
        if st.session_state.page == page_name:
            st.header(f"質問{i}の「裏側」解説")

            st.subheader("AIの回答（再掲）")
            st.info(answers[i-1])
            st.divider()

            backside_image_paths = [
                "backside_1.png", "backside_2.png", "backside_3.png",
                "backside_4.png", "backside_5.png", "backside_6.png"
            ]
            path = backside_image_paths[i-1]

            if os.path.exists(path):
                st.image(path, caption="解説画像", use_container_width=True)
            else:
                st.error(f"エラー: 解説画像 '{path}' が見つかりません。")

            st.divider()
            st.button("◀ 回答に戻る", on_click=go_to, args=(f"自然言語処理結果_{i}",), use_container_width=True)
            st.button("タイトルに戻る", on_click=go_to, args=("タイトル",), use_container_width=True)
            return
