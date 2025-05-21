import streamlit as st
from PIL import Image
import numpy as np


# 画像をリサイズして文字数を調整
def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)  # 高さ調整（フォントの縦横比に合わせる）
    return image.resize((new_width, new_height))

ASCII_CHARS = ['@', '%', '#', '*', '+', '=', '-', ':', '.', ' ']

def image_to_ascii(image):
    image = image.convert("L")  # グレースケール化
    pixels = np.array(image)
    ascii_str = ""
    for row in pixels:
        for pixel in row:
            index = pixel * (len(ASCII_CHARS) - 1) // 255  # 0〜255 を 0〜9 にマッピング
            ascii_str += ASCII_CHARS[index]
        ascii_str += "\n"
    return ascii_str

# Streamlit UI
st.title("画像をアスキーアートに変換するアプリ")

uploaded_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="アップロードされた画像", use_column_width=True)

    width = st.slider("アスキーアートの幅（文字数）", min_value=20, max_value=200, value=100)
    resized_image = resize_image(image, new_width=width)
    ascii_art = image_to_ascii(resized_image)

    st.text_area("🎨 アスキーアート出力", ascii_art, height=500)
