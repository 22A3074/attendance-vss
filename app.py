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

    # numpy 配列化
    arrA = np.array(imgA)
    arrB = np.array(imgB)

    # === 論理積（AND）で合成 ===
    combined = np.minimum(arrA, arrB)

    # 表示
    st.image(combined, caption="合成結果", use_column_width=True)

    # 一時ファイルに保存して QRコード解析
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        Image.fromarray(combined).save(tmp.name)
        tmp_path = tmp.name

    # OpenCVでQRコード読み取り
    detector = cv2.QRCodeDetector()
    data, pts, _ = detector.detectAndDecode(cv2.imread(tmp_path))

    if data:
        st.success(f"QRコード読み取り成功: {data}")
        st.markdown(f"[こちらをクリックしてアクセス]({data})")
    else:
        st.error("QRコードが読み取れませんでした。")
