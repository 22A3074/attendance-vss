import streamlit as st
import numpy as np
from PIL import Image
import hashlib

st.set_page_config(page_title="出席確認アプリ", layout="centered")
st.title("🎓 視覚復号型秘密分散法による出席確認")

# --- シェアAを読み込み ---
try:
    shareA = np.array(Image.open("shareA.png").convert("1"), dtype=np.uint8)
except FileNotFoundError:
    st.error("shareA.png が見つかりません。教員側で生成してください。")
    st.stop()

# --- 学籍番号入力 ---
student_id = st.text_input("あなたの学籍番号を入力してください（例：22A3074）")

# --- シェアBアップロード ---
uploaded = st.file_uploader("あなたのシェアB画像をアップロードしてください（PNG）", type=["png"])

# --- 復号処理 ---
if student_id and uploaded:
    imgB = np.array(Image.open(uploaded).convert("1"), dtype=np.uint8)
    decoded = np.bitwise_xor(shareA, imgB)

    st.image(decoded * 255, caption="復号結果", use_column_width=True)

    # 正しいシェアかどうかを確認
    # 正しいパターンを同様の方法で生成
    seed = int(hashlib.sha256(student_id.encode()).hexdigest(), 16)
    np.random.seed(seed)
    true_pattern = np.random.randint(0, 2, shareA.shape, dtype=np.uint8)
    expected = np.bitwise_xor(shareA, true_pattern)

    if np.array_equal(decoded, expected):
        st.success(f"✅ {student_id} さんの出席を確認しました！")
    else:
        st.error("❌ このシェアは無効です。他の学生のシェアを使用していませんか？")
