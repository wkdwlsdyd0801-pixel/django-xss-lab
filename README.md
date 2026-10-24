# xss-lab

A Django board that renders user input two ways: a **vulnerable** mode that prints raw HTML (so `<script>` runs) and a **safe** mode that relies on output escaping plus a Content-Security-Policy header.

> ⚠️ Intentionally vulnerable. Run locally only.

## Run

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

- Stored XSS: open http://127.0.0.1:8000/ — the seeded `attacker` post pops an alert in `?mode=vulnerable` but is shown as text in `?mode=safe`.
- Reflected XSS: on the board page follow the "반사형 XSS 데모" link; the `?mode=vulnerable` URL runs a script, the `?mode=safe` URL does not.
