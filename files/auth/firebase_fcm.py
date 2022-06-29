from firebase_admin import messaging

def subscribe_news(tokens): # tokens is a list of registration tokens
    topic = "fire_alert"
    response = messaging.subscribe_to_topic(tokens, topic)
    if response.failure_count > 0:
        print(f"Failed to subscribe to topic {topic} due to {list(map(lambda e: e.reason,response.errors))}")

def send_topic_push(title, body, data):
    topic = "fire_alert"
    message = messaging.Message(
        notification = messaging.Notification(
            title=title,
            body=body
        ),
        data = data,
        topic = topic
    )
    messaging.send(message)
