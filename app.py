import os
from flask import Flask, request
from dotenv import load_dotenv
from whatsapp import send_message
from location_handler import handle_location
from ai_handler import ai_reply


load_dotenv()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
if not VERIFY_TOKEN:
    raise ValueError("VERIFY_TOKEN not set in environment variables.")

app = Flask(__name__)

# ✅ Webhook verification
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Invalid verify token", 403

    elif request.method == "POST":
        data = request.get_json()
        print("📩 Incoming:", data)

        if not data or not data.get("entry"):
            return "No entry found", 400

        for entry in data["entry"]:
            for change in entry.get("changes", []):
                value = change.get("value", {})
                messages = value.get("messages", [])

                for msg in messages:
                    from_number = msg.get("from")
                    msg_type = msg.get("type")

                    if not from_number or not msg_type:
                        continue

                    if msg_type == "location":
                        lat = msg["location"].get("latitude")
                        lon = msg["location"].get("longitude")
                        if lat is not None and lon is not None:
                            handle_location(from_number, lat, lon)
                    elif msg_type == "text":
                        user_text = msg["text"].get("body")
                        if user_text:
                            reply = ai_reply(user_text)
                            send_message(from_number, reply)

        return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Read PORT env variable or default to 5000
    app.run(host="0.0.0.0", port=port, debug=False)  # Disable debug mode in production