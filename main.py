from flask import Flask, json, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore, messaging, auth
import requests

app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate('serviceaccount.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()
FIREBASE_WEB_API_KEY = 'AIzaSyBqcNWm95-f7dcNOaG__uf-VmX71bJ6Aq4'
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



@app.route('/send_effect', endpoint='send_effect',  methods=['POST'])
def send_effect():
    try:
        # Get data from request
        data = request.get_json()
        effect_type = data.get('effect_type')
        user_id = data.get('user_id')
        # Get user document from Firestore
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()

        if user_doc.exists:
            # Get push_token
            push_token = user_doc.get('push_token')

            # Create the message
            message = messaging.Message(
                data={
                    "effect_type": str(effect_type),
                },
              
                token=push_token,
            )

            # Send the message
            response = messaging.send(message)
            return jsonify({'status': 'success', 'message_id': response}), 200
        else:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

def verify_password(email, password):
    # Verify user email and password using Firebase Authentication REST API
    url = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}'
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(url, json=payload)
    return response.json()

def delete_document_and_subcollections(doc_ref):
    # Get all subcollections of the document
    subcollections = doc_ref.collections()
    
    for subcollection in subcollections:
        # For each subcollection, get all documents
        for subdoc in subcollection.stream():
            # Recursively delete each document and its subcollections
            delete_document_and_subcollections(subdoc.reference)
    
    # Delete the document itself
    doc_ref.delete()
@app.route('/delete_user', methods=['POST'])
def delete_user():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Verify the user's password
        verify_response = verify_password(email, password)
        if 'error' in verify_response:
            return jsonify({"error": "Invalid email or password"}), 400

        # Get user UID from the response
        user_uid = verify_response['localId']
        # Create references to the "chats" collection
        chats_ref = db.collection("chats")

        # Create queries for "user_id" and "other_user_id"
        query_user_id = chats_ref.where("user_id", "==", user_uid)

        query_other_user_id = chats_ref.where("other_user_id", "==", user_uid)

        # Stream results from both queries
        docs_user_id = list(query_user_id.stream())

        docs_other_user_id = list(query_other_user_id.stream())

        # Combine results
        all_docs = docs_user_id + docs_other_user_id
        # Remove duplicates (if any)
        unique_docs = {doc.id: doc for doc in all_docs}.values()

        # Initialize variable to store the document ID
        document_id = None

        # Check if unique_docs is not empty
        if unique_docs:
        # Get the first document and store its ID
            first_doc = next(iter(unique_docs))
            document_id = first_doc.id

            chat_doc_final = db.collection("chats").document(document_id).get()
            delete_document_and_subcollections(db.collection("chats").document(document_id))

        # Delete the user
        auth.delete_user(user_uid)

        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=False)
