import re
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/140.0 Mobile Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

def extract(pattern, html):
    match = re.search(pattern, html, re.I | re.S)
    return match.group(1).strip() if match else None

def search(username):
    username = username.strip().lstrip("@")
    url = f"https://www.twitch.tv/{username}"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10,
            allow_redirects=True
        )
    except requests.RequestException:
        return None

    if response.status_code == 404:
        return None

    if response.status_code in (401, 403, 429):
        return {
            "username": username,
            "profile_url": url,
            "status": "RESTRICTED",
            "http_status": response.status_code
        }

    if response.status_code != 200:
        return {
            "username": username,
            "profile_url": url,
            "status": f"HTTP {response.status_code}"
        }

    html = response.text

    result = {
        "username": username,
        "profile_url": response.url,
        "status": "FOUND"
    }

    result["display_name"] = extract(
        r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\'](.*?)["\']',
        html
    )

    result["description"] = extract(
        r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\'](.*?)["\']',
        html
    )

    result["profile_image"] = extract(
        r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\'](.*?)["\']',
        html
    )

    result["canonical_url"] = extract(
        r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\'](.*?)["\']',
        html
    )

    title = extract(r"<title>(.*?)</title>", html)

    if title:
        result["page_title"] = title

    return result
