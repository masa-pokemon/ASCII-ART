import streamlit as st

def make_polyglot(png_data: bytes, html_code: str) -> bytes:
    # PNGファイルの終端にHTMLをコメントとして追加
    polyglot_data = bytearray(png_data)

    # HTMLはPNGとして無害になるようにHTMLコメントとして追加
    html_payload = b"\n<!--\n" + html_code.encode("utf-8") + b"\n-->\n"

    polyglot_data.extend(html_payload)
    return bytes(polyglot_data)


st.title("Polyglot PNG + HTML ファイル作成ツール")

uploaded_file = st.file_uploader("PNG画像をアップロードしてください", type=["png"])
html_code = st.text_area("埋め込みたいHTMLコードを入力してください", height=200, value="<h1>Hello Polyglot</h1>")

if uploaded_file and html_code:
    png_data = uploaded_file.read()
    polyglot = make_polyglot(png_data, html_code)

    st.download_button(
        label="Polyglot PNG+HTML ファイルをダウンロード",
        data=polyglot,
        file_name="polyglot.png",
        mime="image/png"
    )

    st.image(png_data, caption="元のPNG画像")
