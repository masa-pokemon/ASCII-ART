import streamlit as st

# ヘッダー表示
st.title("PNG + HTML ポリグロットファイル生成ツール")

# PNGファイルアップロード
uploaded_file = st.file_uploader("PNG画像をアップロードしてください", type=["png"])

# HTMLコード入力
html_code = st.text_area("追加するHTMLコード", height=300, value="<h1>Hello from PNG!</h1>")

# 実行ボタン
if st.button("ポリグロットファイル生成") and uploaded_file:
    # PNGの内容を読み込み
    png_data = uploaded_file.read()

    # IENDチャンクを探して挿入ポイントを見つける
    iend_marker = b'\x00\x00\x00\x00IEND\xaeB`\x82'
    iend_index = png_data.find(iend_marker)

    if iend_index == -1:
        st.error("IENDチャンクが見つかりません。これは有効なPNGファイルではない可能性があります。")
    else:
        # HTMLコンテンツをバイト化
        html_bytes = html_code.encode("utf-8")

        # PNG + HTMLの結合（IENDチャンクの後にHTML追加）
        polyglot_data = png_data + b'\n<!--\n' + html_bytes + b'\n-->\n'

        # ダウンロード
        st.download_button(
            label="ポリグロットファイルをダウンロード",
            data=polyglot_data,
            file_name="polyglot.png",
            mime="image/png"
        )
