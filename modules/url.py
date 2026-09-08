import requests
from urllib.parse import urlparse

HEADERS = {
    "User-Agent": "IntelScope/1.0 (Public OSINT Research)"
}

def analyze_url(url):
    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    result = {
        "url": url,
        "scheme": parsed.scheme,
        "hostname": parsed.hostname,
        "port": parsed.port,
        "path": parsed.path or "/"
    }

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10,
            allow_redirects=True
        )

        result.update({
            "status_code": response.status_code,
            "final_url": response.url,
            "server": response.headers.get("Server"),
            "content_type": response.headers.get("Content-Type"),
            "content_length": response.headers.get("Content-Length"),
            "redirects": len(response.history),
            "security_headers": {
                "HSTS": response.headers.get("Strict-Transport-Security"),
                "CSP": response.headers.get("Content-Security-Policy"),
                "X-Frame-Options": response.headers.get("X-Frame-Options"),
                "X-Content-Type-Options": response.headers.get("X-Content-Type-Options")
            }
        })

    except requests.Timeout:
        result["error"] = "Request timed out"

    except requests.RequestException as error:
        result["error"] = str(error)

    return result
