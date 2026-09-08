import re
import json
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/140.0 Mobile Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

def search(username):
    username = username.strip().lstrip("@")
    url = f"https://www.instagram.com/{username}/"

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

    title = re.search(r"<title>(.*?)</title>", html, re.I | re.S)

    if title:
        result["page_title"] = title.group(1).strip()

    description = re.search(
        r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']',
        html,
        re.I | re.S
    )

    if description:
        result["description"] = description.group(1)

    image = re.search(
        r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\'](.*?)["\']',
        html,
        re.I | re.S
    )

    if image:
        result["profile_image"] = image.group(1)

    og_url = re.search(
        r'<meta[^>]+property=["\']og:url["\'][^>]+content=["\'](.*?)["\']',
        html,
        re.I | re.S
    )

    if og_url:
        result["canonical_url"] = og_url.group(1)

    scripts = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html,
        re.I | re.S
    )

    for script in scripts:
        try:
            data = json.loads(script)

            if isinstance(data, dict):
                if data.get("name"):
                    result["display_name"] = data["name"]

                if data.get("description"):
                    result["bio"] = data["description"]

                if data.get("url"):
                    result["profile_url"] = data["url"]

                if data.get("image"):
                    result["profile_image"] = data["image"]

        except (json.JSONDecodeError, TypeError):
            continue

    return result
