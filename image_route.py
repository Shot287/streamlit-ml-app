import streamlit as st
import os
import time
from PIL import Image

# --- セッション管理の初期化 ---
if "selected_img" not in st.session_state:
    st.session_state.selected_img = None
if "img_index" not in st.session_state:
    st.session_state.img_index = 0

# demo_imagesフォルダの存在確認は不要になったため削除

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
        st.button("体験スタート", on_click=go_to, args=("画像分類体験",))
        st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
        st.markdown("<div style='text-align:center;'>2-1</div>", unsafe_allow_html=True)

    # 2-2: 画像分類体験 (★★ここのロジックを修正★★)
    elif st.session_state.page == "画像分類体験":
        st.header("画像分類を体験しよう！")
        st.write("下の6つの枠から好きなものを1つ選び、「決定」ボタンを押してください。")

        # --- ▼▼▼ 修正箇所 ▼▼▼ ---
        # 画像ファイルに依存せず、固定で6つの選択肢を作成
        num_placeholders = 6
        options = [f"画像{i+1}" for i in range(num_placeholders)]

        # 「決定」ボタンが押されたときに実行される関数
        def set_selection_and_navigate():
            # ラジオボタンで選択された値 (例: "画像3") を取得
            selected_option = st.session_state.radio_selector
            # 選択された値からインデックス番号 (例: 2) を特定
            idx = options.index(selected_option)

            # 選択された画像のインデックスを保存（画像パスはNoneに）
            st.session_state.selected_img = None
            st.session_state.img_index = idx
            # 次のページへ遷移させる
            st.session_state.page = "画像分類アニメ"

        # 6つのプレースホルダーを3列で表示
        cols = st.columns(3)
        for i in range(num_placeholders):
            with cols[i % 3]:
                # HTMLとCSSで枠線を描画
                st.markdown(
                    f"""
                    <div style='
                        border:2px dashed #bbb;
                        border-radius: 5px;
                        width:100%;
                        height:160px;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        margin-bottom:8px;
                        font-weight:bold;
                        color:#bbb;
                    '>
                    {options[i]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.divider() # 区切り線
        st.radio("分析したい画像を1枚選んでください：", options, key="radio_selector", horizontal=True)
        st.button("決定", on_click=set_selection_and_navigate, use_container_width=True)
        # --- ▲▲▲ 修正箇所 ▲▲▲ ---

        st.divider()
        st.button("前のページへ戻る", on_click=go_to, args=("画像分類イントロ",))
        st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
        st.markdown("<div style='text-align:center;'>2-2</div>", unsafe_allow_html=True)


    # 2-3: 画像分類アニメ (変更なし)
    # selected_imgがNoneでもエラーにならないように元々設計されているため修正不要
    elif st.session_state.page == "画像分類アニメ":
        st.header("AIが画像を分析中...")
        # 選択された画像があれば表示する（今回はNoneなので表示されない）
        if st.session_state.selected_img and os.path.exists(st.session_state.selected_img):
             image = Image.open(st.session_state.selected_img)
             st.image(image, caption="分析中の画像", width=300)
        else:
             st.info("（画像なしで分析を実行します）")

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
    # selected_imgがNoneでもエラーにならないように元々設計されているため修正不要
    elif st.session_state.page == "画像分類結果":
        st.header("AIによる画像分類の結果")
        st.balloons()

        dog_breeds = {
            0: "柴犬", 1: "ゴールデン・レトリバー", 2: "コーギー",
            3: "トイ・プードル", 4: "チワワ", 5: "シベリアン・ハスキー"
        }
        # 保存されたインデックスを使って犬種を特定
        result_breed = dog_breeds.get(st.session_state.img_index, "不明な犬種")
        selected_option_name = f"画像{st.session_state.img_index + 1}"

        # 選択された画像があれば表示する（今回はNoneなので表示されない）
        if st.session_state.selected_img and os.path.exists(st.session_state.selected_img):
            image = Image.open(st.session_state.selected_img)
            st.image(image, caption="分析した画像")
        else:
            st.info(f"選択された枠: **{selected_option_name}**")

        st.success(f"**AIの判定結果： この犬は「{result_breed}」です！**")

        st.button("体験のまとめへ", on_click=go_to, args=("画像分類まとめ",))
        st.button("前のページへ戻る", on_click=go_to, args=("画像分類体験",))
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
        st.button("もう一度体験する", on_click=go_to, args=("画像分類体験",))
        st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
        st.markdown("<div style='text-align:center;'>2-5</div>", unsafe_allow_html=True)