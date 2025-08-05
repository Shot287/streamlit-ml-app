import os
from pathlib import Path

import numpy as np
import streamlit as st
from PIL import Image


BASE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = BASE_DIR / "images"


@st.cache_resource
def load_prototypes() -> tuple[np.ndarray, np.ndarray]:
    """Load prototype images for a tiny nearest-neighbor classifier."""
    cat = Image.open(IMAGE_DIR / "cat.jpg").resize((224, 224))
    dog = Image.open(IMAGE_DIR / "dog.jpg").resize((224, 224))
    return np.array(cat, dtype=np.float32), np.array(dog, dtype=np.float32)


def classify_image(img: Image.Image) -> tuple[str, str]:
    """Return label (猫/犬/その他) and explanation."""
    cat_proto, dog_proto = load_prototypes()

    arr = np.array(img.resize((224, 224)), dtype=np.float32)

    cat_dist = float(np.mean((arr - cat_proto) ** 2))
    dog_dist = float(np.mean((arr - dog_proto) ** 2))

    threshold = 4000.0

    if min(cat_dist, dog_dist) > threshold:
        label = "その他"
        explanation = "猫・犬のどちらにも似ていませんでした。"
    elif cat_dist < dog_dist:
        label = "猫"
        explanation = "猫画像との距離が犬画像より小さかったため猫と判断しました。"
    else:
        label = "犬"
        explanation = "犬画像との距離が猫画像より小さかったため犬と判断しました。"

    return label, explanation


# Grad-CAM functionality was removed to keep the app lightweight and
# avoid heavy TensorFlow dependencies.


if __name__ == "__main__":
    # UI
    st.title("画像分類デモ")
    st.write("画像を選択すると、猫か犬かを判定します。")

    image_files = [
        p.name
        for p in IMAGE_DIR.iterdir()
        if p.suffix.lower() in {".jpg", ".png", ".jpeg"}
    ]

    selected = st.selectbox("画像を選択してください", image_files)

    if selected:
        img = Image.open(IMAGE_DIR / selected)
        st.image(img, caption=selected, use_column_width=True)

        label, explanation = classify_image(img)
        st.subheader(f"判定: {label}")
        st.write(explanation)