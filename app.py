import streamlit as st
import streamlit as st
from PIL import Image
import numpy as np
import cv2
import tempfile
import webbrowser

st.title("出席確認（視覚復号型秘密分散）")

# === 画像アップロード ===
shareA = st.file_uploader("先生のシェア画像 (Share A)", type=["png", "jpg"])
shareB = st.file_uploader("学生のシェア画像 (Share B)", type=["png", "jpg"])

if shareA and shareB:
    # 画像読み込み
    imgA = Image.open(shareA).convert("L")
    imgB = Image.open(shareB).convert("L")

    # サイズ調整（片方のサイズに合わせる）
    imgB = imgB.resize(imgA.size)

    # numpy配列化
    arrA = np.array(imgA)
    arrB = np.array(imgB)

    # === 合成（ANDっぽく重ねる） ===
    combined = np.minimum(arrA, arrB).astype(np.uint8)

    st.image(combined, caption="合成結果", use_column_width=True)

    # === QRコード読み取り ===
    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(combined)

    if data:
        st.success(f"QRコードを検出しました: {data}")
        st.markdown(f"[👉 Googleフォームへ移動する]({data})")
    else:
        st.error("QRコードの読み取りに失敗しました。")
