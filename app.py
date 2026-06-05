import os
import random
import string
import subprocess
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


# دالة لتوليد اسم عشوائي بناءً على اسم اللاعب الأصلي بزيادة حروف وأرقام
def generate_bot_name(original_name):
    random_letters = "".join(
        random.choices(string.ascii_letters + string.digits, k=4)
    )
    return f"{original_name}_{random_letters}"


@app.route("/launch-bot", methods=["POST"])
def launch_bot():
    data = request.json
    if not data:
        return (
            jsonify({"status": "error", "message": "لم يتم استقبال بيانات"}),
            400,
        )

    place_id = data.get("PlaceId")
    job_id = data.get("JobId")
    original_username = data.get("Username")

    # 1. توليد الاسم الجديد للبوت
    bot_username = generate_bot_name(original_username)
    print(
        f"\n[+] تم استقبال طلب جديد من اللعبة لإنشاء بوت باسم: {bot_username}"
    )
    print("✅ يتم المتابعة وتجهيز إشارات الدخول فوراً...")

    # 2. هندسة الدخول إلى السيرفر (Protocol Launch URL)
    roblox_uri = f"roblox-player:1+launchmode:play+gameinfo:TOKEN_HERE+placelauncherurl:https%3A%2F%2Fassetgame.roblox.com%2Fgame%2FPlaceLauncher.ashx%3Frequest%3DConnect%26browserTrackerId%3D0%26placeId%3D{place_id}%26isReadOnly%3Dfalse%26gameJobId%3D{job_id}"

    print("==================================================")
    print(f"[+] أمر تشغيل اللعبة الجاهز للمحرك:\n{roblox_uri}")
    print("==================================================")

    # 3. فتح محرك روبلوكس تلقائياً على الكمبيوتر لتشغيل البوت
    try:
        print("[*] جاري إطلاق تطبيق روبلوكس في الخلفية...")
        os.system(f"start {roblox_uri}")
    except Exception as e:
        print(f"[-] فشل فتح اللعبة تلقائياً: {e}")

    return (
        jsonify(
            {
                "status": "success",
                "bot_name": bot_username,
                "message": "Bot launched successfully.",
            }
        ),
        200,
    )


if __name__ == "__main__":
    print("==================================================")
    print("🚀 سيرفر بايثون يعمل الآن ومستعد لاستقبال البيانات!")
    print("==================================================")
    app.run(host="0.0.0.0", port=5000, debug=True)