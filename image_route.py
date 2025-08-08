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
    # 2-1: 画像分類イントロ（既存）
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

    # 2-2: 画像分類体験（★ここを“かっこよく”）
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

        # --- 選択カード用CSS（軽やかなカード＋ホバーで拡大＆影、選択時に枠色） ---
        st.markdown("""
        <style>
        .img-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
        @media (max-width: 900px) { .img-grid { grid-template-columns: repeat(2, 1fr); } }
        @media (max-width: 600px) { .img-grid { grid-template-columns: 1fr; } }

        .image-card {
          position: relative;
          background: #ffffff;
          border-radius: 14px;
          overflow: hidden;
          border: 2px solid transparent;
          box-shadow: 0 2px 8px rgba(0,0,0,0.06);
          transition: transform .18s ease, box-shadow .2s ease, border-color .2s ease;
        }
        .image-card:hover {
          transform: translateY(-2px) scale(1.02);
          box-shadow: 0 10px 24px rgba(0,0,0,0.12);
          border-color: rgba(20,184,166,0.55); /* ティール系アクセント */
        }
        .image-card img { width: 100%; height: auto; display: block; }

        .image-label {
          padding: .55rem .8rem;
          background: #f8fafc;
          color: #0f172a;
          font-weight: 700;
          text-align: center;
        }

        /* 選択状態を視覚化：対応するラベルに data-selected="true" が付く */
        div[role='radiogroup'] > label[data-selected="true"] .image-card {
          border-color: #14b8a6;        /* 選択中の枠色 */
          box-shadow: 0 10px 26px rgba(20,184,166,0.25);
        }

        /* ラジオUI自体もカード化（ラベル全体をクリック可能に） */
        div[role='radiogroup'] { margin-top: .6rem; }
        div[role='radiogroup'] > label {
          background: transparent;
          border-radius: 14px;
          padding: 0;                   /* 画像カードの余白に委ねる */
          margin-bottom: .6rem;
          border: none;
          box-shadow: none;
        }

        /* 下部のラジオ横並びは隠してカードと重複しないように（代替：カード自体がラジオ） */
        /* 複数ブラウザでレイアウト崩れ回避のため、下の水平ラジオは非表示 */
        .horizontal-radio { display:none; }
        </style>
        """, unsafe_allow_html=True)

        # --- カード自体をラジオの選択肢にする ---
        # Streamlit のラジオは <label> 内に任意HTMLを置けるので、その中にカードを入れる
        # キー: selected_card_index
        selected_index = st.session_state.get("selected_card_index", 0)
        # カスタムラジオを作るため、options を range にして format_func でHTMLを返す
        def _format_option(i: int):
            path = image_paths[i]
            label = options[i]
            exists = os.path.exists(path)
            if exists:
                # 画像パスを埋め込んだカードHTML
                return f"""
                <div class="image-card">
                  <img src="{path}">
                  <div class="image-label">{label}</div>
                </div>
                """
            else:
                # 画像が無い場合は簡易プレースホルダ
                return f"""
                <div class="image-card" style="border-color:#ef4444">
                  <div class="image-label">ファイルなし: {label}</div>
                </div>
                """

        # ラジオ本体（カードをそのまま選択肢に）
        st.radio(
            "画像を選んでください",
            options=list(range(len(image_paths))),
            format_func=lambda i: _format_option(i),
            key="selected_card_index",
            label_visibility="collapsed"
        )

        # 旧来の水平ラジオを残す場合は以下を利用。ただし今回は非表示化している。
        # st.radio("分析したい画像を1枚選んでください：", options, key="radio_selector", horizontal=True)

        # 「決定」ボタン：カードの選択値（selected_card_index）を採用
        def _go_with_card_selection():
            st.session_state.selected_index = st.session_state.selected_card_index
            st.session_state.page = "画像分類アニメ"

        st.markdown("<div style='margin-top:.4rem;'></div>", unsafe_allow_html=True)
        st.button("✅  この画像で決定", on_click=_go_with_card_selection, use_container_width=True)

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
    for choice_idx in range(1, 6 + 1):
        for page_num in range(1, 5 + 1):
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
