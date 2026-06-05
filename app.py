import os
import random
import string
from flask import Flask, jsonify, request

app = Flask(__name__)


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

    # توليد اسم البوت الجديد
    bot_username = generate_bot_name(original_username)

    # 🚀 الرابط الرسمي المباشر لتشغيل الحساب البديل في سيرفرك
    roblox_uri = f"roblox://placeId={place_id}&gameJobId={job_id}"

    # نرسل البيانات للأكسكيوتور عشان هو اللي يفتح اللعبة عندك
    return (
        jsonify(
            {
                "status": "success",
                "bot_name": bot_username,
                "roblox_uri": roblox_uri,
            }
        ),
        200,
    )


if __name__ == "__main__":
    # تحديد البورت المتوافق مع Render سحابياً
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
