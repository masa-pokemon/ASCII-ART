import streamlit as st

# PNGのIENDチャンク
IEND_CHUNK = b'\x00\x00\x00\x00IEND\xaeB`\x82'

# タイトル
st.title("PNG + HTML ポリグロットファイル生成")

uploaded_file = st.file_uploader("PNG画像をアップロードしてください", type=["png"])
html_code = st.text_area("末尾に埋め込むHTMLコード", height=300, value="<h1>Hello from PNG!</h1>")

if st.button("ポリグロットファイル生成") and uploaded_file:
    png_data = uploaded_file.read()
    html_payload = html_code.encode("utf-8")

    # IENDがなければ追加
    if IEND_CHUNK not in png_data:
        st.warning("IENDチャンクが見つかりませんでした。追加します。")
        png_data += IEND_CHUNK

    # ポリグロットファイル作成（HTMLを「<!--」の中に入れて、画像として壊れないように）
    polyglot_data = png_data + b"\n<!--\n" + html_payload + b"\n-->\n"

    # ダウンロードボタン
    st.download_button(
        label="ポリグロットPNGファイルをダウンロード",
        data=polyglot_data,
        file_name="polyglot.png",
        mime="image/png"
    )

    st.markdown("💡 `.png`として画像ビューアで表示でき、`.html`にリネームすればWebページとしても動作します。")
