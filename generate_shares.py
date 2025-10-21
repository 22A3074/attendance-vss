import numpy as np
from PIL import Image
import hashlib, os, random

# ==============================
# 設定
# ==============================
IMG_SIZE = (128, 128)  # シェア画像サイズ
STUDENT_IDS = ["22A3074", "22A3002"]  # 学生IDリスト
os.makedirs("student_shares", exist_ok=True)

# ==============================
# 授業共通のシェアAを生成
# ==============================
shareA = np.random.randint(0, 2, IMG_SIZE, dtype=np.uint8)
Image.fromarray(shareA * 255).save("shareA.png")
print("✅ shareA.png を作成しました。")

# ==============================
# 学生ごとのシェアBを生成
# ==============================
def generate_shareB(student_id, base_pattern):
    # 学籍番号から乱数シードを作成（同じIDなら同じ結果に）
    seed = int(hashlib.sha256(student_id.encode()).hexdigest(), 16)
    random.seed(seed)
    student_pattern = np.random.randint(0, 2, IMG_SIZE, dtype=np.uint8)
    shareB = np.bitwise_xor(base_pattern, student_pattern)
    return shareB

for sid in STUDENT_IDS:
    shareB = generate_shareB(sid, shareA)
    Image.fromarray(shareB * 255).save(f"student_shares/shareB_{sid}.png")

print("学生ごとのシェアBを student_shares/ に作成しました。")
