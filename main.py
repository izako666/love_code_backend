from flask import Flask, json, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore, messaging

app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate('serviceaccount.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

@app.route('/send_notification_alert', endpoint='send_notification_alert', methods=['POST'])
def send_notification():
    try:
        # Get data from request
        data = request.get_json()
        title = data.get('title')
        message = data.get('message')
        user_id = data.get('user_id')
        message_id = data.get('message_id')
        # Get user document from Firestore
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()

        if user_doc.exists:
            # Get push_token
            push_token = user_doc.get('push_token')
            # Create the message
            message = messaging.Message(
                android=messaging.AndroidConfig(
                    data={
                           "default_vibrate_timings": "False",
    "vibrate_timings": json.dumps([
                "0.0s",
                "0.2s",
                "0.1s",
                "0.2s",
                "0.3s",
                "0.1s",
                "0.4s"
     ]),
     "messagetype": "text/alert",
     "message_id": str(message_id)
                    },
                    priority='high',
                       notification=messaging.AndroidNotification(
                title=title,
                body=message,
                channel_id="alert_channel",
                vibrate_timings_millis=[0, 1000, 500, 1000, 500, 1000, 500, 1000, 500, 1000]  # Vibration pattern in milliseconds
            ),
                ),
                notification=messaging.Notification(
                    title=title,
                    body=message,
                ),
                token=push_token,
            )

            # Send the message
            response = messaging.send(message)
            return jsonify({'status': 'success', 'message_id': response}), 200
        else:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/send_notification_draw', endpoint='send_notification_draw', methods=['POST'])
def send_notification():
    try:
        # Get data from request
        data = request.get_json()
        title = data.get('title')
        message = data.get('message')
        user_id = data.get('user_id')
        message_id = data.get('message_id')

        # Get user document from Firestore
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()

        if user_doc.exists:
            # Get push_token
            push_token = user_doc.get('push_token')
            # Create the message
            message = messaging.Message(
                android=messaging.AndroidConfig(
                    data={
                           "default_vibrate_timings": "False",
    "vibrate_timings": json.dumps([
                "0.0s",
                "0.2s",
                "0.1s",
                "0.2s",
                "0.3s",
                "0.1s",
                "0.4s"
     ]),
     "messagetype": "text/draw",
     "message_id": str(message_id)
                    },
                    priority='high',
                       notification=messaging.AndroidNotification(
                title=title,
                body=message,
                channel_id="alert_channel",
                vibrate_timings_millis=[0, 1000, 500, 1000, 500, 1000, 500, 1000, 500, 1000]  # Vibration pattern in milliseconds
            ),
                ),
                notification=messaging.Notification(
                    title=title,
                    body=message,
                ),
                token=push_token,
            )

            # Send the message
            response = messaging.send(message)
            return jsonify({'status': 'success', 'message_id': response}), 200
        else:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/send_notification', endpoint='send_notification',  methods=['POST'])
def send_notification():
    try:
        # Get data from request
        data = request.get_json()
        title = data.get('title')
        message = data.get('message')
        user_id = data.get('user_id')
        message_id = data.get('message_id')
        # Get user document from Firestore
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()

        if user_doc.exists:
            # Get push_token
            push_token = user_doc.get('push_token')

            # Create the message
            message = messaging.Message(
                data={
                    "messagetype": "text",
                    "message_id": str(message_id)

                },
                notification=messaging.Notification(
                    title=title,
                    body=message,
                ),
                token=push_token,
            )

            # Send the message
            response = messaging.send(message)
            return jsonify({'status': 'success', 'message_id': response}), 200
        else:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
