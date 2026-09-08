import requests

API = "https://api.github.com"
HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "IntelScope/1.0 (Public OSINT Research)"
}

def get(endpoint):
    response = requests.get(
        API + endpoint,
        headers=HEADERS,
        timeout=10
    )

    if response.status_code == 404:
        return None

    response.raise_for_status()
    return response.json()

def search(username):
    user = get(f"/users/{username}")

    if not user:
        return None

    result = {
        "username": user.get("login"),
        "display_name": user.get("name"),
        "bio": user.get("bio"),
        "profile_url": user.get("html_url"),
        "avatar_url": user.get("avatar_url"),
        "public_repositories": user.get("public_repos"),
        "followers": user.get("followers"),
        "following": user.get("following"),
        "public_gists": user.get("public_gists"),
        "company": user.get("company"),
        "location": user.get("location"),
        "website": user.get("blog"),
        "account_created": user.get("created_at"),
        "last_updated": user.get("updated_at")
    }

    repos = get(f"/users/{username}/repos?per_page=100&sort=updated")

    if repos:
        result["repositories"] = []

        for repo in repos:
            result["repositories"].append({
                "name": repo.get("name"),
                "description": repo.get("description"),
                "url": repo.get("html_url"),
                "language": repo.get("language"),
                "stars": repo.get("stargazers_count"),
                "forks": repo.get("forks_count"),
                "open_issues": repo.get("open_issues_count"),
                "created": repo.get("created_at"),
                "updated": repo.get("updated_at")
            })

    events = get(f"/users/{username}/events/public?per_page=30")

    if events:
        result["recent_public_activity"] = []

        for event in events:
            repo = event.get("repo", {}).get("name")

            result["recent_public_activity"].append({
                "type": event.get("type"),
                "repository": repo,
                "created": event.get("created_at")
            })

    return result
