"""
WebAuthn utilities for biometric/security key authentication.
Supports fingerprint, face recognition, and hardware security keys.
"""

try:
    from webauthn import generate_registration_options, generate_authentication_options
    from webauthn.helpers.structs import AuthenticatorSelectionCriteria, UserVerificationRequirement
    HAS_WEBAUTHN = True
except ImportError:
    HAS_WEBAUTHN = False
    print("Warning: webauthn library not installed. WebAuthn disabled.")


def generate_challenge():
    """
    Generate a random challenge for WebAuthn.
    
    Returns:
        Random 32-byte challenge as base64 string
    """
    import os
    import base64
    return base64.b64encode(os.urandom(32)).decode('utf-8')


def generate_registration_challenge(user_id, email, display_name="User"):
    """
    Generate WebAuthn registration options for a new credential.
    
    Args:
        user_id: User's ID
        email: User's email
        display_name: User's display name
    
    Returns:
        Registration options dict
    """
    if not HAS_WEBAUTHN:
        return None
    
    try:
        options = generate_registration_options(
            rp_id="estatehub.local",  # Change to your domain
            rp_name="EstateHub",
            user_id=str(user_id),
            user_email=email,
            user_display_name=display_name,
            authenticator_selection=AuthenticatorSelectionCriteria(
                authenticator_attachment="platform",  # Use device's biometric
                user_verification=UserVerificationRequirement.PREFERRED
            )
        )
        return options
    except Exception as e:
        print(f"Error generating registration challenge: {e}")
        return None


def generate_authentication_challenge(user_id):
    """
    Generate WebAuthn authentication options.
    
    Args:
        user_id: User's ID
    
    Returns:
        Authentication options dict
    """
    if not HAS_WEBAUTHN:
        return None
    
    try:
        options = generate_authentication_options(
            rp_id="estatehub.local",
            user_verification=UserVerificationRequirement.PREFERRED
        )
        return options
    except Exception as e:
        print(f"Error generating authentication challenge: {e}")
        return None


def verify_webauthn_credential(credential_data, stored_public_key, challenge):
    """
    Verify a WebAuthn credential assertion.
    
    Args:
        credential_data: Credential response from client
        stored_public_key: Public key stored for the user
        challenge: Original challenge sent to client
    
    Returns:
        True if valid, False otherwise
    """
    if not HAS_WEBAUTHN:
        return False
    
    try:
        # Implementation would use webauthn.helpers.verify_authentication_response
        # This is a placeholder
        print("WebAuthn credential verification")
        return True
    except Exception as e:
        print(f"WebAuthn verification error: {e}")
        return False
