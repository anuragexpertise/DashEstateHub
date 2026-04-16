import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create a JWT access token.
    
    Args:
        data: Dictionary containing user info (email, role, society_id, etc.)
        expires_delta: Optional custom expiration time
    
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    """
    Create a JWT refresh token (longer expiration).
    
    Args:
        data: Dictionary containing user info
    
    Returns:
        Encoded refresh token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "iat": datetime.utcnow(), "type": "refresh"})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    """
    Verify a JWT token and return the decoded payload.
    
    Args:
        token: JWT token string (with or without "Bearer " prefix)
    
    Returns:
        Decoded payload dict if valid, None if invalid
    """
    try:
        # Remove "Bearer " prefix if present
        if token.startswith("Bearer "):
            token = token[7:]
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Check if token type is not refresh (access token only)
        if payload.get("type") == "refresh":
            return None
        
        return payload
    except jwt.ExpiredSignatureError:
        print("Token expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None


def verify_refresh_token(token: str):
    """
    Verify a refresh token.
    
    Args:
        token: Refresh token string
    
    Returns:
        Decoded payload if valid refresh token, None otherwise
    """
    try:
        if token.startswith("Bearer "):
            token = token[7:]
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Check if token type is refresh
        if payload.get("type") != "refresh":
            return None
        
        return payload
    except jwt.ExpiredSignatureError:
        print("Refresh token expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid refresh token")
        return None


def require_auth(f):
    """
    Decorator to protect Flask routes with JWT.
    
    Usage:
        @app.route("/api/protected")
        @require_auth
        def protected_route():
            return {"message": "Success"}
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        
        if not token:
            return jsonify({"error": "Missing authorization token"}), 401
        
        payload = verify_token(token)
        
        if not payload:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        # Store payload in request context for use in the route
        request.user = payload
        return f(*args, **kwargs)
    
    return decorated_function


def get_user_from_token(token: str):
    """
    Extract user info from token without route protection.
    
    Args:
        token: JWT token string
    
    Returns:
        User payload dict or None
    """
    return verify_token(token)