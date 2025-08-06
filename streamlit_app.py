import streamlit as st
from PIL import Image
import os

# --- ページ名定義 ---
PAGES = ["タイトル", "自然言語処理", "画像分類", "GRAD-CAM解説", "スライド資料"]

# --- 初期化 ---
if "page" not in st.session_state:
    st.session_state.page = "タイトル"

def go_to(page):
    st.session_state.page = page

# --- 1. タイトル画面 ---
if st.session_state.page == "タイトル":
    st.markdown(
        """
        <div style='text-align:center; margin-top:60px;'>
            <h1 style='font-size:3em;'>機械学習・AI体験</h1>
            <p style='font-size:1.5em;'>好きな体験を選ぼう！</p>
        </div>
        """, unsafe_allow_html=True
    )

    # ボタンを中央寄せ＋大きめに
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.button("自然言語処理", on_click=go_to, args=("自然言語処理",), use_container_width=True)
        st.button("画像分類", on_click=go_to, args=("画像分類",), use_container_width=True)

    st.markdown(
        "<div style='text-align:center; margin-top:40px;'><small>©️ 2025 機械学習体験アプリ</small></div>",
        unsafe_allow_html=True
    )

# --- 2. 自然言語処理体験ページ（サンプル） ---
elif st.session_state.page == "自然言語処理":
    st.header("自然言語処理体験")
    st.write("ここに自然言語処理の体験内容を実装します。")
    st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))

# --- 3. 画像分類体験ページ ---
elif st.session_state.page == "画像分類":
    st.header("画像分類を体験しよう！")
    st.write("高校生に画像を選んでもらい、AIの予測を確認します。")
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
        possible_classes = ["猫", "犬", "鳥"]
        pred_class = random.choice(possible_classes)  # ダミー
        st.success(f"AIの予測結果: **{pred_class}**")
        st.info("推論結果の理由や根拠はGRAD-CAMページで！")

    st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))

# --- 4. GRAD-CAM解説ページ（必要ならボタンから遷移可に拡張してください） ---
elif st.session_state.page == "GRAD-CAM解説":
    st.header("AIの判断根拠を見てみよう！（GRAD-CAM）")
    st.write("AIが画像のどこを見て判断したのか、色で可視化します。")
    gradcam_imgs = sorted([
        f for f in os.listdir("gradcam_images")
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ])
    if not gradcam_imgs:
        st.warning("GRAD-CAM画像がありません。gradcam_images フォルダに画像を追加してください。")
        st.info("実際には、画像分類体験で使った画像＋推論クラスごとにGRAD-CAM画像を用意し、ここで表示します。")
    else:
        gradcam_choice = st.selectbox("GRAD-CAM画像を選んでください", gradcam_imgs)
        gradcam_path = os.path.join("gradcam_images", gradcam_choice)
        st.image(gradcam_path, caption="GRAD-CAM可視化", use_column_width=True)
        st.caption("赤い部分ほどAIが重視した領域です。人間の着目点と比べてみましょう。")

    st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))

# --- 5. スライド資料ページ（もし必要ならここも） ---
elif st.session_state.page == "スライド資料":
    slide_files = sorted([
        f for f in os.listdir("slides")
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ])
    if not slide_files:
        st.error("スライド画像がありません。slides フォルダに画像を追加してください。")
    else:
        slide_num = st.slider("スライド番号", 1, len(slide_files), 1)
        slide_path = os.path.join("slides", slide_files[slide_num-1])
        st.image(slide_path, use_column_width=True)
        st.caption(f"{slide_num}/{len(slide_files)}")
    st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
