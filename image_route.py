import streamlit as st
import streamlit.components.v1 as components
import os
import time
from PIL import Image

# --- 初期化 ---
if "selected_index" not in st.session_state:
    st.session_state.selected_index = 0
if "scrolled_to_analyze" not in st.session_state:
    st.session_state.scrolled_to_analyze = False

def go_to(page):
    st.session_state.page = page
    if page != "画像分類アニメ":
        st.session_state.scrolled_to_analyze = False

def image_pages():
    # 2-1: イントロ
    if st.session_state.page == "画像分類イントロ":
        st.header("画像分類（Vision）とは？")
        st.write(
            "画像分類とは、画像の中に「何が写っているか」をAIが判別する技術です。\n"
            "今回の体験では、6枚の犬の画像から1枚を選び、AIがその犬種を推測します。"
        )
        st.button("▶ 体験スタート", on_click=go_to, args=("画像分類体験",), use_container_width=True)
        st.button("← タイトルに戻る", on_click=go_to, args=("タイトル",), use_container_width=True)

    # 2-2: 画像選択
    elif st.session_state.page == "画像分類体験":
        st.header("画像分類を体験しよう！")
        image_paths = [
            "selectable_1.webp", "selectable_2.png", "selectable_3.png",
            "selectable_4.png", "selectable_5.png", "selectable_6.png"
        ]
        options = [f"画像{i+1}" for i in range(len(image_paths))]

        cols = st.columns(3)
        for i, path in enumerate(image_paths):
            with cols[i % 3]:
                if os.path.exists(path):
                    st.image(path, use_container_width=True)
                st.write(options[i])

        st.radio("分析したい画像を選んでください：", options, key="radio_selector", horizontal=True)

        def _decide():
            idx = options.index(st.session_state.radio_selector)
            st.session_state.selected_index = idx
            st.session_state.page = "画像分類アニメ"

        st.button("✅ 決定", on_click=_decide, use_container_width=True)

    # 2-3: アニメーション
    elif st.session_state.page == "画像分類アニメ":
        st.markdown("<div id='analyze-anchor'></div>", unsafe_allow_html=True)
        if not st.session_state.scrolled_to_analyze:
            components.html(
                """
                <script>
                const el = window.parent?.document?.getElementById('analyze-anchor') || document.getElementById('analyze-anchor');
                if (el) { el.scrollIntoView({behavior:'smooth', block:'start'}); }
                </script>
                """,
                height=0, width=0
            )
            st.session_state.scrolled_to_analyze = True

        st.header("AIが画像を分析中...")
        pb = st.progress(0)
        for i in range(100):
            time.sleep(0.02)
            pb.progress(i + 1)
        st.success("分析が完了しました！")

        idx = st.session_state.selected_index
        st.button("結果を見る", on_click=go_to, args=(f"画像分類結果_{idx + 1}_1",), use_container_width=True)

    # 2-4: 結果ページ
    for choice_idx in range(1, 7):
        for page_num in range(1, 6):
            page_name = f"画像分類結果_{choice_idx}_{page_num}"
            if st.session_state.page == page_name:
                # ページ読み込み時にトップへスクロール
                st.markdown("<div id='page-top'></div>", unsafe_allow_html=True)
                components.html(
                    """
                    <script>
                    const el = window.parent?.document?.getElementById('page-top') || document.getElementById('page-top');
                    if (el) { el.scrollIntoView({behavior:'auto', block:'start'}); }
                    </script>
                    """,
                    height=0, width=0
                )

                # 上部にボタン
                col1, col2 = st.columns(2)
                with col1:
                    if page_num > 1:
                        st.button("◀ 戻る", on_click=go_to,
                                  args=(f"画像分類結果_{choice_idx}_{page_num - 1}",),
                                  use_container_width=True)
                    else:
                        st.button("◀ 選択画面に戻る", on_click=go_to,
                                  args=("画像分類体験",), use_container_width=True)
                with col2:
                    if page_num < 5:
                        st.button("次へ ▶", on_click=go_to,
                                  args=(f"画像分類結果_{choice_idx}_{page_num + 1}",),
                                  use_container_width=True)
                    else:
                        st.button("まとめへ ▶", on_click=go_to,
                                  args=("画像分類まとめ",), use_container_width=True)

                # 分析結果画像
                result_path = f"result_{choice_idx}_{page_num}.png"
                if os.path.exists(result_path):
                    st.image(result_path, caption=f"画像{choice_idx} の分析結果 {page_num}", use_container_width=True)
                else:
                    st.error(f"結果画像 {result_path} が見つかりません。")

    # 2-5: まとめ
    if st.session_state.page == "画像分類まとめ":
        st.header("画像分類まとめ")
        st.success("体験お疲れ様でした！")
        st.button("もう一度体験する", on_click=go_to, args=("画像分類体験",), use_container_width=True)
        st.button("タイトルに戻る", on_click=go_to, args=("タイトル",), use_container_width=True)
