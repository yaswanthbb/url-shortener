import random
import string
import re
from urllib.parse import urlparse

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def is_valid_url(url):
    try:
        parsed = urlparse(url)
        return all([parsed.scheme in ["http", "https"], parsed.netloc])
    except Exception:
        return False
