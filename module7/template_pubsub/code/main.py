import os
from google.cloud import translate_v2 as translate
from google.cloud import pubsub_v1
import json
import base64
# Add any imports that you may need, but make sure to update requirements.txt

PROJECT_ID = 'cssmodule7'

translate_client = translate.Client()
publisher = pubsub_v1.PublisherClient()

# Create a Pub/Sub-triggered function named detect_language_pubsub that
# is triggered when a message is published to a Pub/Sub topic called user-input-text.
# The function must use the Google Translate API to detect the language in the Pub/Sub message
def detect_language_pubsub(event, context):
    if 'data' in event:
        text = base64.b64decode(event['data']).decode('utf-8')
        result = translate_client.detect_language(text)
        src_lang = result['language']

        message_json = json.dumps({'text': text, 'src_lang': src_lang})
        message_bytes = message_json.encode('utf-8')

        print(message_json)

        # If the language is detected as English, the function publishes a JSON string
        # to a Pub/Sub topic called translated-text.
        if src_lang == 'en':
            topic_path = publisher.topic_path(PROJECT_ID, 'translated-text')
            publisher.publish(topic_path, data=message_bytes)
        # If the language is not English, a JSON string is published
        # to the Pub/Sub topic called to-translate-text.
        else:
            topic_path = publisher.topic_path(PROJECT_ID, 'to-translate-text')
            publisher.publish(topic_path, data=message_bytes)

    return '', 200