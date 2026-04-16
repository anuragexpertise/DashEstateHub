import json
import os
from db import get_db

try:
    from pywebpush import webpush
    HAS_WEBPUSH = True
except ImportError:
    HAS_WEBPUSH = False
    print("Warning: pywebpush not installed. Push notifications disabled.")


def register_push_subscription(user_id, subscription):
    """
    Store push subscription for a user in the database.
    
    Args:
        user_id: ID of the user
        subscription: Push subscription object from browser
    """
    try:
        db = get_db()
        cur = db.cursor()
        
        # Note: You may need to add a push_subscriptions table
        # CREATE TABLE push_subscriptions (
        #     id SERIAL PRIMARY KEY,
        #     user_id INT REFERENCES users(id),
        #     endpoint VARCHAR(500),
        #     auth_key VARCHAR(100),
        #     p256dh_key VARCHAR(100),
        #     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        # );
        
        # For now, this is a placeholder
        print(f"Push subscription registered for user {user_id}")
        cur.close()
        db.close()
    except Exception as e:
        print(f"Error registering push subscription: {e}")


def send_push(subscription, title, body, data=None):
    """
    Send a push notification to a user.
    
    Args:
        subscription: User's push subscription object
        title: Notification title
        body: Notification body
        data: Additional data to send
    """
    if not HAS_WEBPUSH:
        print("Push notifications disabled (pywebpush not installed)")
        return False
    
    try:
        payload = {
            "title": title,
            "body": body,
            "data": data or {}
        }
        
        webpush(
            subscription_info=subscription,
            data=json.dumps(payload),
            vapid_private_key=os.getenv("VAPID_PRIVATE"),
            vapid_claims={"sub": f"mailto:{os.getenv('VAPID_EMAIL')}"}
        )
        
        print(f"Push notification sent: {title}")
        return True
    except Exception as e:
        print(f"Error sending push notification: {e}")
        return False


def get_user_subscription(user_id):
    """
    Retrieve a user's push subscription from database.
    
    Args:
        user_id: ID of the user
    
    Returns:
        Subscription object or None
    """
    try:
        # Placeholder for database query
        # SELECT endpoint, auth_key, p256dh_key FROM push_subscriptions
        # WHERE user_id = %s
        return None
    except Exception as e:
        print(f"Error retrieving push subscription: {e}")
        return None
