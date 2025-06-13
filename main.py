import streamlit as st

# PNGのIENDチャンク定義
IEND_CHUNK = b'\x00\x00\x00\x00IEND\xaeB`\x82'

# タイトル表示
st.title("PNG + HTML ポリグロットファイル生成ツール")

# PNGファイルのアップロード
uploaded_file = st.file_uploader("PNG画像をアップロードしてください", type=["png"])

# HTMLコード入力欄
html_code = st.text_area("埋め込むHTMLコード", height=300, value="<h1>Hello from PNG!</h1>")

# 実行ボタン
if st.button("ポリグロットファイル生成") and uploaded_file:
    png_data = uploaded_file.read()
    html_bytes = html_code.encode("utf-8")

    # IENDチャンクの存在を確認
    if IEND_CHUNK in png_data:
        polyglot_data = png_data + b'\n<!--\n' + html_bytes + b'\n-->\n'
    else:
        st.warning("IENDチャンクが見つかりませんでした。自動的に追加します。")
        polyglot_data = png_data + IEND_CHUNK + b'\n<!--\n' + html_bytes + b'\n-->\n'

    # ダウンロードボタン
    st.download_button(
        label="ポリグロットファイルをダウンロード",
        data=polyglot_data,
        file_name="polyglot.png",
        mime="image/png"
    )
