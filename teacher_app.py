import streamlit as st
from PIL import Image
import qrcode
import os

st.title("教員用アプリ：出席シェア画像生成")

# 出席コードを入力
code = st.text_input("出席コードを入力してください（例: lecture1）")

if st.button("シェア画像を生成"):
    if code:
        # QRコードを生成
        qr = qrcode.make(code)
        qr.save("original.png")

        # ダミーの視覚分散処理（本番ではVSSに置き換える）
        shareA = qr.copy()
        shareB = qr.transpose(Image.FLIP_LEFT_RIGHT)

        shareA.save("shareA.png")
        shareB.save("shareB.png")

        st.image(shareA, caption="shareA.png（教員用）")
        st.image(shareB, caption="shareB.png（学生配布用）")

        st.success("✅ 生成完了！ GitHubにアップロードしてください。")

        st.markdown("""
        **次の手順**  
        1. この2つのファイル（shareA.png, shareB.png）をダウンロード  
        2. GitHubのリポジトリ直下にアップロード  
        3. 学生に shareB.png を配布
        """)
    else:
        st.error("出席コードを入力してください。")
