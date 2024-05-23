import hmac
from apiflask import APIFlask, Schema
import logging
from flask import request, jsonify
from apiflask import Schema, abort
from apiflask.fields import String, Dict, DateTime, UUID

APP_NAME = "netbox-webhook-listener"
WEBHOOK_SECRET = "secret"

app = APIFlask(__name__, title="Netbox Webhook Listener", version="1.0")

# Định nghĩa schema sử dụng marshmallow
class WebhookResponse(Schema):
    result = String(required=True)

class WebhookData(Schema):
    username = String(required=True)
    data = Dict(required=True)
    event = String(required=True)
    timestamp = DateTime(required=True)
    model = String(required=True)
    request_id = UUID(required=True)
    snapshots = Dict(required=True)


@app.route('/webhook', methods=['POST'])
@app.input(WebhookData)
@app.output(WebhookResponse)
def webhook_receiver():
    return jsonify({'message': 'Webhook received successfully'}), 200

if __name__ == "__main__":
    app.run("0.0.0.0",debug=True)
