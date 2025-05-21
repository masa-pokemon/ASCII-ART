import streamlit as st
from PIL import Image
import numpy as np

# ASCII文字セット（濃い順に）
ASCII_CHARS = "@%#*+=-:. "

def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * 0.55)  # 高さ補正
    resized_image = image.resize((new_width, new_height))
    return resized_image

def grayify(image):
    return image.convert("L")

def pixels_to_ascii(image):
    pixels = np.array(image)
    ascii_str = ""
    for row in pixels:
        for pixel in row:
            ascii_str += ASCII_CHARS[pixel * len(ASCII_CHARS) // 256]
        ascii_str += "\n"
    return ascii_str

def main():
    st.title("🖼️ 画像 → アスキーアート変換アプリ")
    st.write("画像をアップロードして、アスキーアートに変換しましょう！")

    uploaded_file = st.file_uploader("画像を選択", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="アップロードした画像", use_column_width=True)

        new_width = st.slider("アスキーアートの幅", 50, 200, 100)
        image = resize_image(image, new_width=new_width)
        gray_image = grayify(image)
        ascii_str = pixels_to_ascii(gray_image)

        st.text_area("🎨 アスキーアート出力", ascii_str, height=500)

        st.download_button("💾 アスキーアートをテキストでダウンロード",
                           ascii_str,
                           file_name="ascii_art.txt")

if __name__ == "__main__":
    main()
