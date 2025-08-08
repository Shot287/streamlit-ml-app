import streamlit as st
import streamlit.components.v1 as components
import os
import time
from PIL import Image

# --- セッション管理の初期化 ---
if "selected_index" not in st.session_state:
    st.session_state.selected_index = 0
if "scrolled_to_analyze" not in st.session_state:
    st.session_state.scrolled_to_analyze = False   # アニメページでの一度きりスクロール制御
if "last_scrolled_page" not in st.session_state:
    st.session_state.last_scrolled_page = ""       # 結果ページでの1回スクロール制御

def go_to(page):
    st.session_state.page = page
    # ページが変わるたびにアニメ用フラグはリセット
    if page != "画像分類アニメ":
        st.session_state.scrolled_to_analyze = False

def image_pages():
    # 2-1: 画像分類イントロ
    if st.session_state.page == "画像分類イントロ":
        st.markdown('<div class="label-chip">👀 画像を見るAI</div>', unsafe_allow_html=True)
        st.header("画像分類（Vision）とは？")
        st.markdown(
            """
<div class="card-text" style="font-size:1.05rem; line-height:1.9;">
画像分類とは、画像の中に「何が写っているか」をAIが判別する技術です。  
たとえば、動物の写真から種類を当てたり、商品の写真からカテゴリを分類したりと、さまざまな分野で活用されています。
</div>
<br>
<div class="card-text" style="font-size:1.05rem; line-height:1.9;">
今回の体験では、<b>6枚の犬の画像</b>から1枚を選び、AIがその犬種を推測します。  
AIがどのように画像の特徴を見つけ出し、犬種を判定するのか、その過程も一緒に見ていきましょう。
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

    # 2-2: 画像分類体験（6枚が1画面に収まるレイアウト）
    elif st.session_state.page == "画像分類体験":
        st.header("画像分類を体験しよう！")
        st.write("下の6枚から1つ選び、「決定」を押してください。")

        image_paths = [
            "selectable_1.webp", "selectable_2.png", "selectable_3.png",
            "selectable_4.png", "selectable_5.png", "selectable_6.png"
        ]
        options = [f"画像{i+1}" for i in range(len(image_paths))]

        # --- CSS: サムネ固定高・白帯除去・余白圧縮 ---
        st.markdown("""
        <style>
        div[data-testid="stImage"] { background: transparent !important; padding: 0 !important; margin: 0 !important; }
        div[data-testid="stImage"] img {
            width: 100% !important;
            height: 170px !important;       /* 必要なら 160〜180 で微調整 */
            object-fit: cover !important;
            border-radius: 12px;
            border: 2px solid transparent;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            transition: transform .15s ease, box-shadow .2s ease, border-color .2s ease;
        }
        div[data-testid="stImage"]:hover img {
            transform: translateY(-1px) scale(1.01);
            box-shadow: 0 8px 18px rgba(0,0,0,0.12);
            border-color: rgba(20,184,166,0.55);
        }
        .thumb-label {
            text-align: center;
            padding: .25rem 0 .2rem 0;
            font-weight: 700;
            font-size: 0.92rem;
            color: #0f172a;
            margin-bottom: .15rem;
        }
        .grid-col { padding-right: 8px !important; padding-left: 8px !important; }
        </style>
        """, unsafe_allow_html=True)

        cols = st.columns(3, gap="small")
        for i, path in enumerate(image_paths):
            with cols[i % 3]:
                st.markdown('<div class="grid-col">', unsafe_allow_html=True)
                if os.path.exists(path):
                    st.image(path, use_container_width=True)
                else:
                    st.error(f"エラー: '{path}' が見つかりません。")
                st.markdown(f"<div class='thumb-label'>{options[i]}</div>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        st.radio("分析したい画像を選んでください：", options, key="radio_selector", horizontal=True)

        def _decide():
            idx = options.index(st.session_state.radio_selector)
            st.session_state.selected_index = idx
            st.session_state.page = "画像分類アニメ"

        st.button("✅  決定", on_click=_decide, use_container_width=True)

        st.divider()
        colb1, colb2 = st.columns(2)
        with colb1:
            st.button("◀  前のページへ戻る", on_click=go_to, args=("画像分類イントロ",), use_container_width=True)
        with colb2:
            st.button("🏠  タイトルに戻る", on_click=go_to, args=("タイトル",), use_container_width=True)

    # 2-3: 画像分類アニメ（到達時に自動スクロール）
    elif st.session_state.page == "画像分類アニメ":
        # スクロール先アンカー
        st.markdown("<div id='analyze-anchor'></div>", unsafe_allow_html=True)

        # 初回だけ強制スクロール（ページ遷移直後に実行）
        if not st.session_state.scrolled_to_analyze:
            components.html(
                """
                <script>
                const go = () => {
                  const doc = window.parent?.document || document;
                  const el = doc.getElementById('analyze-anchor');
                  if (el) el.scrollIntoView({behavior:'smooth', block:'start'});
                };
                setTimeout(go, 120);
                </script>
                """,
                height=0, width=0
            )
            st.session_state.scrolled_to_analyze = True

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

    # 2-5: 画像分類まとめ
    elif st.session_state.page == "画像分類まとめ":
        st.header("画像分類まとめ")
        st.success("体験お疲れ様でした！")
        st.write("今回は、AIが犬の画像を見分ける体験をしました。")
        st.button("最後の解説へ ▶", on_click=go_to, args=("画像分類追加_1",), use_container_width=True)
        st.divider()
        st.button("もう一度体験する", on_click=go_to, args=("画像分類体験",), use_container_width=True)
        st.button("タイトルに戻る", on_click=go_to, args=("タイトル",), use_container_width=True)

    # 2-6: 追加ページ1
    elif st.session_state.page == "画像分類追加_1":
        st.header("解説 1/3")
        path = "extra_1.png"
        if os.path.exists(path):
            st.image(path, use_container_width=True)
        else:
            st.error(f"エラー: 画像ファイル '{path}' が見つかりません。")
        st.button("次へ ▶", on_click=go_to, args=("画像分類追加_2",), use_container_width=True)

    # 2-7: 追加ページ2
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

    # 2-8: 追加ページ3
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

    # 2-4: 各結果ページ（スライドショー）→ ページ切替時に常に最上部へ
    for choice_idx in range(1, 7):
        for page_num in range(1, 6):
            page_name = f"画像分類結果_{choice_idx}_{page_num}"
            if st.session_state.page == page_name:
                # --- ここでトップへ自動スクロール（同じページで何度もは実行しない） ---
                st.markdown("<div id='result-top'></div>", unsafe_allow_html=True)
                if st.session_state.last_scrolled_page != page_name:
                    components.html(
                        """
                        <script>
                        const goTop = () => {
                          const doc = window.parent?.document || document;
                          const el = doc.getElementById('result-top');
                          if (el) el.scrollIntoView({behavior:'instant', block:'start'});
                          // instant が合わなければ 'smooth' に変更可
                        };
                        setTimeout(goTop, 60);
                        </script>
                        """,
                        height=0, width=0
                    )
                    st.session_state.last_scrolled_page = page_name

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
