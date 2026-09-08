import re
import json
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/140.0 Mobile Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

def search(username):
    username = username.strip().lstrip("@")
    url = f"https://www.youtube.com/@{username}"

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

    title = re.search(
        r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\'](.*?)["\']',
        html,
        re.I | re.S
    )

    if title:
        result["display_name"] = title.group(1)

    description = re.search(
        r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\'](.*?)["\']',
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
        result["channel_image"] = image.group(1)

    canonical = re.search(
        r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\'](.*?)["\']',
        html,
        re.I | re.S
    )

    if canonical:
        result["canonical_url"] = canonical.group(1)

    channel_id = re.search(
        r'"channelId":"([^"]+)"',
        html
    )

    if channel_id:
        result["channel_id"] = channel_id.group(1)

    subscriber_count = re.search(
        r'"subscriberCountText":\{"simpleText":"([^"]+)"',
        html
    )

    if subscriber_count:
        result["subscribers"] = subscriber_count.group(1)

    video_count = re.search(
        r'"videosCountText":\{"runs":\[\{"text":"([^"]+)"',
        html
    )

    if video_count:
        result["videos"] = video_count.group(1)

    return result
