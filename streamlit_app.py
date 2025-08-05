import streamlit as st
from PIL import Image
import os

# --- 設定 ---
SLIDE_DIR = "slides"
DEMO_IMG_DIR = "demo_images"
GRAD_CAM_DIR = "gradcam_images"  # GRAD-CAM画像はここに出力保存しておくと楽

# --- サイドバー：ページ切替 ---
page = st.sidebar.radio(
    "ページ選択",
    ["スライド資料", "画像分類体験", "GRAD-CAM解説"]
)

# --- 1. スライド資料ページ ---
if page == "スライド資料":
    slide_files = sorted([
        f for f in os.listdir(SLIDE_DIR)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ])
    if not slide_files:
        st.error("スライド画像がありません。slides フォルダに画像を追加してください。")
    else:
        slide_num = st.slider("スライド番号", 1, len(slide_files), 1)
        slide_path = os.path.join(SLIDE_DIR, slide_files[slide_num-1])
        st.image(slide_path, use_column_width=True)
        st.caption(f"{slide_num}/{len(slide_files)}")

# --- 2. 画像分類体験ページ ---
elif page == "画像分類体験":
    st.header("画像分類を体験しよう！")
    st.write("高校生に画像を選んでもらい、AIの予測を確認します。")
    demo_imgs = sorted([
        f for f in os.listdir(DEMO_IMG_DIR)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ])
    if not demo_imgs:
        st.error("デモ画像がありません。demo_images フォルダに画像を追加してください。")
    else:
        # 画像選択
        img_choice = st.selectbox("画像を選んでください", demo_imgs)
        img_path = os.path.join(DEMO_IMG_DIR, img_choice)
        st.image(img_path, caption="選択画像", width=300)

        # --- ★ここに推論ロジックを組み込む（ダミー実装）---
        # 実際はここでAIモデルをロードして推論
        import random
        possible_classes = ["猫", "犬", "鳥"]
        pred_class = random.choice(possible_classes)  # ダミー: ランダム予測
        st.success(f"AIの予測結果: **{pred_class}**")

        # 推論結果の理由や根拠はGRAD-CAMページで！

# --- 3. GRAD-CAM解説ページ ---
elif page == "GRAD-CAM解説":
    st.header("AIの判断根拠を見てみよう！（GRAD-CAM）")
    st.write("AIが画像のどこを見て判断したのか、色で可視化します。")
    gradcam_imgs = sorted([
        f for f in os.listdir(GRAD_CAM_DIR)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ])
    if not gradcam_imgs:
        st.warning("GRAD-CAM画像がありません。gradcam_images フォルダに画像を追加してください。")
        st.info("実際には、画像分類体験で使った画像＋推論クラスごとにGRAD-CAM画像を用意し、ここで表示します。")
    else:
        gradcam_choice = st.selectbox("GRAD-CAM画像を選んでください", gradcam_imgs)
        gradcam_path = os.path.join(GRAD_CAM_DIR, gradcam_choice)
        st.image(gradcam_path, caption="GRAD-CAM可視化", use_column_width=True)
        st.caption("赤い部分ほどAIが重視した領域です。人間の着目点と比べてみましょう。")

# --- 備考 ---
st.sidebar.markdown("---")
st.sidebar.write("©️ 2025 機械学習体験アプリ")

