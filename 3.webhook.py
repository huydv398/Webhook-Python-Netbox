import hmac
import logging
from flask import request
from apiflask import APIFlask, Schema, abort
from apiflask.fields import String, Dict, DateTime, UUID

APP_NAME = "netbox-webhook-listener"
WEBHOOK_SECRET = "secret"

# Initialize the APIFlask app
app = APIFlask(__name__, title="Netbox Webhook Listener", version="1.0")

# Setup logging
logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_logging = logging.FileHandler(f"{APP_NAME}.log")
file_logging.setFormatter(formatter)
logger.addHandler(file_logging)

# Define schemas for request and response
class WebhookResponse(Schema):
    result = String()

class WebhookData(Schema):
    username = String()
    data = Dict()
    event = String()
    timestamp = DateTime()
    model = String()
    request_id = UUID()
    snapshots = Dict()

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

# Define the webhook endpoint
@app.post('/webhook')
@app.input(WebhookData(partial=True))
@app.output(WebhookResponse)
def webhook(data):
    x_hook_signature = request.headers.get('X-Hook-Signature')
    content_length = int(request.headers.get('Content-Length', 0))

    if content_length > 1_000_000:
        # To prevent memory allocation attacks
        logger.error(f"Content too long ({content_length})")
        abort(400, "Content too long")

    if x_hook_signature:
        # Verify signature
        raw_input = request.data
        input_hmac = hmac.new(WEBHOOK_SECRET.encode(), raw_input, digestmod='sha512')
        if not hmac.compare_digest(input_hmac.hexdigest(), x_hook_signature):
            logger.error("Invalid message signature")
            abort(400, "Invalid message signature")
        logger.info("Message signature checked ok")
    else:
        logger.error("No message signature to check")
        abort(400, "No message signature to check")

    # Process the webhook data
    do_something(data)

    return {"result": "ok"}

# Run the application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
