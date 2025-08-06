import streamlit as st
from PIL import Image
import os

os.makedirs("demo_images", exist_ok=True)

# --- ページ名定義 ---
PAGES = [
    "タイトル",              # -
    "自然言語処理イントロ",   # 1-1
    "自然言語処理体験",       # 1-2
    "自然言語処理まとめ",     # 1-3（必要に応じて）
    "画像分類イントロ",       # 2-1
    "犬の画像分類",           # 2-2
    "画像分類まとめ",         # 2-3（必要に応じて）
    "GRAD-CAM解説",          # おまけ
    "スライド資料",           # おまけ
]

# --- 初期化 ---
if "page" not in st.session_state:
    st.session_state.page = "タイトル"

def go_to(page):
    st.session_state.page = page

# --- タイトル画面 ---
if st.session_state.page == "タイトル":
    st.markdown(
        """
        <div style='text-align:center; margin-top:60px;'>
            <h1 style='font-size:3em;'>機械学習・AI体験</h1>
            <p style='font-size:1.5em;'>好きな体験を選ぼう！</p>
        </div>
        """, unsafe_allow_html=True
    )
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.button("自然言語処理", on_click=go_to, args=("自然言語処理イントロ",), use_container_width=True)
        st.button("画像分類", on_click=go_to, args=("画像分類イントロ",), use_container_width=True)
    st.markdown(
        "<div style='text-align:center; margin-top:40px;'><small>©️ 2025 機械学習体験アプリ</small></div>",
        unsafe_allow_html=True
    )
    st.markdown("<div style='text-align:center;'>-</div>", unsafe_allow_html=True)

# --- 自然言語処理イントロページ（1-1）---
elif st.session_state.page == "自然言語処理イントロ":
    st.header("自然言語処理とは？")
    st.write("""
自然言語処理（NLP）は、人間の言葉（日本語や英語など）をコンピュータが理解し、分析するAI技術です。
たとえば、文章から意味を読み取ったり、感情分析をしたり、要約や翻訳もNLPの応用です。
""")
    st.button("体験スタート", on_click=go_to, args=("自然言語処理体験",), use_container_width=True)
    st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
    st.markdown("<div style='text-align:center;'>1-1</div>", unsafe_allow_html=True)

# --- 自然言語処理体験ページ（1-2）---
elif st.session_state.page == "自然言語処理体験":
    st.header("自然言語処理体験")
    st.write("（ここに自然言語処理体験の内容を実装できます）")
    st.button("前のページへ戻る", on_click=go_to, args=("自然言語処理イントロ",))
    st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
    st.markdown("<div style='text-align:center;'>1-2</div>", unsafe_allow_html=True)

# --- 画像分類イントロページ（2-1）---
elif st.session_state.page == "画像分類イントロ":
    st.header("画像分類とは？")
    st.write("""
画像分類とは、**画像に写っているものが何かをAIが判別する技術**です。  
たとえば、「犬の写真を見せて“犬”と答える」「猫と犬を区別する」といった応用が有名です。  
近年では、医療画像診断や自動運転、商品検索など、さまざまな分野で活躍しています。

今回は、実際にAIが犬の画像を分類する体験をしてみましょう！
    """)
    st.button("犬の画像分類", on_click=go_to, args=("犬の画像分類",), use_container_width=True)
    st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
    st.markdown("<div style='text-align:center;'>2-1</div>", unsafe_allow_html=True)

# --- 犬の画像分類体験ページ（2-2）---
elif st.session_state.page == "犬の画像分類":
    st.header("犬の画像分類を体験しよう！")
    st.write("好きな犬の画像を選び、AIの予測を見てみましょう。")
    demo_imgs = sorted([
        f for f in os.listdir("demo_images")
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ])
    if not demo_imgs:
        st.error("デモ画像がありません。demo_images フォルダに画像を追加してください。")
    else:
        img_choice = st.selectbox("画像を選んでください", demo_imgs)
        img_path = os.path.join("demo_images", img_choice)
        st.image(img_path, caption="選択画像", width=300)
        import random
        possible_classes = ["柴犬", "ダックスフント", "プードル", "チワワ"]
        pred_class = random.choice(possible_classes)
        st.success(f"AIの予測結果: **{pred_class}**")
        st.info("推論の根拠は『GRAD-CAM解説』ページで見てみよう。")
    st.button("前のページへ戻る", on_click=go_to, args=("画像分類イントロ",))
    st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
    st.markdown("<div style='text-align:center;'>2-2</div>", unsafe_allow_html=True)

# --- 必要に応じて 2-3, 1-3 など拡張も可能 ---
# --- GRAD-CAM解説・スライド資料ページは省略（従来通り） ---
