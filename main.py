import struct
import zlib
import streamlit as st

def make_polyglot_png(original_png: bytes, html_payload: str) -> bytes:
    # PNGシグネチャ確認
    png_signature = b'\x89PNG\r\n\x1a\n'
    if not original_png.startswith(png_signature):
        raise ValueError("これは正しいPNGファイルではありません。")

    # IENDチャンクの位置を探す
    iend_marker = b'IEND'
    iend_pos = original_png.rfind(iend_marker)

    if iend_pos == -1:
        # IENDが見つからない → 追加する
        st.warning("⚠️ PNGにIENDチャンクが見つかりませんでした。自動的に追加します。")
        # 正しいIENDチャンクを生成（空のデータ + CRC）
        iend_chunk = b'\x00\x00\x00\x00' + b'IEND' + zlib.crc32(b'IEND').to_bytes(4, byteorder='big')
        png_head = original_png
        png_tail = iend_chunk
    else:
        # 正常な場合 → IDATまでを抽出、IEND前にHTMLを挿入
        iend_index = iend_pos - 4  # "IEND"の前の4バイトはデータ長
        png_head = original_png[:iend_index]
        png_tail = original_png[iend_index:]

    # HTMLペイロードをUTF-8としてエンコード
    html_bytes = html_payload.encode('utf-8')

    # 結合してPolyglotを作成
    polyglot_data = png_head + html_bytes + png_tail
    return polyglot_data


st.title("🌀 PNG + HTML Polyglot Creator")
st.write("このツールは、画像としてもHTMLページとしても動作するファイルを作成します。")

uploaded_file = st.file_uploader("PNG画像をアップロードしてください", type=["png"])
html_input = st.text_area("埋め込むHTMLコードを入力", "<h1>Hello from PNG-HTML Polyglot!</h1>", height=200)

if uploaded_file and html_input:
    original_png_data = uploaded_file.read()
    try:
        polyglot_data = make_polyglot_png(original_png_data, html_input)

        st.success("✅ ポリグロットファイルが作成されました！")

        st.download_button(
            label="⬇️ ポリグロットPNGファイルをダウンロード",
            data=polyglot_data,
            file_name="polyglot.png",
            mime="image/png"
        )

        st.image(polyglot_data, caption="画像として表示されたポリグロットPNG")

        with st.expander("🔍 HTMLとして確認する方法"):
            st.markdown("""
            1. ダウンロードした `polyglot.png` のファイル名を `.html` に変更するか、ブラウザで開いてください。
            2. HTMLとして埋め込んだコードが実行されます。
            """)

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
else:
    st.info("PNG画像とHTMLコードを入力してください。")
