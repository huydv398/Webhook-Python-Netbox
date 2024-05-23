import hmac
from apiflask import APIFlask
import logging
from flask import request
from apiflask import Schema, abort
from apiflask.fields import String, Dict, DateTime, UUID

APP_NAME = "netbox-webhook-listener"
WEBHOOK_SECRET = "secret"

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

app = APIFlask(__name__, title="Netbox Webhook Listener", version="1.0")

logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_logging = logging.FileHandler(f"{APP_NAME}.log")
file_logging.setFormatter(formatter)
logger.addHandler(file_logging)

def do_something(data):
    logger.info("WebhookData received:")
    logger.info(f"Raw data: {data}")
    logger.info(f"Request ID: {data['request_id']}")
    logger.info(f"Username: {data['username']}")
    logger.info(f"Event: {data['event']}")
    logger.info(f"Timestamp: {data['timestamp']}")
    logger.info(f"Model: {data['model']}")
    logger.info(f"Data: {data['data']}")
    logger.info(f"URL in data: {data['data']['url']}")

@app.post('/webhook')
@app.input(WebhookData(partial=True))
@app.output(WebhookResponse)
def webhook(data,*args, **kwargs):
    x_hook_signature = request.headers.get('X-Hook-Signature', None)
    content_length = int(request.headers.get('Content-Length', 0))

    if content_length > 1_000_000:
        # To prevent memory allocation attacks
        logger.error(f"Content too long ({content_length})")
        abort(400, "Content too long")

    if x_hook_signature:
        # Check signature
        raw_input = request.data
        input_hmac = hmac.new(key=WEBHOOK_SECRET.encode(), msg=raw_input, digestmod="sha512")
        if not hmac.compare_digest(input_hmac.hexdigest(), x_hook_signature):
            logger.error("Invalid message signature")
            abort(400, "Invalid message signature")

        logger.info("Message signature checked ok")
    else:
        logger.error("No message signature to check")
        abort(400, "No message signature to check")

    # Do something here
    do_something(data)

    return {"result": "ok"}

if __name__ == "__main__":
    app.run("0.0.0.0",debug=True)

