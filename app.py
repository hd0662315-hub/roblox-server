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

    bot_username = generate_bot_name(original_username)

    # 🚀 رابط دخول مباشر ومبسط تفهمه روبلوكس فوراً لفتح سيرفرك بالظبط
    roblox_uri = f"roblox://placeId={place_id}&gameJobId={job_id}"

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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
