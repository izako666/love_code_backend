from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore, messaging

app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate('serviceaccount.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

@app.route('/send_notification', methods=['POST'])
def send_notification():
    try:
        # Get data from request
        data = request.get_json()
        title = data.get('title')
        message = data.get('message')
        user_id = data.get('user_id')

        # Get user document from Firestore
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()

        if user_doc.exists:
            # Get push_token
            push_token = user_doc.get('push_token')

            # Create the message
            message = messaging.Message(
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
    app.run(debug=True)
