import requests
from django.utils.deprecation import MiddlewareMixin

DEFAULT_STORE_CODE = 'AZ'


def get_store_from_ip(ip):
    """IP-dən ölkə kodunu tap, uyğun store qaytar"""
    # Localhost/development üçün skip
    if ip in ('127.0.0.1', '::1', 'localhost'):
        return DEFAULT_STORE_CODE
    try:
        resp = requests.get(f'https://ipapi.co/{ip}/country/', timeout=2)
        country = resp.text.strip().upper()
        from .models import Store
        for store in Store.objects.filter(is_active=True):
            codes = [c.strip().upper() for c in store.country_codes.split(',') if c.strip()]
            if country in codes:
                return store.code
    except Exception:
        pass
    return DEFAULT_STORE_CODE


class StoreMiddleware(MiddlewareMixin):
    """
    Hər request-də aktiv store-u müəyyən edir:
    1. ?store=XX query param  (manual switch, session-a yazır)
    2. Session-da saxlanılmış store
    3. IP-based geo-detection
    4. Default: AZ
    """

    def process_request(self, request):
        from .models import Store

        # 1. Manual switch via query param
        store_code = request.GET.get('store', '').upper()
        if store_code:
            try:
                store = Store.objects.get(code=store_code, is_active=True)
                request.session['store_code'] = store.code
                request.store = store
                return
            except Store.DoesNotExist:
                pass

        # 2. Session
        session_code = request.session.get('store_code', '').upper()
        if session_code:
            try:
                store = Store.objects.get(code=session_code, is_active=True)
                request.store = store
                return
            except Store.DoesNotExist:
                pass

        # 3. IP geo-detection
        ip = self._get_client_ip(request)
        code = get_store_from_ip(ip)
        try:
            store = Store.objects.get(code=code, is_active=True)
        except Store.DoesNotExist:
            store = Store.objects.filter(is_active=True).first()

        if store:
            request.session['store_code'] = store.code
        request.store = store

    def _get_client_ip(self, request):
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        if xff:
            return xff.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '127.0.0.1')