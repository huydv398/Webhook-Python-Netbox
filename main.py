import hmac
from apiflask import APIFlask, Schema
import logging
from flask import request, jsonify
from apiflask import Schema, abort
from apiflask.fields import String, Dict, DateTime, UUID
import requests

APP_NAME = "netbox-webhook-listener"
WEBHOOK_SECRET = "secret"

# Token API của bot
bot_token = '55x98315:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
# ID chat của người nhận (có thể là ID của nhóm hoặc người dùng)
chat_id = '-636xxx447'

app = APIFlask(__name__, title="Netbox Webhook Listener", version="1.0")

# Định nghĩa schema sử dụng marshmallow

class WebhookData(Schema):
    username = String(required=True)
    data = Dict(required=True)
    event = String(required=True)
    timestamp = DateTime(required=True)
    model = String(required=True)
    request_id = UUID(required=True)
    snapshots = Dict(required=True)

class WebhookResponse(Schema):
    result = String(required=True)
    



# # Định nghĩa route để lắng nghe webhook
# Setup logging
logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_logging = logging.FileHandler(f"{APP_NAME}.log")
file_logging.setFormatter(formatter)
logger.addHandler(file_logging)


# Function to handle the webhook data
def do_something(data):
    try:
        logger.info("WebhookData received:")
        logger.info(f"Raw data: {data}")
        logger.info(f"Request ID: {data['request_id']}")
        logger.info(f"Username: {data['username']}")
        logger.info(f"Event: {data['event']}")
        logger.info(f"Timestamp: {data['timestamp']}")
        logger.info(f"Model: {data['model']}")
        logger.info(f"Data: {data['data']}")
        if 'url' in data['data']:
            logger.info(f"URL in data: {data['data']['url']}")
    except KeyError as e:
        logger.error(f"Missing key in data: {e}")

@app.route('/webhook', methods=['POST'])
# @app.input(WebhookData)
# @app.output(WebhookResponse)
def webhook_receiver():
    data = request.json  # Get the JSON data from the incoming request

    # Process the data and perform actions based on the event

    x_hook_signature = request.headers.get('X-Hook-Signature')
    if x_hook_signature:
        # Verify signature
        raw_input = request.data
        input_hmac = hmac.new(WEBHOOK_SECRET.encode(), raw_input, digestmod='sha512')
        if not hmac.compare_digest(input_hmac.hexdigest(), x_hook_signature):
            logger.error("Invalid message signature")
            abort(400, "Invalid message signature")
        logger.info("Message signature checked ok")

    content_length = int(request.headers.get('Content-Length', 0))
    if content_length > 1_000_000:
        # To prevent memory allocation attacks
        logger.error(f"Content too long ({content_length})")
        abort(400, "Content too long")

    # Process the webhook data
    do_something(data)




    # Nội dung tin nhắn
    message1 = f"""
    ```Event: {data['event']}
    Username: {data['username']}
    URL in data: {data['data']['url']}
    Model: {data['model']}
    Timestamp: {data['timestamp']}```
    """

    # URL API để gửi tin nhắn
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

    # Payload chứa thông tin tin nhắn
    payload = {
        'chat_id': chat_id,
        'text': message1,
        'parse_mode' : "MarkdownV2"
    }

    # Gửi request POST để gửi tin nhắn
    response = requests.post(url, data=payload)

    # Kiểm tra kết quả
    if response.status_code == 200:
        print('Message sent successfully')
    else:
        print('Failed to send message')

        
    # print("Received webhook data:", data['data']['url'])
    print("Received webhook data:", message1)
    # return jsonify({'message': 'Webhook received successfully'}), 200
    return jsonify("Received webhook data:"), 200

if __name__ == "__main__":
    app.run("0.0.0.0",debug=True)
