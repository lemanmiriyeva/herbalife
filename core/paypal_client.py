import requests
import json
from django.conf import settings


def _get_paypal_config():
    """settings.py-dən PayPal config al"""
    mode = getattr(settings, 'PAYPAL_MODE', 'sandbox')  # 'sandbox' | 'live'
    if mode == 'live':
        base_url   = 'https://api-m.paypal.com'
        client_id  = settings.PAYPAL_LIVE_CLIENT_ID
        secret     = settings.PAYPAL_LIVE_SECRET
    else:
        base_url   = 'https://api-m.sandbox.paypal.com'
        client_id  = settings.PAYPAL_SANDBOX_CLIENT_ID
        secret     = settings.PAYPAL_SANDBOX_SECRET
    return base_url, client_id, secret


def _get_access_token():
    """PayPal OAuth2 token al"""
    base_url, client_id, secret = _get_paypal_config()
    resp = requests.post(
        f'{base_url}/v1/oauth2/token',
        auth=(client_id, secret),
        data={'grant_type': 'client_credentials'},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()['access_token']


def create_paypal_order(amount: float, currency: str, order_id: int, return_url: str, cancel_url: str) -> dict:
    """
    PayPal order yarat.
    Returns: {'id': 'PAYPAL_ORDER_ID', 'approve_url': 'https://...'}
    """
    base_url, _, _ = _get_paypal_config()
    token = _get_access_token()

    payload = {
        'intent': 'CAPTURE',
        'purchase_units': [{
            'reference_id': str(order_id),
            'description':  f'Herbalife Order #{order_id}',
            'amount': {
                'currency_code': currency,
                'value': f'{amount:.2f}',
            },
        }],
        'application_context': {
            'brand_name':          'Herbalife Nutrition',
            'landing_page':        'BILLING',
            'user_action':         'PAY_NOW',
            'return_url':          return_url,
            'cancel_url':          cancel_url,
            'shipping_preference': 'NO_SHIPPING',
        },
    }

    resp = requests.post(
        f'{base_url}/v2/checkout/orders',
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type':  'application/json',
        },
        json=payload,
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()

    # Approve URL-i tap
    approve_url = next(
        (link['href'] for link in data.get('links', []) if link['rel'] == 'approve'),
        None
    )
    return {'id': data['id'], 'approve_url': approve_url}


def capture_paypal_order(paypal_order_id: str) -> dict:
    """
    PayPal orderi capture et (ödənişi tamamla).
    Returns: {'status': 'COMPLETED', ...}
    """
    base_url, _, _ = _get_paypal_config()
    token = _get_access_token()

    resp = requests.post(
        f'{base_url}/v2/checkout/orders/{paypal_order_id}/capture',
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type':  'application/json',
        },
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


def get_paypal_order(paypal_order_id: str) -> dict:
    """PayPal order statusunu yoxla"""
    base_url, _, _ = _get_paypal_config()
    token = _get_access_token()

    resp = requests.get(
        f'{base_url}/v2/checkout/orders/{paypal_order_id}',
        headers={'Authorization': f'Bearer {token}'},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()