import streamlit as st
import os
import time
from PIL import Image

# --- セッション管理の初期化 ---
if "selected_index" not in st.session_state:
    st.session_state.selected_index = 0

def go_to(page):
    st.session_state.page = page

def image_pages():
    # 2-1: 画像分類イントロ（既存・軽整形）
    if st.session_state.page == "画像分類イントロ":
        st.markdown('<div class="label-chip">👀 画像を見るAI</div>', unsafe_allow_html=True)
        st.header("画像分類（Vision）とは？")
        st.markdown(
            """
<div class="card-text" style="font-size:1.05rem; line-height:1.9;">
画像分類とは、画像の内容を AI が判別する技術です。  
「犬の写真を見せて“犬”と答える」など、さまざまな分野で使われています。
</div>
<br>
<div class="card-text" style="font-size:1.05rem; line-height:1.9;">
今回は <b>犬の画像</b> を題材に、AIが特徴を拾い、どのように答えへたどり着くのかを体験してみましょう。
</div>
""",
            unsafe_allow_html=True,
        )
        st.markdown("<div style='height:0.6rem;'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            st.button("▶  体験スタート", on_click=go_to, args=("画像分類体験",), use_container_width=True)
        with col2:
            st.button("←  タイトルに戻る", on_click=go_to, args=("タイトル",), use_container_width=True)

    # 2-2: 画像分類体験（★カード風に・st.imageで確実表示）
    elif st.session_state.page == "画像分類体験":
        st.header("画像分類を体験しよう！")
        st.write("下の6枚から1つ選んで「決定」を押してください。ホバーでプレビューがふわっと浮きます。")

        image_paths = [
            "selectable_1.webp", "selectable_2.png", "selectable_3.png",
            "selectable_4.png", "selectable_5.png", "selectable_6.png"
        ]
        options = [f"画像{i+1}" for i in range(len(image_paths))]

        def set_selection_and_navigate():
            selected_option = st.session_state.radio_selector
            idx = options.index(selected_option)
            st.session_state.selected_index = idx
            st.session_state.page = "画像分類アニメ"

        # --- CSS: st.image にカード風スタイルを適用 ---
        st.markdown("""
        <style>
        /* 画像カードの見た目（角丸・影・ホバーで拡大） */
        div[data-testid="stImage"] img {
            border-radius: 14px;
            border: 2px solid transparent;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            transition: transform .18s ease, box-shadow .2s ease, border-color .2s ease;
        }
        div[data-testid="stImage"]:hover img {
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 10px 24px rgba(0,0,0,0.12);
            border-color: rgba(20,184,166,0.55); /* ティール系アクセント */
        }
        .thumb-label {
            text-align: center;
            padding-top: .35rem;
            font-weight: 700;
            color: #0f172a;
        }
        </style>
        """, unsafe_allow_html=True)

        # 3カラム×2段のグリッドで表示（st.image を使用）
        cols = st.columns(3, gap="large")
        for i, path in enumerate(image_paths):
            col = cols[i % 3]
            with col:
                if os.path.exists(path):
                    st.image(path, use_container_width=True)
                    st.markdown(f"<div class='thumb-label'>{options[i]}</div>", unsafe_allow_html=True)
                else:
                    st.error(f"エラー: '{path}' が見つかりません。")

        st.divider()
        st.radio("分析したい画像を1枚選んでください：", options, key="radio_selector", horizontal=True)
        st.button("✅  この画像で決定", on_click=set_selection_and_navigate, use_container_width=True)
        st.divider()
        colb1, colb2 = st.columns(2)
        with colb1:
            st.button("◀  前のページへ戻る", on_click=go_to, args=("画像分類イントロ",), use_container_width=True)
        with colb2:
            st.button("🏠  タイトルに戻る", on_click=go_to, args=("タイトル",), use_container_width=True)

    # 2-3: 画像分類アニメ（既存）
    elif st.session_state.page == "画像分類アニメ":
        st.header("AIが画像を分析中...")
        progress_bar = st.progress(0, "AIが画像の特徴を調べています...")
        for i in range(100):
            time.sleep(0.03)
            progress_bar.progress(i + 1)
        st.success("分析が完了しました！")

        def navigate_to_result():
            idx = st.session_state.selected_index
            next_page = f"画像分類結果_{idx + 1}_1"
            go_to(next_page)

        st.button("結果を見る", on_click=navigate_to_result, use_container_width=True)

    # 2-5: 画像分類まとめ（既存）
    elif st.session_state.page == "画像分類まとめ":
        st.header("画像分類まとめ")
        st.success("体験お疲れ様でした！")
        st.write("今回は、AIが犬の画像を見分ける体験をしました。")
        st.button("最後の解説へ ▶", on_click=go_to, args=("画像分類追加_1",), use_container_width=True)
        st.divider()
        st.button("もう一度体験する", on_click=go_to, args=("画像分類体験",), use_container_width=True)
        st.button("タイトルに戻る", on_click=go_to, args=("タイトル",), use_container_width=True)

    # 2-6: 追加ページ1（既存）
    elif st.session_state.page == "画像分類追加_1":
        st.header("解説 1/3")
        path = "extra_1.png"
        if os.path.exists(path):
            st.image(path, use_container_width=True)
        else:
            st.error(f"エラー: 画像ファイル '{path}' が見つかりません。")
        st.button("次へ ▶", on_click=go_to, args=("画像分類追加_2",), use_container_width=True)

    # 2-7: 追加ページ2（既存）
    elif st.session_state.page == "画像分類追加_2":
        st.header("解説 2/3")
        path = "extra_2.png"
        if os.path.exists(path):
            st.image(path, use_container_width=True)
        else:
            st.error(f"エラー: 画像ファイル '{path}' が見つかりません。")
        col1, col2 = st.columns(2)
        with col1:
            st.button("◀ 戻る", on_click=go_to, args=("画像分類追加_1",), use_container_width=True)
        with col2:
            st.button("次へ ▶", on_click=go_to, args=("画像分類追加_3",), use_container_width=True)

    # 2-8: 追加ページ3（既存）
    elif st.session_state.page == "画像分類追加_3":
        st.header("解説 3/3")
        path = "extra_3.png"
        if os.path.exists(path):
            st.image(path, use_container_width=True)
        else:
            st.error(f"エラー: 画像ファイル '{path}' が見つかりません。")
        col1, col2 = st.columns(2)
        with col1:
            st.button("◀ 戻る", on_click=go_to, args=("画像分類追加_2",), use_container_width=True)
        with col2:
            st.button("タイトルに戻る", on_click=go_to, args=("タイトル",), use_container_width=True)

    # 2-4: 各結果ページ（スライドショー）
    for choice_idx in range(1, 7):
        for page_num in range(1, 6):
            page_name = f"画像分類結果_{choice_idx}_{page_num}"
            if st.session_state.page == page_name:
                st.header(f"分析結果：画像 {choice_idx} ({page_num}/5)")

                result_image_path = f"result_{choice_idx}_{page_num}.png"
                if os.path.exists(result_image_path):
                    image = Image.open(result_image_path)
                    st.image(image, caption=f"画像{choice_idx} の分析結果 {page_num}", use_container_width=True)
                else:
                    st.error(f"エラー: 結果画像ファイル '{result_image_path}' が見つかりません。")

                col1, col2 = st.columns(2)
                with col1:
                    if page_num > 1:
                        prev_page = f"画像分類結果_{choice_idx}_{page_num - 1}"
                        st.button("◀ 戻る", on_click=go_to, args=(prev_page,), use_container_width=True)
                    else:
                        st.button("◀ 選択画面に戻る", on_click=go_to, args=("画像分類体験",), use_container_width=True)
                with col2:
                    if page_num < 5:
                        next_page = f"画像分類結果_{choice_idx}_{page_num + 1}"
                        st.button("次へ ▶", on_click=go_to, args=(next_page,), use_container_width=True)
                    else:
                        st.button("まとめへ ▶", on_click=go_to, args=("画像分類まとめ",), use_container_width=True)

                return
