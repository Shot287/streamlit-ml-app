import streamlit as st
from PIL import Image
import os
import time

os.makedirs("demo_images", exist_ok=True)

PAGES = [
    "タイトル",
    "自然言語処理イントロ",  # 1-1
    "自然言語処理体験",    # 1-2
    "自然言語処理まとめ",  # 1-3
    "画像分類イントロ",    # 2-1
    "犬の画像分類",        # 2-2
    "画像分類アニメ",      # 2-3
    "画像分類結果",        # 2-4
    "GRAD-CAM解説",
    "スライド資料",
]

# --- セッション初期化 ---
if "page" not in st.session_state:
    st.session_state.page = "タイトル"
if "selected_img" not in st.session_state:
    st.session_state.selected_img = None
if "img_index" not in st.session_state:
    st.session_state.img_index = 0
if "anim_done" not in st.session_state:
    st.session_state.anim_done = False

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

# --- 1-1 自然言語処理イントロ ---
elif st.session_state.page == "自然言語処理イントロ":
    st.header("自然言語処理とは？")
    st.write("""
自然言語処理（NLP）は、人間の言葉（日本語や英語など）をコンピュータが理解し、分析するAI技術です。
たとえば、文章から意味を読み取ったり、感情分析をしたり、要約や翻訳もNLPの応用です。
""")
    st.button("体験スタート", on_click=go_to, args=("自然言語処理体験",), use_container_width=True)
    st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
    st.markdown("<div style='text-align:center;'>1-1</div>", unsafe_allow_html=True)

# --- 1-2 自然言語処理体験 ---
elif st.session_state.page == "自然言語処理体験":
    st.header("自然言語処理体験")
    st.write("（ここに自然言語処理体験の内容を実装できます）")
    st.button("前のページへ戻る", on_click=go_to, args=("自然言語処理イントロ",))
    st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
    st.markdown("<div style='text-align:center;'>1-2</div>", unsafe_allow_html=True)

# --- 1-3 自然言語処理まとめ（必要なら）---
elif st.session_state.page == "自然言語処理まとめ":
    st.header("自然言語処理まとめ")
    st.write("（まとめ・ふりかえりページ。必要なら追加してください）")
    st.button("前のページへ戻る", on_click=go_to, args=("自然言語処理体験",))
    st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
    st.markdown("<div style='text-align:center;'>1-3</div>", unsafe_allow_html=True)

# --- 2-1 画像分類イントロ ---
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

# --- 2-2 犬の画像分類（画像選択）---
elif st.session_state.page == "犬の画像分類":
    st.header("犬の画像分類を体験しよう！")
    st.write("下の6枚から好きな犬の画像を選んで、AIの予測を見てみましょう。")
    demo_imgs = sorted([
        f for f in os.listdir("demo_images")
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ])[:6]
    cols = st.columns(3)
    for i in range(6):
        col = cols[i % 3]
        with col:
            if i < len(demo_imgs):
                img_path = os.path.join("demo_images", demo_imgs[i])
                if st.button(f"画像{i+1}", key=f"img_btn_{i}"):
                    st.session_state.selected_img = img_path
                    st.session_state.img_index = i
                    st.session_state.anim_done = False
                    st.session_state.page = "画像分類アニメ"
                    st.experimental_rerun()  # ← ココが絶対に必要！
                st.image(img_path, caption=f"犬の画像{i+1}", use_column_width=True)
            else:
                st.markdown(
                    f"""<div style="border:2px dashed #bbb; width:100%; height:160px;
                    display:flex; align-items:center; justify-content:center; margin-bottom:8px;">
                    <span style="color:#bbb;">画像をここに追加</span></div>""", unsafe_allow_html=True)
                st.button(f"画像{i+1}", key=f"dummy_btn_{i}")
    st.button("前のページへ戻る", on_click=go_to, args=("画像分類イントロ",))
    st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
    st.markdown("<div style='text-align:center;'>2-2</div>", unsafe_allow_html=True)

# --- 2-3 画像分類アニメーション ---
elif st.session_state.page == "画像分類アニメ":
    st.header("AIが画像を分類中…")
    st.write("AIが一生懸命考えています。しばらくお待ちください。")
    img_path = st.session_state.selected_img
    if img_path:
        st.image(img_path, caption="選択した画像", width=250)
    progress = st.empty()
    percent_text = st.empty()
    if not st.session_state.anim_done:
        for i in range(0, 101, 5):
            progress.progress(i)
            percent_text.markdown(f"<div style='font-size:2em; text-align:center;'>{i}%</div>", unsafe_allow_html=True)
            time.sleep(0.05)
        st.session_state.anim_done = True
        percent_text.markdown("<div style='font-size:2em; text-align:center;'>完了！</div>", unsafe_allow_html=True)
    else:
        progress.progress(100)
        percent_text.markdown("<div style='font-size:2em; text-align:center;'>完了！</div>", unsafe_allow_html=True)
    st.button("結果を見る", on_click=go_to, args=("画像分類結果",))
    st.markdown("<div style='text-align:center;'>2-3</div>", unsafe_allow_html=True)

# --- 2-4 画像分類結果 ---
elif st.session_state.page == "画像分類結果":
    st.header("AIの画像分類結果！")
    img_path = st.session_state.selected_img
    img_index = getattr(st.session_state, "img_index", 0)
    if img_path:
        st.image(img_path, caption="あなたが選んだ画像", width=300)
    results = [
        ("柴犬", "特徴的な巻き尾と立ち耳を持つ日本犬です。"),
        ("ダックスフント", "胴が長くて足が短いのが特徴の人気犬種です。"),
        ("プードル", "巻き毛が特徴。知能も高くペットとして人気です。"),
        ("チワワ", "世界最小クラスの小型犬。大きな目と耳がチャームポイント。"),
        ("ポメラニアン", "ふわふわの毛並みと活発な性格が魅力です。"),
        ("ビーグル", "垂れ耳が特徴の猟犬。嗅覚が非常に優れています。"),
    ]
    dog_class, description = results[img_index % len(results)]
    st.success(f"AIの判定: **{dog_class}**")
    st.write(description)
    st.info("推論の根拠は『GRAD-CAM解説』ページで見てみよう。")
    st.button("もう一度画像分類へ", on_click=go_to, args=("犬の画像分類",))
    st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
    st.markdown("<div style='text-align:center;'>2-4</div>", unsafe_allow_html=True)

# --- GRAD-CAM解説ページ ---
elif st.session_state.page == "GRAD-CAM解説":
    st.header("AIの判断根拠を見てみよう！（GRAD-CAM）")
    st.write("AIが画像のどこを見て判断したのか、色で可視化します。")
    st.write("（ここにGRAD-CAMの画像や解説を実装できます）")
    st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))

# --- スライド資料ページ ---
elif st.session_state.page == "スライド資料":
    st.header("スライド資料")
    st.write("（ここにスライド資料の内容を実装できます）")
    st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
