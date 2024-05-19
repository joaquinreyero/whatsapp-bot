import json


def process_notification(self, data):
    entries = data["entry"]
    for entry in entries:
        for change in entry["changes"]:
            value = change["value"]
            if value:
                if "messages" in value:
                    for message in value["messages"]:
                        if message["type"] == "text":
                            from_no = message["from"]
                            message_body = message["text"]["body"]
                            prompt = message_body
                            print(f"Ack from FastAPI-WtsApp Webhook: {message_body}")
                            return {
                                "statusCode": 200,
                                "body": prompt,
                                "from_no": from_no,
                                "isBase64Encoded": False
                            }

    return {
        "statusCode": 403,
        "body": json.dumps("Unsupported method"),
        "isBase64Encoded": False
    }
