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

    elif st.session_state.page == "犬の画像分類":
        st.header("犬の画像分類を体験しよう！")
        st.write("下の6枚から好きな画像を選ぼう！")
        demo_imgs = sorted([
            f for f in os.listdir("demo_images")
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ])[:6]
        cols = st.columns(3)
        clicked = None
        clicked_img = None
        for i in range(6):
            col = cols[i % 3]
            with col:
                btn_label = f"画像{i+1}"
                btn_key = f"img_btn_{i}_2_2"
                img_path = os.path.join("demo_images", demo_imgs[i]) if i < len(demo_imgs) else None
                if st.button(btn_label, key=btn_key):
                    clicked = i
                    clicked_img = img_path
                if img_path:
                    st.image(img_path, caption=f"犬の画像{i+1}", use_column_width=True)
                else:
                    st.markdown(
                        "<div style='border:2px dashed #bbb; width:100%; height:160px; "
                        "display:flex; align-items:center; justify-content:center; margin-bottom:8px;'>"
                        "<span style='color:#bbb;'>画像をここに追加</span></div>",
                        unsafe_allow_html=True
                    )
        # forループ外でボタン判定＆ワンクリックでページ遷移
        if clicked is not None:
            st.session_state.selected_img = clicked_img
            st.session_state.img_index = clicked
            st.session_state.page = "画像分類アニメ"
            st.experimental_rerun()
            return

        st.button("前のページへ戻る", on_click=go_to, args=("画像分類イントロ",))
        st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
        st.markdown("<div style='text-align:center;'>2-2</div>", unsafe_allow_html=True)

    elif st.session_state.page == "画像分類アニメ":
        st.button("前のページへ戻る", on_click=go_to, args=("犬の画像分類",))
        st.markdown("<div style='text-align:center;'>2-3</div>", unsafe_allow_html=True)

    elif st.session_state.page == "画像分類結果":
        pass
