from flask import Blueprint, request, jsonify
from auth.jwt_utils import create_access_token, create_refresh_token, verify_refresh_token, require_auth
from services.auth_service import authenticate_user
from db import get_db
import os

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/start-auth", methods=["POST"])
def start_auth():
    """
    Initiate login flow - verify email and send push notification.
    
    Request body:
        {
            "email": "user@example.com",
            "password": "password123"  (or PIN/pattern for other methods)
        }
    """
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        society_id = data.get("society_id")  # Optional, for multi-tenant
        
        if not email or not password:
            return jsonify({"error": "Email and password required"}), 400
        
        # Authenticate user with existing service
        user = authenticate_user(email, password, society_id)
        
        if not user:
            return jsonify({"error": "Invalid credentials"}), 401
        
        # Generate tokens
        access_token = create_access_token({
            "user_id": user["user_id"],
            "email": user["email"],
            "role": user["role"],
            "society_id": user["society_id"]
        })
        
        refresh_token = create_refresh_token({
            "user_id": user["user_id"],
            "email": user["email"]
        })
        
        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user,
            "token_type": "Bearer"
        }), 200
    
    except Exception as e:
        print(f"Auth error: {e}")
        return jsonify({"error": "Authentication failed"}), 500


@auth_bp.route("/refresh", methods=["POST"])
def refresh_access_token():
    """
    Refresh expired access token using refresh token.
    
    Request body:
        {
            "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
        }
    """
    try:
        data = request.get_json()
        refresh_token = data.get("refresh_token")
        
        if not refresh_token:
            return jsonify({"error": "Refresh token required"}), 400
        
        payload = verify_refresh_token(refresh_token)
        
        if not payload:
            return jsonify({"error": "Invalid or expired refresh token"}), 401
        
        # Create new access token with same user info
        access_token = create_access_token({
            "user_id": payload["user_id"],
            "email": payload["email"]
        })
        
        return jsonify({
            "access_token": access_token,
            "token_type": "Bearer"
        }), 200
    
    except Exception as e:
        print(f"Refresh error: {e}")
        return jsonify({"error": "Token refresh failed"}), 500


@auth_bp.route("/verify-token", methods=["POST"])
def verify_token():
    """
    Verify if a token is valid (no expiration).
    
    Request headers:
        Authorization: Bearer <token>
    """
    try:
        token = request.headers.get("Authorization")
        
        if not token:
            return jsonify({"valid": False}), 401
        
        from auth.jwt_utils import verify_token as verify
        payload = verify(token)
        
        if not payload:
            return jsonify({"valid": False}), 401
        
        return jsonify({"valid": True, "user": payload}), 200
    
    except Exception as e:
        print(f"Verify error: {e}")
        return jsonify({"valid": False}), 500


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """
    Logout - on client side, remove tokens from localStorage.
    This endpoint is optional for server-side token blacklist (not implemented).
    """
    return jsonify({"message": "Logged out successfully"}), 200


@auth_bp.route("/protected-example", methods=["GET"])
@require_auth
def protected_example():
    """
    Example protected route - requires valid JWT.
    """
    user = request.user
    return jsonify({
        "message": "Access granted",
        "user_id": user.get("user_id"),
        "email": user.get("email")
    }), 200
