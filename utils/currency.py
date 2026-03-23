import requests
import time
import logging

logger = logging.getLogger(__name__)

# Simple in-memory cache
# Format: {'EGP': {'rate': 50.0, 'expiry': 123456789}}
_RATE_CACHE = {}
CACHE_DURATION = 3600  # 1 hour

def get_exchange_rate(target='EGP'):
    """Fetch real-time exchange rate from USD to target currency."""
    global _RATE_CACHE
    now = time.time()
    
    if target in _RATE_CACHE and _RATE_CACHE[target]['expiry'] > now:
        return _RATE_CACHE[target]['rate']
    
    try:
        # Using exchangerate-api.com (Free tier, no key needed for some endpoints or public ones)
        # However, it's better to use a reliable public one.
        # api.exchangerate-api.com/v4/latest/USD is a common free public endpoint.
        url = f"https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if 'rates' in data and target in data['rates']:
            rate = data['rates'][target]
            _RATE_CACHE[target] = {
                'rate': rate,
                'expiry': now + CACHE_DURATION
            }
            logger.info(f"Updated exchange rate: 1 USD = {rate} {target}")
            return rate
    except Exception as e:
        logger.error(f"Error fetching exchange rate: {e}")
    
    # Fallback to a reasonable default if API fails and no cache exists
    if target == 'EGP':
        return 50.0 # Default fallback
    return 1.0


def format_currency_dual(amount_usd, target_currency='EGP', lang='ar', show_secondary=True):
    """
    Formats amount from USD base to: $0.20 (~ 10.00 جنيه) or similar.
    amount_usd is in USD.
    """
    if not show_secondary:
        if lang == 'ar':
            return f"{amount_usd:.2f}$"
        else:
            return f"${amount_usd:.2f}"

    # Identify secondary currency and amount
    if target_currency == 'USD':
        # Default secondary is EGP if pref is USD
        rate_egp = get_exchange_rate('EGP')
        amount_secondary = amount_usd * rate_egp
        cur_secondary = "جنيه" if lang == 'ar' else "EGP"
    else:
        rate_target = get_exchange_rate(target_currency)
        amount_secondary = amount_usd * rate_target
        if target_currency == 'EGP' and lang == 'ar':
            cur_secondary = "جنيه"
        else:
            cur_secondary = target_currency

    if lang == 'ar':
        return f"{amount_usd:.2f}$ (~ {amount_secondary:.2f} {cur_secondary})"
    else:
        return f"${amount_usd:.2f} (~ {amount_secondary:.2f} {cur_secondary})"
