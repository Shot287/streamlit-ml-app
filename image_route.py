import streamlit as st
import os
import time
from PIL import Image

# --- セッション管理の初期化 ---
if "selected_img" not in st.session_state:
    st.session_state.selected_img = None
if "img_index" not in st.session_state:
    st.session_state.img_index = 0

# demo_imagesフォルダがなければ作成
os.makedirs("demo_images", exist_ok=True)

def go_to(page):
    st.session_state.page = page

def image_pages():
    # 2-1: 画像分類イントロ (変更なし)
    if st.session_state.page == "画像分類イントロ":
        st.header("画像分類とは？")
        st.write("""
        画像分類とは、画像の内容をAIが判別する技術です。
        「犬の写真を見せて“犬”と答える」など、様々な分野で使われています。
        今回は犬の画像を分類するAIを体験できます。
        """)
        st.button("犬の画像分類へ", on_click=go_to, args=("犬の画像分類",))
        st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
        st.markdown("<div style='text-align:center;'>2-1</div>", unsafe_allow_html=True)

    # 2-2: 犬の画像分類 (★★ここのロジックを修正★★)
    elif st.session_state.page == "犬の画像分類":
        st.header("犬の画像分類を体験しよう！")
        st.write("下の6枚から好きな画像を選び、「決定」ボタンを押してください。")

        # demo_imagesフォルダから画像リストを取得
        demo_imgs = sorted([
            f for f in os.listdir("demo_images")
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ])[:6]

        # 画像がない場合はエラー表示
        if not demo_imgs:
            st.error("`demo_images` フォルダに画像ファイルを追加してください。")
            st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
            return

        options = [f"画像{i+1}" for i in range(len(demo_imgs))]

        # --- ▼▼▼ 修正箇所 ▼▼▼ ---
        # 「決定」ボタンが押されたときに実行される関数
        def set_selection_and_navigate():
            # ラジオボタンで選択された値 (例: "画像3") を取得
            selected_option = st.session_state.radio_selector
            # 選択された値からインデックス番号 (例: 2) を特定
            idx = options.index(selected_option)

            # 選択された画像の情報をsession_stateに保存
            st.session_state.selected_img = os.path.join("demo_images", demo_imgs[idx])
            st.session_state.img_index = idx
            # 次のページへ遷移させる
            st.session_state.page = "画像分類アニメ"

        # 画像を3列で表示
        cols = st.columns(3)
        for i, img_file in enumerate(demo_imgs):
            with cols[i % 3]:
                st.image(os.path.join("demo_images", img_file), caption=f"犬の画像{i+1}", use_column_width=True)

        st.divider() # 区切り線

        # ラジオボタンと決定ボタンを配置
        st.radio("分析したい画像を1枚選んでください：", options, key="radio_selector", horizontal=True)
        st.button("決定", on_click=set_selection_and_navigate, use_container_width=True)
        # --- ▲▲▲ 修正箇所 ▲▲▲ ---

        st.divider()
        st.button("前のページへ戻る", on_click=go_to, args=("画像分類イントロ",))
        st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
        st.markdown("<div style='text-align:center;'>2-2</div>", unsafe_allow_html=True)


    # 2-3: 画像分類アニメ (変更なし)
    elif st.session_state.page == "画像分類アニメ":
        st.header("AIが画像を分析中...")
        if st.session_state.selected_img and os.path.exists(st.session_state.selected_img):
             image = Image.open(st.session_state.selected_img)
             st.image(image, caption="分析中の画像", width=300)

        progress_bar = st.progress(0, "AIが画像の特徴を調べています...")
        for i in range(100):
            time.sleep(0.03)
            progress_bar.progress(i + 1)
        progress_bar.empty()
        st.success("分析が完了しました！")
        time.sleep(1)
        go_to("画像分類結果")
        st.experimental_rerun()


    # 2-4: 画像分類結果 (変更なし)
    elif st.session_state.page == "画像分類結果":
        st.header("AIによる画像分類の結果")
        st.balloons()
        
        dog_breeds = {
            0: "柴犬", 1: "ゴールデン・レトリバー", 2: "コーギー",
            3: "トイ・プードル", 4: "チワワ", 5: "シベリアン・ハスキー"
        }
        result_breed = dog_breeds.get(st.session_state.img_index, "不明な犬種")

        if st.session_state.selected_img and os.path.exists(st.session_state.selected_img):
            image = Image.open(st.session_state.selected_img)
            st.image(image, caption="分析した画像")
            st.success(f"**AIの判定結果： この犬は「{result_breed}」です！**")
        else:
            st.error("画像が選択されていません。前のページに戻ってやり直してください。")

        st.button("体験のまとめへ", on_click=go_to, args=("画像分類まとめ",))
        st.button("前のページへ戻る", on_click=go_to, args=("犬の画像分類",))
        st.markdown("<div style='text-align:center;'>2-4</div>", unsafe_allow_html=True)

    # 2-5: 画像分類まとめ (変更なし)
    elif st.session_state.page == "画像分類まとめ":
        st.header("画像分類まとめ")
        st.success("体験お疲れ様でした！")
        st.write("""
        今回は、AIが犬の画像を見分ける体験をしました。
        実際のAIは、何万枚もの犬の画像を学習することで、様々な犬種や角度の画像でも見分けられるようになります。
        """)
        st.info("""
        **応用例**
        - スマートフォンの顔認証ロック
        - 医療画像の診断支援（例：レントゲン写真から病変を発見）
        - 自動運転車での障害物検知
        """)
        st.button("もう一度体験する", on_click=go_to, args=("犬の画像分類",))
        st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
        st.markdown("<div style='text-align:center;'>2-5</div>", unsafe_allow_html=True)