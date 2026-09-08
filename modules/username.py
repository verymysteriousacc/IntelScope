import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

SITES = {
    "Instagram": "https://www.instagram.com/{}/",
    "GitHub": "https://github.com/{}/",
    "Reddit": "https://www.reddit.com/user/{}/",
    "TikTok": "https://www.tiktok.com/@{}",
    "YouTube": "https://www.youtube.com/@{}",
    "X": "https://x.com/{}",
    "Twitch": "https://www.twitch.tv/{}",
    "Pinterest": "https://www.pinterest.com/{}/",
    "SoundCloud": "https://soundcloud.com/{}",
    "GitLab": "https://gitlab.com/{}",
    "Codeberg": "https://codeberg.org/{}",
    "Keybase": "https://keybase.io/{}",
    "Dev.to": "https://dev.to/{}",
    "Medium": "https://medium.com/@{}",
    "BuyMeACoffee": "https://buymeacoffee.com/{}",
    "Patreon": "https://www.patreon.com/{}",
    "Kaggle": "https://www.kaggle.com/{}",
    "Docker Hub": "https://hub.docker.com/u/{}",
    "Hugging Face": "https://huggingface.co/{}",
    "PyPI": "https://pypi.org/user/{}/",
    "Replit": "https://replit.com/@{}",
    "Steam": "https://steamcommunity.com/id/{}/",
    "Linktree": "https://linktr.ee/{}",
    "Gravatar": "https://gravatar.com/{}",
    "Flickr": "https://www.flickr.com/people/{}/"
}

HEADERS = {
    "User-Agent": "IntelScope/1.0 (Public OSINT Research)"
}

def check_site(site, template, username):
    url = template.format(username)

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10,
            allow_redirects=True
        )

        final_url = response.url

        if response.status_code == 200:
            status = "FOUND"
        elif response.status_code == 404:
            status = "NOT FOUND"
        elif response.status_code in (401, 403):
            status = "RESTRICTED"
        elif 300 <= response.status_code < 400:
            status = "REDIRECT"
        else:
            status = f"HTTP {response.status_code}"

        return {
            "site": site,
            "url": url,
            "final_url": final_url,
            "status": status,
            "code": response.status_code
        }

    except requests.Timeout:
        return {
            "site": site,
            "url": url,
            "final_url": None,
            "status": "TIMEOUT",
            "code": None
        }

    except requests.RequestException:
        return {
            "site": site,
            "url": url,
            "final_url": None,
            "status": "ERROR",
            "code": None
        }

def search_username(username):
    username = username.strip().lstrip("@")

    results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        tasks = [
            executor.submit(check_site, site, template, username)
            for site, template in SITES.items()
        ]

        for task in as_completed(tasks):
            results.append(task.result())

    return sorted(results, key=lambda x: x["site"].lower())
