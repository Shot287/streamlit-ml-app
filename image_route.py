import streamlit as st
import os
if "selected_img" not in st.session_state:
    st.session_state.selected_img = None
if "img_index" not in st.session_state:
    st.session_state.img_index = 0

os.makedirs("demo_images", exist_ok=True)

def go_to(page):
    st.session_state.page = page

def image_pages():
    # 2-1
    if st.session_state.page == "画像分類イントロ":
        st.header("画像分類とは？")
        st.write("""
画像分類とは、画像の内容をAIが判別する技術です。
「犬の写真を見せて“犬”と答える」など、様々な分野で使われています。
今回は犬の画像を分類するAIを体験できます。
""")
        st.button("犬の画像分類", on_click=go_to, args=("犬の画像分類",))
        st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
        st.markdown("<div style='text-align:center;'>2-1</div>", unsafe_allow_html=True)

    # 2-2
    elif st.session_state.page == "犬の画像分類":
        st.header("犬の画像分類を体験しよう！")
        st.write("下の6枚から好きな画像を選ぼう！")
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
                        st.session_state.page = "画像分類アニメ"
                        st.experimental_rerun()
                    st.image(img_path, caption=f"犬の画像{i+1}", use_column_width=True)
                else:
                    st.markdown(
                        "<div style='border:2px dashed #bbb; width:100%; height:160px; display:flex; align-items:center; justify-content:center; margin-bottom:8px;'><span style='color:#bbb;'>画像をここに追加</span></div>",
                        unsafe_allow_html=True
                    )
                    st.button(f"画像{i+1}", key=f"dummy_btn_{i}")
        st.button("前のページへ戻る", on_click=go_to, args=("画像分類イントロ",))
        st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
        st.markdown("<div style='text-align:center;'>2-2</div>", unsafe_allow_html=True)


    # 2-3
    elif st.session_state.page == "画像分類アニメ":
        st.header("画像を受け取りました！")
        st.write("AIが画像を受け取りました。下のボタンで結果を見てみましょう。")
        img_path = st.session_state.selected_img
        if img_path:
            st.image(img_path, caption="選択した画像", width=250)
        st.button("結果を見る", on_click=go_to, args=("画像分類結果",))
        st.markdown("<div style='text-align:center;'>2-3</div>", unsafe_allow_html=True)

    # 2-4
    elif st.session_state.page == "画像分類結果":
        st.header("AIの画像分類結果！")
        img_path = st.session_state.selected_img
        img_index = st.session_state.img_index
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
        st.button("もう一度画像分類へ", on_click=go_to, args=("犬の画像分類",))
        st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
        st.markdown("<div style='text-align:center;'>2-4</div>", unsafe_allow_html=True)
