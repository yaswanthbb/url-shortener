## CHANGES.md

### Implementation Notes

- Built a basic URL shortening service using **Flask**.
- Used an **in-memory dictionary** to store short codes and associated metadata.
- Added concurrency-safe access using `threading.Lock` to avoid race conditions.
- Created utility functions for:
  - Validating URLs
  - Generating unique 6-character short codes
- Implemented 3 main API endpoints:
  - `POST /api/shorten` to shorten URLs
  - `GET /<short_code>` to redirect
  - `GET /api/stats/<short_code>` to view analytics
- Wrote tests using `pytest` to cover all major functionalities.

---

### AI Used For : 

- Toke Help of Chatgpt to write test cases and models.
