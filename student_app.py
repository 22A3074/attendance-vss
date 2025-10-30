import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import numpy as np

st.title("学生用アプリ：出席確認（VSS復号）")

# GitHub上のshareA.pngを取得
url = "https://raw.githubusercontent.com/22A3074/attendance-vss/main/shareA.png"
response = requests.get(url)
if response.status_code == 200:
    shareA = Image.open(BytesIO(response.content))
else:
    st.error("教員側の shareA.png が見つかりません。")
    st.stop()

# 学生がshareB.pngをアップロード
uploaded_file = st.file_uploader("あなたのシェア画像（shareB.png）をアップロードしてください", type=["png"])

if uploaded_file is not None:
    shareB = Image.open(uploaded_file)

    # 同サイズに調整
    shareA = shareA.convert("1")
    shareB = shareB.convert("1")

    # 論理積で復号
    arrA = np.array(shareA)
    arrB = np.array(shareB)
    decoded = np.logical_and(arrA, arrB)

    st.image(decoded.astype(np.uint8) * 255, caption="復号結果", use_column_width=True)
    st.success("✅ 出席確認成功！")
