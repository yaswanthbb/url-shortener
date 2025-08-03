from datetime import datetime
from threading import Lock

class URLStore:
    def __init__(self):
        self.url_map = {}
        self.lock = Lock()

    def save_url(self, short_code, original_url):
        with self.lock:
            self.url_map[short_code] = {
                'url': original_url,
                'created_at': datetime.utcnow(),
                'clicks': 0
            }

    def get_url(self, short_code):
        return self.url_map.get(short_code)

    def increment_click(self, short_code):
        with self.lock:
            if short_code in self.url_map:
                self.url_map[short_code]['clicks'] += 1

    def get_stats(self, short_code):
        return self.url_map.get(short_code)

store = URLStore()
