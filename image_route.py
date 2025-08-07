import streamlit as st
import os
import time
from PIL import Image

# --- セッション管理の初期化 ---
# 選択された画像のインデックス(0-5)を保存する変数
if "selected_index" not in st.session_state:
    st.session_state.selected_index = 0

def go_to(page):
    st.session_state.page = page

def image_pages():
    # 2-1: 画像分類イントロ
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

    # 2-2: 画像分類体験（画像選択ページ）
    elif st.session_state.page == "画像分類体験":
        st.header("画像分類を体験しよう！")
        st.write("下の6つの枠から好きなものを1つ選び、「決定」ボタンを押してください。")

        num_placeholders = 6
        options = [f"画像{i+1}" for i in range(num_placeholders)]

        # 「決定」ボタンが押されたときに実行される関数
        def set_selection_and_navigate():
            selected_option = st.session_state.radio_selector
            idx = options.index(selected_option)
            # 選択されたインデックスを保存
            st.session_state.selected_index = idx
            # アニメーションページへ遷移
            st.session_state.page = "画像分類アニメ"

        # 6つのプレースホルダーを3列で表示
        cols = st.columns(3)
        for i in range(num_placeholders):
            with cols[i % 3]:
                st.markdown(
                    f"""
                    <div style='border:2px dashed #bbb; border-radius: 5px; width:100%; height:160px;
                        display:flex; align-items:center; justify-content:center; margin-bottom:8px;
                        font-weight:bold; color:#bbb;'>
                    {options[i]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        st.divider()
        st.radio("分析したい画像を1枚選んでください：", options, key="radio_selector", horizontal=True)
        st.button("決定", on_click=set_selection_and_navigate, use_container_width=True)

        st.divider()
        st.button("前のページへ戻る", on_click=go_to, args=("画像分類イントロ",))
        st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
        st.markdown("<div style='text-align:center;'>2-2</div>", unsafe_allow_html=True)

    # 2-3: 画像分類アニメ
    elif st.session_state.page == "画像分類アニメ":
        st.header("AIが画像を分析中...")
        progress_bar = st.progress(0, "AIが画像の特徴を調べています...")
        for i in range(100):
            time.sleep(0.03)
            progress_bar.progress(i + 1)
        st.success("分析が完了しました！")
        time.sleep(1)

        # ★★ここからが分岐処理★★
        # 保存されたインデックスを基に、遷移先のページ名を動的に作成
        idx = st.session_state.selected_index
        next_page = f"画像分類結果_{idx + 1}"
        go_to(next_page)
        st.experimental_rerun() # ページを再読み込みして遷移を確定

    # 2-5: 画像分類まとめ
    elif st.session_state.page == "画像分類まとめ":
        st.header("画像分類まとめ")
        st.success("体験お疲れ様でした！")
        st.write("""
        今回は、AIが犬の画像を見分ける体験をしました。
        """)
        st.button("もう一度体験する", on_click=go_to, args=("画像分類体験",))
        st.button("タイトルに戻る", on_click=go_to, args=("タイトル",))
        st.markdown("<div style='text-align:center;'>2-5</div>", unsafe_allow_html=True)

    # 2-4: 各結果ページの生成
    # ループを使って6つの結果ページを動的に処理
    for i in range(1, 7):
        page_name = f"画像分類結果_{i}"
        if st.session_state.page == page_name:
            st.header(f"分析結果：画像 {i}")
            result_image_path = f"result_{i}.png" # 対応する結果画像ファイル名

            # 画像ファイルの存在を確認して表示
            if os.path.exists(result_image_path):
                image = Image.open(result_image_path)
                st.image(image, caption=f"画像{i} の分析結果", use_column_width=True)
            else:
                st.error(f"エラー: 結果画像ファイル '{result_image_path}' が見つかりません。")

            st.button("体験のまとめへ", on_click=go_to, args=("画像分類まとめ",))
            st.button("選択画面に戻る", on_click=go_to, args=("画像分類体験",))
            st.markdown(f"<div style='text-align:center;'>2-4-{i}</div>", unsafe_allow_html=True)
            break # 該当ページを処理したらループを抜ける