import os

import numpy as np
import streamlit as st
from PIL import Image
from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    decode_predictions,
    preprocess_input,
)


@st.cache_resource
def load_model():
    """Load a pre-trained MobileNetV2 model."""
    return MobileNetV2(weights="imagenet")


def classify_image(img: Image.Image) -> tuple[str, str]:
    """Return label (猫/犬/その他) and explanation."""
    model = load_model()

    resized = img.resize((224, 224))
    arr = np.array(resized)
    arr = np.expand_dims(arr, 0)
    arr = preprocess_input(arr)

    preds = model.predict(arr)
    decoded = decode_predictions(preds, top=3)[0]

    label = "その他"
    explanation = ""
    for _, cls, prob in decoded:
        if "cat" in cls:
            label = "猫"
            explanation = f"上位予測が『{cls}』({prob:.0%})のため猫と判断しました。"
            break
        if "dog" in cls:
            label = "犬"
            explanation = f"上位予測が『{cls}』({prob:.0%})のため犬と判断しました。"
            break

    if label == "その他":
        cls, prob = decoded[0][1], decoded[0][2]
        explanation = f"上位予測が『{cls}』({prob:.0%})でした。"

    return label, explanation


def make_gradcam_heatmap(img: Image.Image, model, last_conv_layer_name="Conv_1"):
    """Generate a Grad-CAM heatmap for the image."""
    import matplotlib.cm as cm
    import tensorflow as tf

    arr = np.array(img.resize((224, 224)))
    arr = np.expand_dims(arr, 0)
    arr = preprocess_input(arr)

    grad_model = tf.keras.models.Model(
        [model.inputs], [model.get_layer(last_conv_layer_name).output, model.output]
    )
    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(arr)
        pred_index = tf.argmax(predictions[0])
        loss = predictions[:, pred_index]

    grads = tape.gradient(loss, conv_outputs)[0]
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_outputs = conv_outputs[0]
    heatmap = tf.reduce_sum(tf.multiply(pooled_grads, conv_outputs), axis=-1)
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    heatmap = heatmap.numpy()

    # Resize and apply colormap
    heatmap = Image.fromarray(np.uint8(255 * heatmap)).resize(img.size)
    heatmap = np.array(heatmap) / 255.0
    colormap = cm.get_cmap("jet")
    heatmap = colormap(heatmap)[:, :, :3]
    heatmap = Image.fromarray((heatmap * 255).astype("uint8"))

    return Image.blend(img.convert("RGB"), heatmap, alpha=0.4)


# UI
st.title("画像分類デモ")
st.write("画像を選択すると、猫か犬かを判定します。")

image_dir = "images"
image_files = [f for f in os.listdir(image_dir) if f.lower().endswith((".jpg", ".png", ".jpeg"))]

selected = st.selectbox("画像を選択してください", image_files)

if selected:
    path = os.path.join(image_dir, selected)
    img = Image.open(path)
    st.image(img, caption=selected, use_column_width=True)

    label, explanation = classify_image(img)
    st.subheader(f"判定: {label}")
    st.write(explanation)

    if st.checkbox("Grad-CAMヒートマップを表示する"):
        heatmap = make_gradcam_heatmap(img, load_model())
        st.image(heatmap, caption="Grad-CAM", use_column_width=True)