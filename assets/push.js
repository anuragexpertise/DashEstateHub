/**
 * Push Notification utilities for EstateHub
 * Handles registration and sending of push notifications
 */

class PushManager {
  constructor() {
    this.serviceWorkerUrl = '/assets/sw.js';
    this.publicVapidKey = null; // Load from server
  }

  /**
   * Register service worker and request notification permission
   */
  async init() {
    try {
      // Check browser support
      if (!('serviceWorker' in navigator)) {
        console.warn('Service Workers not supported');
        return false;
      }

      // Register service worker
      const registration = await navigator.serviceWorker.register(this.serviceWorkerUrl);
      console.log('Service Worker registered:', registration);

      // Check notification permission
      if (!('Notification' in window)) {
        console.warn('Notifications not supported');
        return false;
      }

      // Request permission if needed
      if (Notification.permission === 'denied') {
        console.warn('Notification permission denied');
        return false;
      }

      if (Notification.permission !== 'granted') {
        const permission = await Notification.requestPermission();
        if (permission !== 'granted') {
          console.warn('Notification permission not granted');
          return false;
        }
      }

      // Subscribe to push notifications
      await this.subscribeUserToPush(registration);
      return true;
    } catch (error) {
      console.error('Error initializing push:', error);
      return false;
    }
  }

  /**
   * Subscribe user to push notifications
   */
  async subscribeUserToPush(swRegistration) {
    try {
      // Get VAPID public key from server
      const response = await fetch('/auth/vapid-public-key');
      const data = await response.json();
      this.publicVapidKey = data.vapid_public_key;

      const subscription = await swRegistration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: this.urlBase64ToUint8Array(this.publicVapidKey)
      });

      console.log('Push subscription:', subscription);

      // Send subscription to server
      await fetch('/auth/register-push', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify(subscription)
      });

      console.log('Push subscription registered with server');
    } catch (error) {
      console.error('Error subscribing to push:', error);
    }
  }

  /**
   * Convert VAPID key from base64 to Uint8Array
   */
  urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
      .replace(/\-/g, '+')
      .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i);
    }

    return outputArray;
  }

  /**
   * Request biometric verification
   * Called when user clicks a push notification for login approval
   */
  async requestBiometric(challenge) {
    try {
      if (!window.PublicKeyCredential) {
        console.warn('WebAuthn not supported');
        return null;
      }

      const credential = await navigator.credentials.get({
        publicKey: {
          challenge: this.str2ab(challenge),
          timeout: 60000,
          userVerification: 'preferred'
        }
      });

      console.log('Biometric verification successful:', credential);
      return credential;
    } catch (error) {
      console.error('Biometric verification error:', error);
      return null;
    }
  }

  /**
   * Convert string to ArrayBuffer
   */
  str2ab(str) {
    const buf = new ArrayBuffer(str.length);
    const bufView = new Uint8Array(buf);
    for (let i = 0, strLen = str.length; i < strLen; i++) {
      bufView[i] = str.charCodeAt(i);
    }
    return buf;
  }

  /**
   * Show local notification (for testing)
   */
  showNotification(title, options = {}) {
    if (!('serviceWorker' in navigator)) {
      console.warn('Service Workers not supported');
      return;
    }

    navigator.serviceWorker.ready.then(registration => {
      registration.showNotification(title, {
        icon: '/assets/RRARWA LOGO.PNG',
        badge: '/assets/RRARWA LOGO.PNG',
        ...options
      });
    });
  }
}

// Export for use in HTML
const pushManager = new PushManager();

// Auto-init on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => pushManager.init());
} else {
  pushManager.init();
}
